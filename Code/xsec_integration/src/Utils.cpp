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
  // double get_ZqL(int quark_id) {
  //   double ZqL;
  //   if (quark_id % 2 == 0) {
  //     // up-type quark
  //     ZqL = Const::ZuL;
  //   }
  //   else {
  //     // down-type quark
  //     ZqL = Const::ZdL;
  //   }
  //   return ZqL;
  // }
  // double get_ZqR(int quark_id) {
  //   double ZqR;
  //   if (quark_id % 2 == 0) {
  //     // up-type quark
  //     ZqR = Const::ZuR;
  //   }
  //   else {
  //     // down-type quark
  //     ZqR = Const::ZdR;
  //   }
  //   return ZqR;
  // }
  std::complex<double> get_ZqL(int quark_id) {
    std::complex<double> ZqL;
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
  std::complex<double> get_ZqR(int quark_id) {
    std::complex<double> ZqR;
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
    const int flags = 0;
    const int seed = 0;
    const int mineval = 0;
    const int nstart = 10'000;
    const int nincrease = 1'000;
    const int nbatch = 1'000;
    const int gridno = 0;
    // Vegas(ndim, ncomp, integrand, userdata, 1,
    // epsrel, epsabs, 0, 0,
    // 0, maxeval, 10'000, 1'000, 1'000,
    // 0, nullptr, nullptr,
    // &neval, &fail, integral, error, prob);
    Vegas(ndim, ncomp, integrand, userdata, 1,
    epsrel, epsabs, flags, seed,
    mineval, maxeval, nstart, nincrease, nbatch,
    gridno, nullptr, nullptr,
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

  // void integrate_vegas(
  //     int ndim,
  //     int ncomp,
  //     integrand_t integrand,
  //     void* userdata,
  //     double epsrel,
  //     double epsabs,
  //     int maxeval,
  //     double* integral,
  //     double* error,
  //     double* prob
  // ) {
  //   int nregions, neval, fail;

  //   const int nvec     = 1;      // one point at a time
  //   const int flags    = 0;      // basic settings
  //   const int seed     = 0;      // deterministic; set nonzero for randomness
  //   const int mineval  = 0;

  //   // Sampling / subdivision strategy:
  //   const int key1     = 47;     // points per region (CUBA default-ish)
  //   const int key2     = 1;      // partition strategy
  //   const int key3     = 1;      // refinement strategy
  //   const int maxpass  = 3;      // maximum refinement passes

  //   // Region border and chi^2 / deviation limits:
  //   const double border       = 0.0;  // no special border region
  //   const double maxchisq     = 0.0;  // use default
  //   const double mindeviation = 0.0;  // use default

  //   // No given points and no additional peakfinder:
  //   const int ngiven    = 0;
  //   const int ldxgiven  = 0;
  //   cubareal* xgiven    = nullptr;
  //   const int nextra    = 0;
  //   peakfinder_t peakfinder = nullptr;

  //   const char* statefile = nullptr;
  //   void* spin            = nullptr;

  //   Divonne(ndim, ncomp, integrand, userdata, nvec,
  //           epsrel, epsabs, flags, seed,
  //           mineval, maxeval,
  //           key1, key2, key3, maxpass,
  //           border, maxchisq, mindeviation,
  //           ngiven, ldxgiven, xgiven,
  //           nextra, peakfinder,
  //           statefile, spin,
  //           &nregions, &neval, &fail,
  //           integral, error, prob);

  //   if (fail != 0) {
  //     printf("Divonne integration failed (fail=%d):\n", fail);
  //     printf("\tndim=%d\n\tncomp=%d\n\tepsrel=%g\n\tepsabs=%g\n\tmaxeval=%d\n",
  //            ndim, ncomp, epsrel, epsabs, maxeval);
  //     for (int icomp=0; icomp < ncomp; ++icomp) {
  //       printf("\tcomp=%d\tintegral=%g\terror=%g\tprob=%g\n",
  //              icomp, integral[icomp], error[icomp], prob[icomp]);
  //     }
  //   }
  // }

  void integrate_cuhre(
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
    int nregions = 0;
    int neval    = 0;
    int fail     = 0;

    const int nvec    = 1;   // scalar integrand
    const int flags   = 0;   // basic settings
    const int mineval = 0;   // no minimum
    const int key     = 11;  // default cubature rule (good starting point)

    const char* statefile = nullptr;
    void* spin = nullptr;

    Cuhre(ndim, ncomp, integrand, userdata, nvec,
          epsrel, epsabs, flags, mineval, maxeval,
          key, statefile, spin,
          &nregions, &neval, &fail,
          integral, error, prob);

    // Optional logging:
    if (fail != 0) {
      printf("Cuhre integration failed (fail=%d):\n", fail);
      printf("\tndim=%d\n\tncomp=%d\n\tepsrel=%g\n\tepsabs=%g\n\tmaxeval=%d\n",
             ndim, ncomp, epsrel, epsabs, maxeval);
      for (int icomp=0; icomp < ncomp; ++icomp) {
        printf("\tcomp=%d\tintegral=%g\terror=%g\tprob=%g\n",
               icomp, integral[icomp], error[icomp], prob[icomp]);
      }
    }
  }
}