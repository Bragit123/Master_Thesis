#ifndef PDFIntegrator_HPP
#define PDFIntegrator_HPP

#include "LHAPDF/LHAPDF.h"

class PDFIntegrator {
  private:
    const LHAPDF::PDF* pdf;
    const std::vector<int> quark_ids;
    const int sleptonA_id;
    const int sleptonB_id;
    const double s;
    const double mix_cos;
    double mA;
    double mB;
    double Q2;
    double tau;
    double muF2;
  
  public:
    // Constructor
    PDFIntegrator(
      const LHAPDF::PDF* pdf_,
      const std::vector<int> quark_ids_,
      const int sleptonA_id_,
      const int sleptonB_id_,
      const double s_,
      const double mix_cos_=1.0
    );

    // Sets slepton masses. If only one mass is provided, set both masses to
    // that value
    void set_masses(double mA_, double mB_=NAN);


    // Integrate over PDFs for partonic cross section proportional to delta(1-z)
    integrand_t delta_integrand(
      const int* ndim,
      const cubareal xx[],
      const int* ncomp,
      cubareal ff[],
      void* userdata
    );

    double diff_xsec(int nQ2, w_t w_func);

    // Finds full (hadronic) cross section
    double total_xsec();
};

#endif