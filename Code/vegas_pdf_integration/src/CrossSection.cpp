#include "CrossSection.hpp"

#include "LHAPDF/LHAPDF.h"
#include "Utils.hpp"

#include <cmath>
#include <vector>

// Constructor
CrossSection::CrossSection(
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

///////////////////////
// Private functions //
///////////////////////

double CrossSection::get_ZliAB() {
  const int A = Utils::first_digit(sleptonA_id);
  const int B = Utils::first_digit(sleptonB_id);

  if (A == B && A == 1) {
    return 0.5 * mix_cos*mix_cos - Const::SW2;
  } else if (A == B && A == 2) {
    return 0.5 * (1.0 - mix_cos*mix_cos) - Const::SW2;
  } else {
    return 0.5 * mix_cos * std::sqrt(1.0 - mix_cos*mix_cos);
  }
}

double CrossSection::get_FqliAB(double Q2) {
  double Qq;
  double ZqL;
  double ZqR;
  if (quark_id % 2 == 0) {
    // up-type quark
    Qq = Const::Qu;
    ZqL = Const::ZuL;
    ZqR = Const::ZuR;
  } else {
    // down-type quark
    Qq = Const::Qd;
    ZqL = Const::ZdL;
    ZqR = Const::ZdR;
  }
  
  double deltaAB;
  if (sleptonA_id == sleptonB_id) {
    deltaAB = 1.0;
  } else {
    deltaAB = 0.0;
  }

  const double ZliAB = get_ZliAB();
  const double cwsw2inv = 1.0 / (Const::SW2 * Const::CW2);
  const double Q2MZ2 = Q2 - Const::MZ2;
  const double propagator2inv = 1.0 / (Q2MZ2*Q2MZ2 + Const::MZ2 * Const::GAMMAZ2);
  const double term1 = Qq*Qq * deltaAB;
  const double term2 = -2.0*Qq*deltaAB * ZliAB*cwsw2inv 
                        * (ZqL+ZqR) * Q2*Q2MZ2*propagator2inv;
  const double term3 = 2.0 * ZliAB*ZliAB*cwsw2inv*cwsw2inv
                        * (ZqL*ZqL + ZqR*ZqR) * Q2*Q2*propagator2inv;
  
  return term1 + term2 + term3;
}

double CrossSection::born_xsec(double Q2) {
  const double Q5 = Q2*Q2 * std::sqrt(Q2);
  const double mA2 = mA*mA;
  const double mB2 = mB*mB;
  const double m2diff = mA2-mB2;

  // squared 3-momentum in slepton RF
  const double mom2 = 0.25*Q2 - 0.5*(mA2+mB2) + 0.25*m2diff*m2diff / Q2;
  // const double mom3 = std::pow(mom2, 3.0/2.0);
  const double mom3 = std::sqrt(mom2) * mom2;
  
  const double FqliAB = get_FqliAB(Q2);
  
  const double xsec = Const::BORN_PREFAC * mom3 / (s * Q5) * FqliAB;

  return xsec;
}


////////////////
// Integrands //
////////////////
int CrossSection::LO_integrand_full(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
  double Q2_min = self->Q2_min;
  double Q2_max = self->Q2_max;
  double s = self->s;
  int quark_id = self->quark_id;
  double muF2 = self->muF2;
  const LHAPDF::PDF* pdf = self->pdf;
  
  double jacobian_Q2 = Q2_max - Q2_min;
  double Q2 = Q2_min + jacobian_Q2 * xx[0];
  double tau = Q2/s;
  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian_x1 = x1_end - x1_start;
  double x1 = x1_start + jacobian_x1 * xx[1];
  double x2 = tau / x1;
  
  const double jacobian = jacobian_Q2 * jacobian_x1;
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
  
  const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
  const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);

  const double born = self->born_xsec(Q2);

  // Factor 2 to account for changing which particle is (anti-)quark
  ff[0] = 2.0 * born * jacobian * xfq * xfqbar / (x1 * tau);

  return 0;
}

//////////////////////
// Public functions //
//////////////////////
void CrossSection::set_masses(double mA_, double mB_) {
  mA = mA_;
  if (std::isnan(mB_)) mB = mA_;
  else mB = mB_;
  double muF = 0.5 * (mA + mB);
  muF2 = muF*muF;
}
void CrossSection::set_Q2(double Q2_) {
  Q2 = Q2_;
  tau = Q2/s;
}


double CrossSection::full_xsec(
    double epsrel,
    double epsabs,
    double maxeval
) {
  double m_tot = mA+mB;
  Q2_min = m_tot*m_tot;
  Q2_max = s;
  
  double xsec = 0.0;
  for (int quark_id_ : quark_ids) {
    quark_id = quark_id_;
    double integral[1], error[1], prob[1];
    int neval, fail;
    Utils::integrate_vegas(2, 1, LO_integrand_full, this, epsrel, epsabs,
                          maxeval, integral, error, prob);
    xsec += integral[0];
  }
  
  return xsec;
}