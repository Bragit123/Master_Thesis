#ifndef CrossSection_HPP
#define CrossSection_HPP

#include "LHAPDF/LHAPDF.h"
#include <cuba.h>

#include <vector>

enum class Weight {
  LO,
  HADRON_SOFT,
  HADRON_RAD,
  HADRON_PLUS_1,
  HADRON_PLUS_LOG,
  SLEPTON_SOFT,
  SLEPTON_RAD,
  SLEPTON_PLUS_1
};

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

    // Pointer to weight function. Allows changing weight function for integrand
    double (CrossSection::*weight_func)(double);
    
    double get_ZliAB();
    double get_FqliAB(double Q2);
    double born_xsec(double Q2);

    // Integrand
    static int integrand_x1_Q(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );

    // Weights
    double w_LO(double z);
    double w_hadron_soft(double z);
    double w_hadron_rad(double z);
    double w_hadron_plus_1(double z);
    double w_hadron_plus_log(double z);
    double w_slepton_soft(double z);
    double w_slepton_rad(double z);
    double w_slepton_plus_1(double z);

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
    void set_weight(Weight weight);
    
    double full_xsec(
      double epsrel=1e-4,
      double epsabs=1e-12,
      double maxeval=1'000'000
    );
};

#endif