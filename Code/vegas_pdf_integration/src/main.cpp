#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <array>
#include "clooptools.h"

#include "Utils.hpp"
#include "CrossSection.hpp"

// int main(int argc, char* argv[]) {
//   ltini(); // Initialize LoopTools
//   setlambda(0.0);

//   const std::string setname = "PDF4LHC21_40";
//   const int mem = 0; // Only considering central PDF for now. Expanding laterz!

//   LHAPDF::setVerbosity(0);
//   const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, mem);
//   const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

//   const double s_sqrt = 13'000.0; // 13 TeV
//   const double s = s_sqrt*s_sqrt;

//   //Slepton mass
//   const double m_min = 100.;
//   const double m_max = 1000.;
//   const double dm = 100.;
//   const double nm = std::floor((m_max - m_min) / dm) + 1;
  
//   std::vector<int> slepton_ids = {1000011, 2000011};
//   for (int slepton_id : slepton_ids) {
//     std::cout << "Slepton " << slepton_id << ":\n";
    
//     std::string filename = "output/xsec_mass_" + std::to_string(slepton_id) + ".dat";
//     std::ofstream outfile(filename);
//     outfile << "# mass(GeV) lo(fb) nlo(fb) hadronside(fb) sleptonside(fb)" << std::endl;
    
//     for (int im=0; im < nm; ++im) {
//       Utils::print_progress(im+1, nm);
      
//       const double slepton_mass = m_min + im*dm;
      
//       CrossSection integrator = CrossSection(pdf, quark_ids, slepton_id, slepton_id, s);
//       integrator.set_masses(slepton_mass);
//       const double muF2 = slepton_mass*slepton_mass;
//       setmudim(muF2);
      
//       const double xsec_lo = integrator.full_xsec(0);
//       const double xsec_hadron = integrator.full_xsec(1);
//       const double xsec_slepton = integrator.full_xsec(2);
//       const double xsec_nlo = xsec_hadron + xsec_slepton;
      
//       outfile << slepton_mass << " " << xsec_lo << " " << xsec_nlo
//               << " " << xsec_hadron << " " << xsec_slepton << "\n";
//     }
//     outfile.close();
//   }
  
//   delete pdf;

//   ltexi(); // Print errors and warnings from LoopTools
  
//   return 0;
// }

int main(int argc, char* argv[]) {
  ltini(); // Initialize LoopTools
  setlambda(0.0);

  LHAPDF::setVerbosity(0);
  const std::string setname = "PDF4LHC21_40";
  const int n_mem = 43;
  
  const LHAPDF::PDF* pdf_0 = LHAPDF::mkPDF(setname, 0);
  
  std::array<LHAPDF::PDF*, n_mem-1> err_pdfs;
  for (int mem=1; mem < n_mem; ++mem) {
    err_pdfs.at(mem-1) = LHAPDF::mkPDF(setname, mem);
  }
  // const LHAPDF::PDF* pdf_0 = pdfs.at(0);

  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double m_min = 100.;
  const double m_max = 1000.;
  const double dm = 100.;
  const double nm = std::floor((m_max - m_min) / dm) + 1;
  
  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/xsec_mass_err_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# mass(GeV) | lo(fb) | +-PDFerr | nlo(fb) | +-PDFerr | hadronside(fb)"
            << "| +-PDFerr | sleptonside(fb) | +-PDFerr | ratio | +-PDFerr" << std::endl;
    
    for (int im=0; im < nm; ++im) {
      Utils::print_progress(im+1, nm);
      
      const double slepton_mass = m_min + im*dm;
      
      CrossSection integrator = CrossSection(pdf_0, quark_ids, slepton_id, slepton_id, s);
      integrator.set_masses(slepton_mass);
      const double muF2 = slepton_mass*slepton_mass;
      setmudim(muF2);
      
      const double epsrel = 1e-1;
      const double xsec_lo = integrator.full_xsec(0, epsrel);
      const double xsec_hadron = integrator.full_xsec(1, epsrel);
      const double xsec_slepton = integrator.full_xsec(2, epsrel);
      const double xsec_nlo = xsec_hadron + xsec_slepton;
      const double ratio = xsec_nlo/xsec_lo;

      double pdf_variance_lo = 0.0;
      double pdf_variance_hadron = 0.0;
      double pdf_variance_slepton = 0.0;
      double pdf_variance_nlo = 0.0;
      double pdf_variance_ratio = 0.0;
      for (LHAPDF::PDF* pdf_i : err_pdfs) {
        integrator.pdf = pdf_i;

        const double xsec_lo_i = integrator.full_xsec(0, epsrel);
        const double xsec_diff_lo = xsec_lo_i - xsec_lo;
        pdf_variance_lo += xsec_diff_lo * xsec_diff_lo;

        const double xsec_hadron_i = integrator.full_xsec(1, epsrel);
        const double xsec_diff_hadron = xsec_hadron_i - xsec_hadron;
        pdf_variance_hadron += xsec_diff_hadron * xsec_diff_hadron;

        const double xsec_slepton_i = integrator.full_xsec(2, epsrel);
        const double xsec_diff_slepton = xsec_slepton_i - xsec_slepton;
        pdf_variance_slepton += xsec_diff_slepton * xsec_diff_slepton;

        const double xsec_nlo_i = xsec_hadron_i + xsec_slepton_i;
        const double xsec_diff_nlo = xsec_nlo_i - xsec_nlo;
        pdf_variance_nlo += xsec_diff_nlo * xsec_diff_nlo;

        const double ratio_i = xsec_nlo_i / xsec_lo_i;
        const double diff_ratio = ratio_i - ratio;
        pdf_variance_ratio += diff_ratio * diff_ratio;
      }

      const double pdf_std_lo = sqrt(pdf_variance_lo);
      const double pdf_std_hadron = sqrt(pdf_variance_hadron);
      const double pdf_std_slepton = sqrt(pdf_variance_slepton);
      const double pdf_std_nlo = sqrt(pdf_variance_nlo);
      const double pdf_std_ratio = sqrt(pdf_variance_ratio);
      
      outfile << slepton_mass << " " << xsec_lo << " " << pdf_std_lo << " "
              << xsec_nlo << " " << pdf_std_nlo << " "
              << xsec_hadron << " " << pdf_std_hadron << " "
              << xsec_slepton << " " << pdf_std_slepton << " "
              << ratio << " " << pdf_std_ratio << "\n";
    }
    outfile.close();
  }
  
  delete pdf_0;
  for (LHAPDF::PDF* pdf : err_pdfs) {
    delete pdf;
  }

  ltexi(); // Print errors and warnings from LoopTools
  
  return 0;
}