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

    // Sets slepton masses. If only one mass is provided, set both masses to that value
    void set_masses(double mA_, double mB_=NAN);

    double integrate_delta(
      double log10x_min,
      double log10x_max,
      double dlog10x,
      double w_delta
    );

    double total_xsec(
      int nQ2=10000,
      double dlog10x=0.001,
      double w_delta=1.0
      // Add other w-functions...
    );
};

#endif