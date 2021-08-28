# JCORMS design/theory

While the ORM in JCORMS is to imply that its syntax is similar to that of a true
object relational mapper for a database, JCORMS is not a database frontend.
It is, however, helpful to consider the analogues to a database when trying to
understand the general concepts.

JCORMS objects are similar to records in a relational database.  Instances of a
class all have common fields, so the class is similar to the table.  Some of
the fields can include pointers to other objects, which are like foreign keys.
Herein lies the difficulty in implementation.

While there is debate among the computer science community as to the difference
between marshalling and serializing, in this author's eyes, marshalling is about
transforming data between formats without the explicit intent of transmission
over a stream while serialization includes preparing that data to be streamed.
It could be argued that JCORMS is more of a marshalling engine because even
where the JSON in the name is concerned we don't generate the JSON: we create
data structures that are compatible with JSON serialization instead.  As for the
C interfaces part, the intent is to create objects to pass by reference via
a foreign function interface, either internal or external to JCORMS.  It is
arguable that is considered a parallel communication instead of a serial one
as if over a stream.  Therefore, it is probably most accurate to call JCORMS
a marshalling engine.

Since JCORMS is inherently a system for streamlining marshalling of objects,
there are times when unmarshalling we may encounter a pointer of some sort to
another object not yet unmarshalled.  As such, we must address how to handle
this unresolved reference.  To a user, this should be a black box, so for now
I will not discuss the internal handling of this.  However, there are use cases
where a user may want to provide a reference that, at the time of the
assignment, the pointer may not be resolved easily.

For a database, this is easy.  A simple database can allow setting a foreign
key field without validating that given key.  Since this is the syntax/behavior
we are attempting to emulate, there has to be some support of this capability.
The burden of resolving the pointer should be on JCORMS and only kicking back to
the user if it cannot validate the pointer on its own.

The problem arises from the fact that the envisioned use cases for JCORMS
include trees of objects.  A given object can share an edge with two other
objects in the tree and thus have two "parents."  Since "vague" references
depend on context information to resolve (perhaps we allow the user to specify
a foreign object's name instead of some globally-unique identifier), we require
calling information to resolve.  Python does not inherently provide easy access
to the call stack in a reliable way without requiring interpreter-specific
details, so we must use another way to get the context.  One such solution
can be found here: <https://stackoverflow.com/a/15838968>.

What if, however, we want to allow users to leverage vague references
intentionally?  For example, we create object A that refers to another
object in the tree by name, but because it can belong to two trees that may both
contain different objects with that same name, the resolution can be
context-dependent.  We need to protect for this use case in the design
of JCORMS.

Perhaps the solution is that the resolution of the pointer can only ever be done
just-in-time whenever handling a getter for the attribute storing the pointer.
If no context is given, return the "pointer" itself.  If the context can be
somehow extracted, then resolve the pointer.

This is where we must consider the black box internals for the marshalling
process.  Consider the following Python code:

```python
# ordinarily this class would be imported as a black box; only shown here
# are the pertinent parts for illustration.  Assume metaclass mechanism has been
# provided already to handle converting the class members to instance members.
class JcormsStruct:
    def marshall(self):
        z = dict()
        for key, value in self.__dict__.items():
            z[key] = value.marshall()


class A(JcormsStruct):
    name = JcormsField(name='name', datatype=str)
    data = JcormsPointer(name='data', datatype='A', default=None,
                         searchattrs=('name',), searchpool=('B.q',), )


class B(JcormsStruct):
    q = JcormsArray(name='q', datatype=A)


c = A()
c.name = "foo"
d = A()
d.name = "foo"
e = A()
e.name = "bar"
e.data = "foo"
f = B()
f.q = [c, e]
g = B()
g.q = [d, e]
f.marshall()
```

In this example, the `e.data` pointer should resolve to the object `c` since it
is part of the namespace of `f`.
However, the `searchpool` parameter leaves it to JCORMS to find the correct
object of type `B`.  The given implementation simply does not provide adequate
context to find `f` without querying the entire heap for objects of type `B`.
This is not an ideal scenario if we are to be thread-safe, not to mention the
lack of call stack information due to the method of calling via
`value.marshall()` in the `for` loop.

One could assume, since the `for` loop is an implementation detail inside
the JCORMS black box, that we provide some argument manually to `marshall()` in
the call to pass tree/stack information.  We can look to the implementation
of `deepcopy` for inspiration, which has a similar design problem.  It uses the
`memo` dictionary to keep track of objects it has already copied.
Using something like this would allow for keeping things more thread-safe by not
relying on the heap alone to find the tree.

JCORMS also has parallels with pickling.
