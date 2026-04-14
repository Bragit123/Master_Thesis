#include "Utils.hpp"
#include <string>
#include <iostream>
#include <fstream>

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
}
namespace CrossSections {
  double get_ZliAB(int sleptonA_id, int sleptonB_id, double mix_cos) {
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

  double get_FqliAB(
      int quark_id,
      int sleptonA_id,
      int sleptonB_id,
      double Q2,
      double mix_cos
  ) {
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

    const double ZliAB = get_ZliAB(sleptonA_id, sleptonB_id, mix_cos);
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

  double born_xsec(
      int quark_id,
      int sleptonA_id,
      int sleptonB_id,
      double s,
      double Q2,
      double mA,
      double mB,
      double mix_cos
  ) {
    const double Q5 = Q2*Q2 * std::sqrt(Q2);
    const double mA2 = mA*mA;
    const double mB2 = mB*mB;
    const double m2diff = mA2-mB2;

    // squared 3-momentum in slepton RF
    const double mom2 = 0.25*Q2 - 0.5*(mA2+mB2) + 0.25*m2diff*m2diff / Q2;
    // const double mom3 = std::pow(mom2, 3.0/2.0);
    const double mom3 = std::sqrt(mom2) * mom2;
    
    const double FqliAB = get_FqliAB(quark_id, sleptonA_id, sleptonB_id, Q2, mix_cos);
    
    const double xsec = Const::BORN_PREFAC * mom3 / (s * Q5) * FqliAB;

    return xsec;
  }
}