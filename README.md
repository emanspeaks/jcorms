# jcorms

JSON-C Object Relational Mapping Structures: strictly-typed serializable
structures for Python

JCORMS provides a means to create structures for seamlessly passing data between
Python and C APIs.  The design use case is for Python packages that manipulate
input files for applications written in other, more strictly-typed
languages--notably C or even modern Fortran.  In some cases, these applications
use JSON-like data structures, so it is important to be able to serialize
these structures to dictionaries of primitives compatible with JSON.  The goal
is to make the code necessary for the serialization transparent to the user.

JCORMS also provides an alternative foreign function interface (FFI) to Ctypes.
Ctypes provides just-in-time conversion of data from Python to C type, while
JCORMS provides eager type coercion at assignment time.  Data is stored in C
buffers so that at API call time a pointer to the buffer can be passed with no
delay. Having the type coercion happening at the C level instead of Python will
also provide some performance benefits over a wrapper to Ctypes.
