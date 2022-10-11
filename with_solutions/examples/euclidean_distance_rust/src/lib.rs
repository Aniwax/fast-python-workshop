#![allow(non_snake_case)]

use numpy::{PyArray2, PyReadonlyArray2};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

#[pymodule]
fn euclidean_distance(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m, "dist_matrix")]
    fn dist_matrix<'a>(
        _py: Python,
        points: PyReadonlyArray2<f64>,
        out: &'a PyArray2<f64>,
    ) -> PyResult<&'a PyArray2<f64>> {
        let (n, m) = (points.dims()[0], points.dims()[1]);
        if m != 3 {
            Err(PyValueError::new_err("Only 3d allowed"))?;
        }
        let p = points.as_slice()?;
        let o = out.as_cell_slice()?;
        let l = n * (n - 1);
        // We first abuse the last row of out to store the values of p[î]*p[i]:
        for i in 0..n {
            o[l + i].set(
                p[i * 3] * p[i * 3] + p[i * 3 + 1] * p[i * 3 + 1] + p[i * 3 + 2] * p[i * 3 + 2],
            );
        }
        // Then we compute the upper triangle of the matrix p[i]^2 + p[j]^2 -2 (p[i]*p[j])_ij
        for i in 0..n - 1 {
            o[i * n + i].set(0.); // diagonal is 0.
            for j in i + 1..n {
                o[i * n + j].set(
                    o[l + i].get() + o[l + j].get()
                        - 2. * (p[i * 3] * p[j * 3]
                            + p[i * 3 + 1] * p[j * 3 + 1]
                            + p[i * 3 + 2] * p[j * 3 + 2]),
                );
            }
        }
        // Finally, we mirror the matrix and set out[n-1][n-1] = 0.
        for i in 1..n {
            for j in 0..i {
                o[i * n + j].set(o[j * n + i].get());
            }
        }
        o[n * n - 1].set(0.);
        Ok(out)
    }
    Ok(())
}
