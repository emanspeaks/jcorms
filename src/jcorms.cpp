#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <datetime.h>
#include <structmember.h>

#include "jcorms.h"

static PyObject* test_c(PyObject* self, PyObject* args)
{
  Py_RETURN_NONE;
}

static PyMethodDef jcorms_methods[] = {
  {"test", (PyCFunction)test_c, METH_VARARGS, PyDoc_STR("A test docstring.")},
  {NULL, NULL, 0, NULL} /* sentinel */
};

static int jcorms_exec(PyObject* m)
{
  if (PyModule_AddStringConstant(m, "__version__", STRINGIFY(JCORMS_VERSION))
      || PyModule_AddStringConstant(m, "__author__", STRINGIFY(JCORMS_AUTHOR))
  ) return -1;
  return 0;
}

static PyModuleDef_Slot jcorms_slots[] = {
  {Py_mod_exec, (void*)jcorms_exec},
  {0, NULL}
};

static PyModuleDef jcorms_mod = {
  PyModuleDef_HEAD_INIT, /* m_base */
  "jcorms",              /* m_name */
  PyDoc_STR("JSON-C Object Relational Mapping Structures"),
  0,                     /* m_size */
  jcorms_methods,        /* m_methods */
  jcorms_slots,          /* m_slots */
  NULL,                  /* m_traverse */
  NULL,                  /* m_clear */
  NULL                   /* m_free */
};

PyMODINIT_FUNC PyInit_jcorms()
{
  return PyModuleDef_Init(&jcorms_mod);
}
