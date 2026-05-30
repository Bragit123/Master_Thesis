#ifndef CrossSection_HPP
#define CrossSection_HPP

#include "LHAPDF/LHAPDF.h"
#include <cuba.h>

#include <vector>
#include <complex>


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
    double muF2;
    int quark_id;
    
    double get_ZliAB();
    double get_FqliAB(double Q2);
    double born_xsec(double q2);

    // Integrand
    static int integrand_LO_x1_Q(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );
    static int integrand_hadron_x1_Q(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );
    static int integrand_hadron_x1_x2_Q(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );
    static int integrand_slepton_x1_Q(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );
    static int integrand_slepton_x1_x2_Q(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );




    static int integrand_LO_x1(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );

    // Sleptonside integrals (the functions named I)
    double I_virt_real(double z, double Q2);
    double I_emission_1(double Q2);
    double I_emission_2(double Q2);

    // Weights
    double w_LO(double z, double Q2);
    double w_hadron_soft(double z, double Q2);
    double w_hadron_rad(double z, double Q2);
    double w_hadron_plus_1(double z, double Q2);
    double w_hadron_plus_log(double z, double Q2);
    double w_slepton_soft(double z, double Q2);
    double w_slepton_rad(double z, double Q2);
    double w_slepton_plus_1(double z, double Q2);

  public:
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
      double epsrel=1e-3,
      double epsabs=1e-10,
      double maxeval=10'000'000
      // double maxeval=10'000
    );
    double diff_xsec(
      int subset=0, // 0=LO, 1=Hadronside, 2=Sleptonside
      double epsrel=1e-3,
      double epsabs=1e-3,
      // double maxeval=1'000'000
      double maxeval=10'000
    );
};

#endif





// # mass lo nlo hadronside sleptonside
// 100 1.83381
// 200 1.28441
// 300 0.792691
// 400 0.443372
// 500 0.233546
// 600 0.119668
// 700 0.0610111
// 800 0.0313777
// 900 0.0163964
// 1000 0.00873124




// # mass lo nlo hadronside sleptonside
// 100 0.721319
// 200 0.506361
// 300 0.31329
// 400 0.175747
// 500 0.0928871
// 600 0.0477737
// 700 0.0244575
// 800 0.012634
// 900 0.00663299
// 1000 0.00354961
