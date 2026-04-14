#include "PDFIntegrator.hpp"

#include "LHAPDF/LHAPDF.h"
#include "Utils.hpp"

#include <cmath>
#include <vector>

PDFIntegrator::PDFIntegrator(
    const LHAPDF::PDF* pdf_,
    const std::vector<int> quark_ids_,
    const int sleptonA_id_,
    const int sleptonB_id_,
    const double s_sqrt_,
    const double mix_cos_
)
  : pdf(pdf_),
    quark_ids(quark_ids_),
    sleptonA_id(sleptonA_id_),
    sleptonB_id(sleptonB_id_),
    s(s_sqrt_*s_sqrt_),
    mix_cos(mix_cos_)
{}

void PDFIntegrator::set_masses(double mA_, double mB_) {
  mA = mA_;
  if (std::isnan(mB_)) mB = mA_;
  else mB = mB_;
}

// Integrate over PDF for partonic cross section proportional to delta(1-z)
double PDFIntegrator::integrate_delta(
    double log10x_min,
    double log10x_max,
    double dlog10x,
    double w_delta
) {
  int nx = (int) std::floor((log10x_max - log10x_min) / dlog10x) + 1;

  double dsigma_dQ2 = 0.0;
  for (int quark_id : quark_ids) {
    double x_res = 0.0;
    for (int ix=1; ix < nx-1; ++ix) {
      double log10x = log10x_min + ix*dlog10x;
      double x1 = std::pow(10, log10x);
      double x2 = tau / x1;

      // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
      const double tol = 1e-10;
      if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
      if (std::abs(x2 - 1.0) < tol) x2 = 1.0;

      const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
      const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);

      x_res += xfq * xfqbar / tau;
    }
    
    const double xfqtau = pdf->xfxQ2(quark_id, tau, muF2);
    const double xfq1 = pdf->xfxQ2(quark_id, 1, muF2);
    const double xfqbartau = pdf->xfxQ2(-quark_id, tau, muF2);
    const double xfqbar1 = pdf->xfxQ2(-quark_id, 1, muF2);
    double born_xsec = CrossSections::born_xsec(quark_id, sleptonA_id, sleptonB_id, s, Q2, mA, mB, mix_cos);
    
    x_res += 0.5 * (xfqtau*xfqbar1 + xfq1*xfqbartau) / tau;
    x_res *= born_xsec * w_delta;

    dsigma_dQ2 += x_res;
  }

  // Factor 2 to account for changing which particle is (anti-)quark
  dsigma_dQ2 *= 2 * std::log(10) * dlog10x;
  
  return dsigma_dQ2;
}

double PDFIntegrator::total_xsec(
  int nQ2,
  double dlog10x,
  double w_delta
) {
  const double mtot = mA + mB;
  double muF = 0.5*mtot;
  muF2 = muF*muF;
  
  const double Q2_min = mtot*mtot;
  const double Q2_max = s;
  const double dQ2 = std::floor((Q2_max - Q2_min) / (double) nQ2);
  
  double xsec = 0.0;
  for (int iQ2=0; iQ2 < nQ2; ++iQ2) {
    Q2 = Q2_min + iQ2*dQ2;
    tau = Q2/s;
    
    const double log10x_min = std::log10(tau);
    const double log10x_max = 0.0;
    
    xsec += integrate_delta(log10x_min, log10x_max, dlog10x, w_delta);
  }

  xsec *= dQ2;

  return xsec;
}