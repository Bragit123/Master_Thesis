#ifndef UTILS_HPP
#define UTILS_HPP

#include <cmath>

// Values are taken from PDG
namespace Const {
  // Electroweak theory (Gmu scheme)
  const double MW = 80.369;
  const double MW2 = MW*MW;
  const double MZ = 91.188;
  const double MZ2 = MZ*MZ;
  const double GAMMAZ = 2.4955; // Z decay rate
  const double GAMMAZ2 = GAMMAZ*GAMMAZ;
  const double CW2 = MW2 / MZ2; // cos(thetaW)^2
  const double SW2 = 1.0 - CW2; // sin(thetaW)^2
  const double GF = 1.16638e-5; // Fermi constant
  const double ALPHA = std::sqrt(2.0) * GF * MW2 * SW2 / M_PI;
  
  // Quarks
  const double NC = 3.0;
  const double Qu = 2.0/3.0;
  const double Qd = -1.0/3.0;
  const double ZuL = -0.25 * (1.0 - 2.0 * Qu * SW2);
  const double ZuR = 0.5 * Qu * SW2;
  const double ZdL = 0.25 * (1.0 + 2.0 * Qd * SW2);
  const double ZdR = 0.5 * Qd * SW2;

  const double BORN_PREFAC = 8.0 * M_PI * ALPHA*ALPHA / (3.0 * NC);
}

namespace Utils {
  int first_digit(int x);
}

namespace CrossSections {
  double get_FqliAB(
    int quark_id,
    int sleptonA_id,
    int sleptonB_id,
    double Q2,
    double mix_cos = 1.0
  );

  double born_xsec(
    int quark_id,
    int sleptonA_id,
    int sleptonB_id,
    double s,
    double Q,
    double mA,
    double mB,
    double mix_cos = 1.0
  );
}

#endif