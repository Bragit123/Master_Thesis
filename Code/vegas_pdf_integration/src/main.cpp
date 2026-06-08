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
//   // const LHAPDF::PDF* pdf_0 = pdfs.at(0);

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
//     outfile << "# mass(GeV) | lo(fb) | +-PDFerr | nlo(fb) | +-PDFerr | hadronside(fb)"
//             << "| +-PDFerr | sleptonside(fb) | +-PDFerr | ratio | +-PDFerr" << std::endl;
    
//     for (int im=0; im < nm; ++im) {
//       Utils::print_progress(im+1, nm);
      
//       const double slepton_mass = m_min + im*dm;
      
//       CrossSection integrator = CrossSection(pdf_0, quark_ids, slepton_id, slepton_id, s);
//       integrator.set_masses(slepton_mass);
//       const double muF2 = slepton_mass*slepton_mass;
//       setmudim(muF2);
      
//       const double epsrel = 1e-3;
//       const double maxeval = 1e8;
//       const double xsec_lo = integrator.full_xsec(0, epsrel, maxeval);
//       const double xsec_hadron = integrator.full_xsec(1, epsrel, maxeval);
//       const double xsec_slepton = integrator.full_xsec(2, epsrel, maxeval);
//       const double xsec_nlo = xsec_hadron + xsec_slepton;
//       const double ratio = (xsec_lo + xsec_nlo)/xsec_lo;

//       double pdf_variance_lo = 0.0;
//       double pdf_variance_hadron = 0.0;
//       double pdf_variance_slepton = 0.0;
//       double pdf_variance_nlo = 0.0;
//       double pdf_variance_ratio = 0.0;
//       for (LHAPDF::PDF* pdf_i : err_pdfs) {
//         integrator.pdf = pdf_i;

//         const double xsec_lo_i = integrator.full_xsec(0, epsrel, maxeval);
//         const double xsec_diff_lo = xsec_lo_i - xsec_lo;
//         pdf_variance_lo += xsec_diff_lo * xsec_diff_lo;

//         const double xsec_hadron_i = integrator.full_xsec(1, epsrel, maxeval);
//         const double xsec_diff_hadron = xsec_hadron_i - xsec_hadron;
//         pdf_variance_hadron += xsec_diff_hadron * xsec_diff_hadron;

//         const double xsec_slepton_i = integrator.full_xsec(2, epsrel, maxeval);
//         const double xsec_diff_slepton = xsec_slepton_i - xsec_slepton;
//         pdf_variance_slepton += xsec_diff_slepton * xsec_diff_slepton;

//         const double xsec_nlo_i = xsec_hadron_i + xsec_slepton_i;
//         const double xsec_diff_nlo = xsec_nlo_i - xsec_nlo;
//         pdf_variance_nlo += xsec_diff_nlo * xsec_diff_nlo;

//         const double ratio_i = (xsec_lo_i + xsec_nlo_i) / xsec_lo_i;
//         const double diff_ratio = ratio_i - ratio;
//         pdf_variance_ratio += diff_ratio * diff_ratio;
//       }

//       const double pdf_std_lo = sqrt(pdf_variance_lo);
//       const double pdf_std_hadron = sqrt(pdf_variance_hadron);
//       const double pdf_std_slepton = sqrt(pdf_variance_slepton);
//       const double pdf_std_nlo = sqrt(pdf_variance_nlo);
//       const double pdf_std_ratio = sqrt(pdf_variance_ratio);
      
//       outfile << slepton_mass << " " << xsec_lo << " " << pdf_std_lo << " "
//               << xsec_nlo << " " << pdf_std_nlo << " "
//               << xsec_hadron << " " << pdf_std_hadron << " "
//               << xsec_slepton << " " << pdf_std_slepton << " "
//               << ratio << " " << pdf_std_ratio << "\n";
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

// int main(int argc, char* argv[]) {
//   ltini(); // Initialize LoopTools
//   setlambda(0.0);

//   LHAPDF::setVerbosity(0);
//   const std::string setname = "PDF4LHC21_40";
//   const int n_mem = 43;
  
//   const LHAPDF::PDF* pdf_0 = LHAPDF::mkPDF(setname, 0);

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
//     outfile << "# mass(GeV) | lo(fb) | +-scale_err | nlo(fb) | +-scale_err | hadronside(fb)"
//             << "| +-scale_err | sleptonside(fb) | +-scale_err | ratio | +-scale_err" << std::endl;
    
//     for (int im=0; im < nm; ++im) {
//       Utils::print_progress(im+1, nm);
      
//       const double slepton_mass = m_min + im*dm;
      
//       CrossSection integrator = CrossSection(pdf_0, quark_ids, slepton_id, slepton_id, s);
//       integrator.set_masses(slepton_mass);
//       const double muF_0 = slepton_mass;
//       const double muF_min = muF_0/2.;
//       const double muF_max = 2.*muF_0;
//       const std::vector<double> muF2s = {
//         muF_min * muF_min,
//         muF_0 * muF_0,
//         muF_max * muF_max
//       };
      
//       const double epsrel = 1e-3;
//       const double maxeval = 1e9;
//       std::array<double, 3> xsec_los;
//       std::array<double, 3> xsec_hadrons;
//       std::array<double, 3> xsec_sleptons;
//       std::array<double, 3> xsec_nlos;
//       std::array<double, 3> ratios;
//       for (int i=0; i<3; ++i) {
//         const double muF2 = muF2s.at(i);
//         integrator.muF2 = muF2;
//         setmudim(muF2);
//         xsec_los.at(i) = integrator.full_xsec(0, epsrel, maxeval);
//         xsec_hadrons.at(i) = integrator.full_xsec(1, epsrel, maxeval);
//         xsec_sleptons.at(i) = integrator.full_xsec(2, epsrel, maxeval);
//         xsec_nlos.at(i) = xsec_hadrons.at(i) + xsec_sleptons.at(i);
//         ratios.at(i) = (xsec_los.at(i) + xsec_nlos.at(i))/xsec_los.at(i);
//       }
//       const double xsec_lo = xsec_los.at(1);
//       const double xsec_hadron = xsec_hadrons.at(1);
//       const double xsec_slepton = xsec_sleptons.at(1);
//       const double xsec_nlo = xsec_nlos.at(1);
//       const double ratio = ratios.at(1);

//       const double mu_err_lo = std::abs(xsec_los.at(2) - xsec_los.at(0));
//       const double mu_err_hadron = std::abs(xsec_hadrons.at(2) - xsec_hadrons.at(0));
//       const double mu_err_slepton = std::abs(xsec_sleptons.at(2) - xsec_sleptons.at(0));
//       const double mu_err_nlo = std::abs(xsec_nlos.at(2) - xsec_nlos.at(0));
//       const double mu_err_ratio = std::abs(ratios.at(2) - ratios.at(0));
      
//       outfile << slepton_mass << " " << xsec_lo << " " << mu_err_lo << " "
//               << xsec_nlo << " " << mu_err_nlo << " "
//               << xsec_hadron << " " << mu_err_hadron << " "
//               << xsec_slepton << " " << mu_err_slepton << " "
//               << ratio << " " << mu_err_ratio << "\n";
//     }
//     outfile.close();
//   }
  
//   delete pdf_0;

//   ltexi(); // Print errors and warnings from LoopTools
  
//   return 0;
// }

int main(int argc, char* argv[]) {
  ltini(); // Initialize LoopTools
  setlambda(0.0);

  LHAPDF::setVerbosity(0);
  const std::string setname = "PDF4LHC21_40";
  
  const LHAPDF::PDF* pdf_0 = LHAPDF::mkPDF(setname, 0);

  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double slepton_mass = 700;

  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/xsec_scale_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# SLEPTON_MASS = " << slepton_mass << std::endl;
    outfile << "# mu/mass | lo(fb) | nlo(fb) | hadronside(fb)"
            << "| sleptonside(fb) | ratio" << std::endl;
        
    CrossSection integrator = CrossSection(pdf_0, quark_ids, slepton_id, slepton_id, s);
    integrator.set_masses(slepton_mass);

    const double muF_mass_log2_min = -2.;
    const double muF_mass_log2_max = 2.;
    const int n_muF_mass_log2 = 10;
    const double dmuF_mass = (muF_mass_log2_max - muF_mass_log2_min) / (double) (n_muF_mass_log2 - 1);

    const double epsrel = 1e-3;
    const double maxeval = 2e9;

    for (int imuF=0; imuF<n_muF_mass_log2; ++imuF) {
      Utils::print_progress(imuF+1, n_muF_mass_log2);
      const double muF_mass_log2 = muF_mass_log2_min + (double) imuF * dmuF_mass;
      const double muF_mass = pow(2., muF_mass_log2);
      const double muF = muF_mass * slepton_mass;
      const double muF2 = muF * muF;

      integrator.muF2 = muF2;
      setmudim(muF2);

      const double xsec_lo = integrator.full_xsec(0, epsrel, maxeval);
      const double xsec_hadron = integrator.full_xsec(1, epsrel, maxeval);
      const double xsec_slepton = integrator.full_xsec(2, epsrel, maxeval);
      const double xsec_nlo = xsec_hadron + xsec_slepton;
      const double ratio = (xsec_lo + xsec_nlo)/xsec_lo;

      outfile << muF_mass << " " << xsec_lo << " " << xsec_lo+xsec_nlo << " "
              << xsec_lo+xsec_hadron << " " << xsec_lo+xsec_slepton << " " << ratio << "\n";
    }

    outfile.close();
  }
  
  
  delete pdf_0;

  ltexi(); // Print errors and warnings from LoopTools
  
  return 0;
}