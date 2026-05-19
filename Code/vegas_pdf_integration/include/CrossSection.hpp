#ifndef CrossSection_HPP
#define CrossSection_HPP

#include "LHAPDF/LHAPDF.h"
#include <cuba.h>

#include <vector>

class CrossSection {
  private:
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
    double Q2;
    double tau;
    double muF2;
    int quark_id;
    
    double get_ZliAB();
    double get_FqliAB(double Q2);
    double born_xsec(double Q2);

    static int LO_integrand(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );
    static int LO_integrand_full(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );

  public:
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

    void set_Q2(double Q2_);

    double diff_xsec(
      double Q2_,
      double epsrel=1e-3,
      double epsabs=1e-12,
      double maxeval=50'000
    );
    
    double full_xsec(
      double epsrel=1e-4,
      double epsabs=1e-12,
      double maxeval=1'000'000
    );
};

#endif