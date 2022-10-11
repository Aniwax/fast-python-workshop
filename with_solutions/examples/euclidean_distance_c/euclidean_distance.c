#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

static _Bool check(_Bool result, PyObject *err_type, const char* err_msg, ...);

#define SQ(x) (x)*(x)

static void dist_matrix(const double *points, unsigned int n, double *out) {
  /* C core function.
   * Assumes, that out is preallocated.
   * Works on contiguous C arrays - points has length 3*n, and out has length n*n
   */
  unsigned int i, j;
  // We first abuse the last row of out to store the values of p[î]*p[i]:
  double *p_2 = &out[n*(n-1)];
  for(i=0; i<n; i++)
    p_2[i] = points[i*3]*points[i*3] + points[i*3+1]*points[i*3+1] + points[i*3+2]*points[i*3+2];
  // Then we compute the upper triangle of the matrix p[i]^2 + p[j]^2 -2 (p[i]*p[j])_ij
  for(i=0; i<n-1; i++) {
    out[i*n+i] = 0.; // diagonal is 0.
    for(j=i+1; j<n; j++)
      out[i*n + j] = p_2[i] + p_2[j] - 2.*(points[i*3] * points[j*3]
                                           + points[i*3+1] * points[j*3+1]
                                           + points[i*3+2] * points[j*3+2]);
  }
  // Finally, we mirror the matrix and set out[n-1][n-1] = 0.
  for(i=1; i<n; i++)
    for(j=0; j<i; j++)
      out[i*n+j] = out[j*n+i];
  out[n*n-1] = 0.;
}

static PyObject *py_dist_matrix(PyObject *self, PyObject *args, PyObject *keywords) {
  /* Wraps dist_matrix
   * This is the corresponding python function
   */
  unsigned int i, j, k;
  double x;
  PyArrayObject *py_points, *py_out;

  if(PyArg_ParseTupleAndKeywords(args, keywords,
				 "O!O!:dist_matrix",
				 (char*[]){
				   "points", "out", NULL},
				 &PyArray_Type, &py_points,
				 &PyArray_Type, &py_out)
     // Validate arguments
     && check(PyArray_NDIM(py_points) == 2, PyExc_ValueError, "points must be 2-dimensional")
     && check(PyArray_DIMS(py_points)[1] == 3, PyExc_ValueError, "points must have shape (n, 3)")
     && check(PyArray_NDIM(py_out) == 2, PyExc_ValueError, "out must be 2-dimensional")
     && check(PyArray_DIMS(py_points)[0] == PyArray_DIMS(py_out)[0] && PyArray_DIMS(py_points)[0] == PyArray_DIMS(py_out)[1], PyExc_ValueError, "Shape mismatch. points must have shape (n, 3), out must have shape (n, n)")
     ) {
      npy_long n = PyArray_DIMS(py_points)[0];
      dist_matrix((double*)PyArray_DATA(py_points), n, (double*)PyArray_DATA(py_out));
    }
  return (PyObject*)py_out;
}

static _Bool check(_Bool result, PyObject *err_type, const char* err_msg, ...) {
  if(!result) {
    va_list ap;
    va_start(ap, err_msg);
    PyErr_FormatV(err_type, err_msg, ap);
    va_end(ap);
  }
  return result;
}


static PyMethodDef methods[] = {
                                { "dist_matrix", (PyCFunction)py_dist_matrix, METH_VARARGS | METH_KEYWORDS, "dist_matrix" },
                                { NULL, NULL, 0, NULL }
};

static struct PyModuleDef module_def = {
                                        .m_base = PyModuleDef_HEAD_INIT,
                                        .m_name = "euclidean_distance",   /* name of module */
                                        .m_doc = NULL, /* module documentation, may be NULL */
                                        .m_size = -1,       /* size of per-interpreter state of the module,
                                                               or -1 if the module keeps state in global variables. */
                                        .m_methods = methods,
                                        .m_slots = NULL
};

PyMODINIT_FUNC
PyInit_euclidean_distance(void) {
  import_array();
  return PyModule_Create(&module_def);
}
