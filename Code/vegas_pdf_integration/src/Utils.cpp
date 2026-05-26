#include "Utils.hpp"
#include <cuba.h>
#include "clooptools.h"

#include <string>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <mutex>

static std::mutex li2_mutex;

namespace Utils {
  int first_digit(int x) {
    while (x >= 10) {
      x /= 10;
    }
    return x;
  }

  void print_progress(int current, int max) {
    std::cout << "\r  " << std::setw(3) << std::floor(100*current/max)
              << "%" << std::flush;
    if (current == max) std::cout << "\n";
  }

  double Kallen(double a, double b, double c) {
    return a*a + b*b + c*c - 2.0*a*b - 2.0*a*c - 2.0*b*c;
  }

  std::complex<double> safe_Li2(double arg) {
    // Cuba uses multiple threads for integration, which messes up LoopTools' Li2
    // function. safe_Li2 "locks" the function, circumventing the problem
    std::lock_guard<std::mutex> lock(li2_mutex);
    return Li2(arg);
  }

  void integrate_vegas(
      int ndim,
      int ncomp,
      integrand_t integrand,
      void* userdata,
      double epsrel,
      double epsabs,
      int maxeval,
      double* integral,
      double* error,
      double* prob
  ) {
    int neval, fail;
    Vegas(ndim, ncomp, integrand, userdata, 1,
    epsrel, epsabs, 0, 0,
    0, maxeval, 10'000, 1'000, 1'000,
    0, nullptr, nullptr,
    &neval, &fail, integral, error, prob);
    
    if (fail != 0) {
      printf("Vegas integration failed (fail=%d):\n", fail);
      printf("\tndim=%d\n\tncomp=%d\n\tepsrel=%g\n\tepsabs=%g\n\tmaxeval=%d\n",
        ndim, ncomp, epsrel, epsabs, maxeval);
      for (int icomp=0; icomp < ncomp; ++icomp) {
        printf("\tcomp=%d\tintegral=%g\terror=%g\tprob=%g\n",
          icomp, integral[icomp], error[icomp], prob[icomp]);
      }
    }
  }
}