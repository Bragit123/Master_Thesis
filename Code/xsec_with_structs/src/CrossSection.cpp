#include "CrossSection.hpp"

#include "Integrands.hpp"

#include "LHAPDF/LHAPDF.h"
#include "Utils.hpp"

#include <cmath>
#include <vector>
#include "clooptools.h"


namespace CrossSection {
  double get_ZliAB(CSParams* params) {
    const int sleptonA_id = params->sleptonA_id;
    const int sleptonB_id = params->sleptonB_id;
    const double mix_cos = params->mix_cos;
    
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

  double get_FqliAB(double q2, CSParams* params) {
    const int quark_id = params->quark_id.value();
    const int sleptonA_id = params->sleptonA_id;
    const int sleptonB_id = params->sleptonB_id;
    
    const double Qq = Utils::get_Qq(quark_id);
    const double ZqL = Utils::get_ZqL(quark_id);
    const double ZqR = Utils::get_ZqR(quark_id);
    
    double deltaAB;
    if (sleptonA_id == sleptonB_id) {
      deltaAB = 1.0;
    } else {
      deltaAB = 0.0;
    }

    const double ZliAB = get_ZliAB(params);
    const double cwsw2inv = 1.0 / (Const::SW2 * Const::CW2);
    const double q2MZ2 = q2 - Const::MZ2;
    const double propagator2inv = 1.0 / (q2MZ2*q2MZ2 + Const::MZ2 * Const::GAMMAZ2);
    const double term1 = Qq*Qq * deltaAB;
    const double term2 = -2.0*Qq*deltaAB * ZliAB*cwsw2inv 
                          * (ZqL+ZqR) * q2*q2MZ2*propagator2inv;
    const double term3 = 2.0 * ZliAB*ZliAB*cwsw2inv*cwsw2inv
                          * (ZqL*ZqL + ZqR*ZqR) * q2*q2*propagator2inv;
    
    return term1 + term2 + term3;
  }

  double born_xsec(double q2, CSParams* params) {
    const double mA = params->mA;
    const double mB = params->mB;
    const double s = params->s;

    const double q5 = q2*q2 * std::sqrt(q2);
    const double mA2 = mA*mA;
    const double mB2 = mB*mB;
    const double m2diff = mA2-mB2;

    // squared 3-momentum in slepton RF
    const double mom2 = 0.25*q2 - 0.5*(mA2+mB2) + 0.25*m2diff*m2diff / q2;
    const double mom3 = std::sqrt(mom2) * mom2;
    
    const double FqliAB = get_FqliAB(q2, params);
    
    const double xsec = Const::BORN_PREFAC * mom3 / (s * q5) * FqliAB;

    return xsec;
  }

  double full_xsec(
      CSParams params,
      std::vector<int> quark_ids,
      int subset, // 0=LO, 1=Hadronside, 2=Sleptonside
      double epsrel,
      double maxeval,
      double epsabs
  ) {
    // const double mA = params.mA;
    // const double mB = params.mB;
    // const double s = params.s;

    // const double m_tot = mA+mB;
    // const double Q2_min = m_tot*m_tot;
    // const double Q2_max = s;
    
    double xsec = 0.0;
    for (int quark_id_ : quark_ids) {
      CSParams params_q = params;
      params_q.quark_id = quark_id_;
      
      // NOTE: Factor 2 to account for interchange of particle--anti-particle
      if (subset == 0) {
        double integral[1], error[1], prob[1];
        Utils::integrate_vegas(2, 1, Integrands::LO_x1_Q, &params_q, epsrel, epsabs,
                              maxeval, integral, error, prob);
        xsec += 2.*integral[0];
      } else if (subset == 1) {
        // // Integral over x1:
        double integral1[1], error1[1], prob1[1];
        Utils::integrate_vegas(2, 1, Integrands::hadron_x1_Q, &params_q, epsrel, epsabs,
                              maxeval, integral1, error1, prob1);
        xsec += 2.*integral1[0];
        
        // Integral over x1 and x2:
        double integral2[1], error2[1], prob2[1];
        Utils::integrate_vegas(3, 1, Integrands::hadron_x1_x2_Q, &params_q, epsrel, epsabs,
                              maxeval, integral2, error2, prob2);
        xsec += 2.*integral2[0];
      } else if (subset == 2) {
        // // Integral over x1:
        double integral1[1], error1[1], prob1[1];
        Utils::integrate_vegas(2, 1, Integrands::slepton_x1_Q, &params_q, epsrel, epsabs,
                              maxeval, integral1, error1, prob1);
        xsec += 2.*integral1[0];
        
        // Integral over x1 and x2:
        double integral2[1], error2[1], prob2[1];
        Utils::integrate_vegas(3, 1, Integrands::slepton_x1_x2_Q, &params_q, epsrel, epsabs,
                              maxeval, integral2, error2, prob2);
        xsec += 2.*integral2[0];
      }
    }
    
    return xsec;
  }
}