#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include <Python.h>

#include "approx_pi.h"

static PyObject *py_approx_pi(PyObject *self, PyObject *args, PyObject *keywords) {
  /* Wraps approx_pi
   * This is the corresponding python function
   */
  unsigned int n_attempts;

  if(!PyArg_ParseTupleAndKeywords(args, keywords,
				 "i:approx_pi",
				 (char*[]){
				   "n_attempts", NULL},
				 &n_attempts)
     ) Py_RETURN_NONE;
  double pi = approx_pi(n_attempts);

  return PyFloat_FromDouble(pi);
}

static PyMethodDef methods[] = {
                                { "approx_pi", (PyCFunction)py_approx_pi, METH_VARARGS | METH_KEYWORDS, "approx_pi" },
                                { NULL, NULL, 0, NULL }
};

static struct PyModuleDef module_def = {
                                        .m_base = PyModuleDef_HEAD_INIT,
                                        .m_name = "pi",   /* name of module */
                                        .m_doc = NULL, /* module documentation, may be NULL */
                                        .m_size = -1,       /* size of per-interpreter state of the module,
                                                               or -1 if the module keeps state in global variables. */
                                        .m_methods = methods,
                                        .m_slots = NULL
};

PyMODINIT_FUNC
PyInit_pi(void) {
  return PyModule_Create(&module_def);
}
