#include "Utils.hpp"
#include <cuba.h>
#include "clooptools.h"

#include <string>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <mutex>


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
    return a*a + b*b + c*c - 2.*a*b - 2.*a*c - 2.*b*c;
  }

  double get_Qq(int quark_id) {
    double Qq;
    if (quark_id % 2 == 0) {
      // up-type quark
      Qq = Const::Qu;
    }
    else {
      // down-type quark
      Qq = Const::Qd;
    }
    return Qq;
  }
  double get_ZqL(int quark_id) {
    double ZqL;
    if (quark_id % 2 == 0) {
      // up-type quark
      ZqL = Const::ZuL;
    }
    else {
      // down-type quark
      ZqL = Const::ZdL;
    }
    return ZqL;
  }
  double get_ZqR(int quark_id) {
    double ZqR;
    if (quark_id % 2 == 0) {
      // up-type quark
      ZqR = Const::ZuR;
    }
    else {
      // down-type quark
      ZqR = Const::ZdR;
    }
    return ZqR;
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