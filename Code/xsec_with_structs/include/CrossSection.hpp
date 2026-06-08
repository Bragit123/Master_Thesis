#ifndef CrossSection_HPP
#define CrossSection_HPP

#include "LHAPDF/LHAPDF.h"
#include <cuba.h>

#include <vector>
#include <complex>


class CrossSection {
  public:
    const LHAPDF::PDF* pdf;
    const std::vector<int> quark_ids;
    const int sleptonA_id;
    const int sleptonB_id;
    const double s;
    const double mix_cos;
    double mA;
    double mB;
    double Q2_min;
    double Q2_max;
    double muF2;
    int quark_id;
    
    double get_ZliAB();
    double get_FqliAB(double Q2);
    double born_xsec(double q2);

  // public:
    double Q2;
    // Constructor
    CrossSection(
      const LHAPDF::PDF* pdf_,
      const std::vector<int> quark_ids_,
      const int sleptonA_id_,
      const int sleptonB_id_,
      const double s_,
      const double mix_cos_=1.0
    );

    void set_masses(double mA_, double mB_=NAN);
    // void set_Q2(double Q2_);
    
    double full_xsec(
      int subset=0, // 0=LO, 1=Hadronside, 2=Sleptonside
      double epsrel=3e-3,
      double maxeval=1e7,
      double epsabs=1e-20
    );
};

#endif