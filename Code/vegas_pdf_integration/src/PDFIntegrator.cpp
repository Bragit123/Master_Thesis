#include "PDFIntegrator.hpp"

#include "LHAPDF/LHAPDF.h"
#include "Utils.hpp"

#include <cmath>
#include <vector>

using w_t = double(*)(double z);

PDFIntegrator::PDFIntegrator(
    const LHAPDF::PDF* pdf_,
    const std::vector<int> quark_ids_,
    const int sleptonA_id_,
    const int sleptonB_id_,
    const double s_,
    const double mix_cos_
)
  : pdf(pdf_),
    quark_ids(quark_ids_),
    sleptonA_id(sleptonA_id_),
    sleptonB_id(sleptonB_id_),
    s(s_),
    mix_cos(mix_cos_)
{}

void PDFIntegrator::set_masses(double mA_, double mB_) {
  mA = mA_;
  if (std::isnan(mB_)) mB = mA_;
  else mB = mB_;
}

double PDFIntegrator::diff_xsec(
    int nQ2,
    w_t w_func
) {
  const double mtot = mA + mB;
  double muF = 0.5*mtot;
  muF2 = muF*muF;

  const double Q2_min = mtot*mtot;
  const double Q2_max = s;
  const double dQ2 = std::floor((Q2_max - Q2_min) / (double) nQ2);

  const int ndim = 1;
  const int ncomp = 1;

  Utils::integrate_vegas(ndim, ncomp, delta_integrand);
}

double PDFIntegrator::total_xsec() {
  const double mtot = mA + mB;
  double muF = 0.5*mtot;
  muF2 = muF*muF;
  
  const double Q2_min = mtot*mtot;
  const double Q2_max = s;
  const double dQ2 = std::floor((Q2_max - Q2_min) / (double) nQ2);
  
  double xsec = 0.0;
  for (int iQ2=0; iQ2 <= nQ2; ++iQ2) {
    Q2 = Q2_min + iQ2*dQ2;
    tau = Q2/s;
    
    const double log10x_min = std::log10(tau);
    const double log10x_max = 0.0;
    
    double dxsec = integrate_delta(log10x_min, log10x_max, dlog10x, w_delta);
    if (iQ2 == 0 || iQ2 == nQ2)
      dxsec *= 0.5; // Half of first and last (trapezoid)

    xsec += dxsec;
  }
  
  xsec *= dQ2;

  return xsec;
}




integrand_t delta_integrand(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian = x1_end - x1_start;
  double x1 = x1_start + jacobian * xx[0];
  double x2 = tau / x1;
  const double z = 1.0;
  w_t w_soft = static_cast<w_t>(userdata);
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;

  double xf_prefac = w_soft(z) / (x1 * tau);

  ff[0] = 0.0;
  for (int quark_id : quark_ids) {
    const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
    const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);

    ff[0] += xf_prefac * xfq * xfqbar;
  }

  ff[0] *= jacobian;

  return 0;
}