#include "CrossSection.hpp"

#include "Integrands.hpp"

#include "LHAPDF/LHAPDF.h"
#include "Utils.hpp"

#include <cmath>
#include <vector>
#include "clooptools.h"

struct IntegrandParams {
  double Q2_min;
  double Q2_max;
  double s;
  int quark_id;
  LHAPDF::PDF* pdf;
};

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
  const double Qq = Utils::get_Qq(quark_id);
  const double ZqL = Utils::get_ZqL(quark_id);
  const double ZqR = Utils::get_ZqR(quark_id);
  
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

double CrossSection::born_xsec(double q2) {
  const double q5 = q2*q2 * std::sqrt(q2);
  const double mA2 = mA*mA;
  const double mB2 = mB*mB;
  const double m2diff = mA2-mB2;

  // squared 3-momentum in slepton RF
  const double mom2 = 0.25*q2 - 0.5*(mA2+mB2) + 0.25*m2diff*m2diff / q2;
  const double mom3 = std::sqrt(mom2) * mom2;
  
  const double FqliAB = get_FqliAB(q2);
  
  const double xsec = Const::BORN_PREFAC * mom3 / (s * q5) * FqliAB;

  return xsec;
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

double CrossSection::full_xsec(
    int subset, // 0=LO, 1=Hadronside, 2=Sleptonside
    double epsrel,
    double maxeval,
    double epsabs
) {
  double m_tot = mA+mB;
  Q2_min = m_tot*m_tot;
  Q2_max = s;
  
  double xsec = 0.0;
  for (int quark_id_ : quark_ids) {
    quark_id = quark_id_;
    // NOTE: Factor 2 to account for interchange of particle--anti-particle
    if (subset == 0) {
      double integral[1], error[1], prob[1];
      Utils::integrate_vegas(2, 1, Integrands::LO_x1_Q, this, epsrel, epsabs,
                            maxeval, integral, error, prob);
      xsec += 2.*integral[0];
    } else if (subset == 1) {
      // // Integral over x1:
      double integral1[1], error1[1], prob1[1];
      Utils::integrate_vegas(2, 1, Integrands::hadron_x1_Q, this, epsrel, epsabs,
                            maxeval, integral1, error1, prob1);
      xsec += 2.*integral1[0];
      
      // Integral over x1 and x2:
      double integral2[1], error2[1], prob2[1];
      Utils::integrate_vegas(3, 1, Integrands::hadron_x1_x2_Q, this, epsrel, epsabs,
                            maxeval, integral2, error2, prob2);
      xsec += 2.*integral2[0];
    } else if (subset == 2) {
      // // Integral over x1:
      double integral1[1], error1[1], prob1[1];
      Utils::integrate_vegas(2, 1, Integrands::slepton_x1_Q, this, epsrel, epsabs,
                            maxeval, integral1, error1, prob1);
      xsec += 2.*integral1[0];
      
      // Integral over x1 and x2:
      double integral2[1], error2[1], prob2[1];
      Utils::integrate_vegas(3, 1, Integrands::slepton_x1_x2_Q, this, epsrel, epsabs,
                            maxeval, integral2, error2, prob2);
      xsec += 2.*integral2[0];
    }
  }
  
  return xsec;
}