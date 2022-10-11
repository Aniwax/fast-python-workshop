#!/usr/bin/env python3

from ctypes import cdll, c_double

approx_pi = cdll.LoadLibrary("./approx_pi.so").approx_pi
approx_pi.restype = c_double  # By default ctypes assumes int as a return type

if __name__ == "__main__":
    π = approx_pi(2_000_000)
    print(π, type(π))
