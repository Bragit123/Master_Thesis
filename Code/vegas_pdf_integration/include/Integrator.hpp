#ifndef Integrator_HPP
#define Integrator_HPP

#include "LHAPDF/LHAPDF.h"
#include <cuba.h>
#include <vector>
#include <complex>

namespace Integrands {
  int LO_x1_Q(
      const int* ndim, const cubareal xx[], const int* ncomp,
      cubareal ff[], void* userdata
  );
  int hadron_x1_Q(
    const int* ndim, const cubareal xx[], const int* ncomp,
    cubareal ff[], void* userdata
  );
  int hadron_x1_x2_Q(
    const int* ndim, const cubareal xx[], const int* ncomp,
    cubareal ff[], void* userdata
  );
  int slepton_x1_Q(
    const int* ndim, const cubareal xx[], const int* ncomp,
    cubareal ff[], void* userdata
  );
  int slepton_x1_x2_Q(
    const int* ndim, const cubareal xx[], const int* ncomp,
    cubareal ff[], void* userdata
  );
}




#endif