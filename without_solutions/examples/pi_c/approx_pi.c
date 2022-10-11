#include <stdlib.h>

#include "approx_pi.h"

double approx_pi(unsigned int n_attempts) {
  /* C core function   */
  unsigned int n_hits = 0, i;
  double x, y;
  for(i=0; i<n_attempts; i++) {
    x = 2.*rand()/RAND_MAX -1.;
    y = 2.*rand()/RAND_MAX -1.;
    if(x*x + y*y <= 1.0) n_hits ++;
  }
  return 4. * n_hits / n_attempts;
}
