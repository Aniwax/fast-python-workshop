use pyo3::prelude::{pymodule, PyModule, PyResult, Python};
use rand;

#[pymodule]
fn pi(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m, "approx_pi")]
    fn approx_pi<'a>(_py: Python, n_attempts: u32) -> PyResult<f64> {
        let mut n_hits: u32 = 0;
        for _ in 0..n_attempts {
            let x = 2. * rand::random::<f64>() - 1.;
            let y = 2. * rand::random::<f64>() - 1.;
            if x * x + y * y <= 1.0 {
                n_hits += 1;
            }
        }
        Ok(4. * n_hits as f64 / n_attempts as f64)
    }
    Ok(())
}
