#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <array>
#include "clooptools.h"

#include "Utils.hpp"
#include "CrossSection.hpp"

/////////////////////
/// Cross Section ///
/////////////////////
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
//       const double mass_tot = slepton_mass + slepton_mass;
//       const double Q2_min = mass_tot * mass_tot;
//       const double Q2_max = s;
//       const double muF = 0.5 * mass_tot;
//       const double muF2 = muF * muF;
//       setmudim(muF2);

//       const CSParams params {
//         .sleptonA_id = slepton_id,
//         .sleptonB_id = slepton_id,
//         .mA = slepton_mass,
//         .mB = slepton_mass,
//         .s = s,
//         .Q2_min = Q2_min,
//         .Q2_max = Q2_max,
//         .muF2 = muF2,
//         .pdf = pdf,
//         .mix_cos = 1.0
//       };
      
//       const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0);
//       const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1);
//       const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2);
//       const double xsec_nlo = xsec_hadron + xsec_slepton;
      
//       outfile << slepton_mass << " " << xsec_lo << " " << xsec_lo + xsec_nlo
//               << " " << xsec_lo + xsec_hadron << " " << xsec_lo + xsec_slepton << "\n";
//     }
//     outfile.close();
//   }
  
//   delete pdf;

//   ltexi(); // Print errors and warnings from LoopTools
  
//   return 0;
// }

//////////////////
/// PDF ERRORS ///
//////////////////
// int main(int argc, char* argv[]) {
//   ltini(); // Initialize LoopTools
//   setlambda(0.0);

//   LHAPDF::setVerbosity(0);
//   const std::string setname = "PDF4LHC21_40";
//   const int n_mem = 43;
  
//   const LHAPDF::PDF* pdf_0 = LHAPDF::mkPDF(setname, 0);
  
//   std::array<LHAPDF::PDF*, n_mem-1> err_pdfs;
//   for (int mem=1; mem < n_mem; ++mem) {
//     err_pdfs.at(mem-1) = LHAPDF::mkPDF(setname, mem);
//   }

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
    
//     std::string filename = "output/xsec_mass_err_" + std::to_string(slepton_id) + ".dat";
//     std::ofstream outfile(filename);
//     outfile << "# mass(GeV) | lo(fb) | +-PDFerr | nlo(fb) | +-PDFerr" << std::endl;
    
//     for (int im=0; im < nm; ++im) {
//       std::cout << "Mass: " << im+1 << "/" << nm << std::endl;
      
//       const double slepton_mass = m_min + im*dm;
//       const double mass_tot = slepton_mass + slepton_mass;
//       const double Q2_min = mass_tot * mass_tot;
//       const double Q2_max = s;
//       const double muF = 0.5 * mass_tot;
//       const double muF2 = muF * muF;
//       setmudim(muF2);
//       const CSParams params {
//         .sleptonA_id = slepton_id,
//         .sleptonB_id = slepton_id,
//         .mA = slepton_mass,
//         .mB = slepton_mass,
//         .s = s,
//         .Q2_min = Q2_min,
//         .Q2_max = Q2_max,
//         .muF2 = muF2,
//         .pdf = pdf_0,
//         .mix_cos = 1.0
//       };
      
//       const double epsrel = 1e-1;
//       const double maxeval = 1e8;
//       const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
//       const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
//       const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
//       const double xsec_nlo = xsec_lo + xsec_hadron + xsec_slepton;

//       double pdf_variance_lo = 0.0;
//       double pdf_variance_nlo = 0.0;
//       for (int i=0; i<n_mem-1; ++i) {
//         Utils::print_progress(i+1, n_mem-1);
//         const LHAPDF::PDF* pdf_i = err_pdfs.at(i);
//         CSParams params_i = params;
//         params_i.pdf = pdf_i;

//         const double xsec_lo_i = CrossSection::full_xsec(params_i, quark_ids, 0, epsrel, maxeval);
//         const double xsec_diff_lo = xsec_lo_i - xsec_lo;
//         pdf_variance_lo += xsec_diff_lo * xsec_diff_lo;

//         const double xsec_hadron_i = CrossSection::full_xsec(params_i, quark_ids, 1, epsrel, maxeval);
//         const double xsec_slepton_i = CrossSection::full_xsec(params_i, quark_ids, 2, epsrel, maxeval);
//         const double xsec_nlo_i = xsec_lo_i + xsec_hadron_i + xsec_slepton_i;
//         const double xsec_diff_nlo = xsec_nlo_i - xsec_nlo;
//         pdf_variance_nlo += xsec_diff_nlo * xsec_diff_nlo;
//       }

//       const double pdf_std_lo = sqrt(pdf_variance_lo);
//       const double pdf_std_nlo = sqrt(pdf_variance_nlo);

//       outfile << slepton_mass << " " << xsec_lo << " " << pdf_std_lo << " "
//               << xsec_nlo << " " << pdf_std_nlo << std::endl;
//     }
//     outfile.close();
//   }
  
//   delete pdf_0;
//   for (LHAPDF::PDF* pdf : err_pdfs) {
//     delete pdf;
//   }

//   ltexi(); // Print errors and warnings from LoopTools
  
//   return 0;
// }

///////////////////
/// Scale Error ///
///////////////////
// int main(int argc, char* argv[]) {
//   ltini(); // Initialize LoopTools
//   setlambda(0.0);

//   LHAPDF::setVerbosity(0);
//   const std::string setname = "PDF4LHC21_40";
  
//   const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, 0);

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
    
//     std::string filename = "output/xsec_mass_scale_err_" + std::to_string(slepton_id) + ".dat";
//     std::ofstream outfile(filename);
//     outfile << "# mass(GeV) | lo(fb) | +-scale_err | nlo(fb) | +-scale_err" << std::endl;
    
//     for (int im=0; im < nm; ++im) {
//       Utils::print_progress(im+1, nm);
      
//       const double slepton_mass = m_min + im*dm;
//       const double mass_tot = slepton_mass + slepton_mass;
//       const double Q2_min = mass_tot * mass_tot;
//       const double Q2_max = s;
//       const double muF_0 = 0.5 * mass_tot;
//       const double muF_min = muF_0/2.;
//       const double muF_max = 2.*muF_0;
//       const std::vector<double> muF2s = {
//         muF_min * muF_min,
//         muF_0 * muF_0,
//         muF_max * muF_max
//       };

//       const CSParams params_0 {
//         .sleptonA_id = slepton_id,
//         .sleptonB_id = slepton_id,
//         .mA = slepton_mass,
//         .mB = slepton_mass,
//         .s = s,
//         .Q2_min = Q2_min,
//         .Q2_max = Q2_max,
//         .muF2 = muF_0*muF_0,
//         .pdf = pdf,
//         .mix_cos = 1.0
//       };
      
//       const double epsrel = 1e-2;
//       const double maxeval = 1e9;
//       std::array<double, 3> xsec_los;
//       std::array<double, 3> xsec_nlos;
//       for (int i=0; i<3; ++i) {
//         const double muF2 = muF2s.at(i);
//         setmudim(muF2);

//         CSParams params = params_0;
//         params.muF2 = muF2;

//         xsec_los.at(i) = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
//         const double xsec_hadrons_i = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
//         const double xsec_sleptons_i = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
//         xsec_nlos.at(i) = xsec_los.at(i) + xsec_hadrons_i + xsec_sleptons_i;
//       }
//       const double xsec_lo = xsec_los.at(1);
//       const double xsec_nlo = xsec_nlos.at(1);

//       const double mu_err_lo = std::abs(xsec_los.at(2) - xsec_los.at(0));
//       const double mu_err_nlo = std::abs(xsec_nlos.at(2) - xsec_nlos.at(0));
      
//       outfile << slepton_mass << " " << xsec_lo << " " << mu_err_lo << " "
//               << xsec_nlo << " " << mu_err_nlo << std::endl;
//     }
//     outfile.close();
//   }
  
//   delete pdf;

//   ltexi(); // Print errors and warnings from LoopTools
  
//   return 0;
// }

/////////////////////
/// xsec vs scale ///
/////////////////////
int main(int argc, char* argv[]) {
  ltini(); // Initialize LoopTools
  setlambda(0.0);

  LHAPDF::setVerbosity(0);
  const std::string setname = "PDF4LHC21_40";
  
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, 0);

  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double slepton_mass = 700;
  const double mass_tot = slepton_mass + slepton_mass;
  const double Q2_min = mass_tot * mass_tot;
  const double Q2_max = s;

  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/xsec_scale_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# SLEPTON_MASS = " << slepton_mass << std::endl;
    outfile << "# mu/mass | lo(fb) | nlo(fb) | hadronside(fb)"
            << "| sleptonside(fb)" << std::endl;
        
    const double muF_0 = 0.5 * mass_tot;
    const double muF2_0 = muF_0 * muF_0;

    const double muF_mass_log2_min = -2.;
    const double muF_mass_log2_max = 2.;
    const int n_muF_mass_log2 = 5;
    const double dmuF_mass = (muF_mass_log2_max - muF_mass_log2_min) / (double) (n_muF_mass_log2 - 1);
    
    const double epsrel = 1e-3;
    const double maxeval = 1e9;

    const CSParams params_0 {
        .sleptonA_id = slepton_id,
        .sleptonB_id = slepton_id,
        .mA = slepton_mass,
        .mB = slepton_mass,
        .s = s,
        .Q2_min = Q2_min,
        .Q2_max = Q2_max,
        .muF2 = muF2_0,
        .pdf = pdf,
        .mix_cos = 1.0
      };
    
    for (int imuF=0; imuF<n_muF_mass_log2; ++imuF) {
      Utils::print_progress(imuF+1, n_muF_mass_log2);
      const double muF_mass_log2 = muF_mass_log2_min + (double) imuF * dmuF_mass;
      const double muF_mass = pow(2., muF_mass_log2);
      const double muF = muF_mass * slepton_mass;
      const double muF2 = muF * muF;
      setmudim(muF2);

      CSParams params = params_0;
      params.muF2 = muF2;

      const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
      const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
      const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
      const double xsec_nlo = xsec_lo + xsec_hadron + xsec_slepton;

      outfile << muF_mass << " " << xsec_lo << " " << xsec_nlo << " "
              << xsec_lo+xsec_hadron << " " << xsec_lo+xsec_slepton << std::endl;
    }

    outfile.close();
  }
  
  
  delete pdf;

  ltexi(); // Print errors and warnings from LoopTools
  
  return 0;
}