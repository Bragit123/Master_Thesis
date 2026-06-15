#ifndef CrossSection_HPP
#define CrossSection_HPP

#include "LHAPDF/LHAPDF.h"
#include <cuba.h>

#include <vector>
#include <complex>

#include <optional>

// Parameters for CrossSection functions that should not vary between Vegas integrations
struct CSParams {
  int sleptonA_id;
  int sleptonB_id;
  double mA;
  double mB;
  double s;
  double Q2_min;
  double Q2_max;
  double muF2;
  const LHAPDF::PDF* pdf;
  double mix_cos = 1.0;
  std::optional<int> quark_id = std::nullopt; // Needed in integrands, but should not be passed to full_xsec
};


namespace CrossSection {
  double get_ZliAB(CSParams* params);
  double get_FqliAB(double q2, CSParams* params);
  double born_xsec(double q2, double Q2, CSParams* params);
  
  double full_xsec(
    CSParams params,
    std::vector<int> quark_ids,
    int subset=0, // 0=LO, 1=Hadronside, 2=Sleptonside
    double epsrel=3e-3,
    double maxeval=1e7,
    double epsabs=1e-20
  );
}

#endif