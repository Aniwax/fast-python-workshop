#include <random>
#include <pybind11/pybind11.h>

double approx_pi(unsigned int n_attempts) {
  std::random_device generator;
  std::uniform_real_distribution<double> distribution(-1.0,1.0);
  
  unsigned int n_hits = 0;
  double x, y;
  for(unsigned int i=0; i<n_attempts; i++) {
    x = distribution(generator);
    y = distribution(generator);
    if(x*x + y*y <= 1.0) n_hits ++;
  }
  return 4. * n_hits / n_attempts;
}

PYBIND11_MODULE(pi, m) {
    m.doc() = "Pi"; // optional module docstring

    m.def("approx_pi", &approx_pi, "Approximates pi");
}
