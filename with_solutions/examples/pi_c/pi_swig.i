%module pi_swig

%{
#define SWIG_FILE_WITH_INIT
#include "approx_pi.h"
%}

double approx_pi(unsigned int n_attempts);
