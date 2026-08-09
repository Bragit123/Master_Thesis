#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <array>
#include "clooptools.h"

#include "Utils.hpp"
#include "CrossSection.hpp"

// Function declarations
void compute_xsec_over_mass(double epsrel=1e-3, double maxeval=1e8);
void compute_xsec_with_scale_err(double epsrel=1e-3, double maxeval=1e8);
void compute_xsec_over_scale(double slepton_mass=100, bool varyR=false, double epsrel=1e-3, double maxeval=1e8);
void compute_with_pdf_err(double epsrel=1e-3, double maxeval=1e8);
void compute_xsec_with_errs(double epsrel=1e-3, double maxeval=1e8);



int main(int argc, char* argv[]) {
  
  compute_xsec_over_mass(1e-3);
  // compute_xsec_with_scale_err(1e-2, 1e8);
  // compute_xsec_with_errs(1e-3);
  // compute_xsec_over_scale(400, true, 1e-3);
  // compute_xsec_over_scale(600, true, 1e-3);
  // compute_xsec_over_scale(800, true, 1e-3);
  // compute_xsec_over_scale(1000, true, 1e-3);
  // compute_with_pdf_err(1e-2);
  
  return 0;
}


/////////////////////
/// Cross Section ///
/////////////////////
void compute_xsec_over_mass(double epsrel, double maxeval) {
  ltini(); // Initialize LoopTools
  setlambda(0.0);
  const std::string setname = "PDF4LHC21_40";
  const int mem = 0; // Only considering central PDF for now. Expanding laterz!

  LHAPDF::setVerbosity(0);
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, mem);
  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double m_min = 300.;
  const double m_max = 1000.;
  const double dm = 100.;
  const double nm = std::floor((m_max - m_min) / dm) + 1;
  
  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/xsec_mass_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# mass(GeV) lo(fb) nlo(fb) hadronside(fb) sleptonside(fb)" << std::endl;
    
    for (int im=0; im < nm; ++im) {
      Utils::print_progress(im+1, nm);
      
      const double slepton_mass = m_min + im*dm;
      const double mass_tot = slepton_mass + slepton_mass;
      const double Q2_min = mass_tot * mass_tot;
      const double Q2_max = s;
      const double mu = 0.5 * mass_tot;
      const double muR2 = mu * mu;
      const double muF2 = muR2;
      setmudim(muR2);
      // setmudim(muF2);

      const CSParams params {
        .sleptonA_id = slepton_id,
        .sleptonB_id = slepton_id,
        .mA = slepton_mass,
        .mB = slepton_mass,
        .s = s,
        .Q2_min = Q2_min,
        .Q2_max = Q2_max,
        .muR2 = muR2,
        .muF2 = muF2,
        .pdf = pdf,
        .mix_cos = 1.0
      };
      
      // const double epsrel = 1e-2;
      // const double maxeval = 1e9;
      const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
      const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
      const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
      const double xsec_nlo = xsec_hadron + xsec_slepton;
      
      outfile << slepton_mass << " " << xsec_lo << " " << xsec_lo + xsec_nlo
              << " " << xsec_lo + xsec_hadron << " " << xsec_lo + xsec_slepton << "\n";
    }
    outfile.close();
  }
  
  delete pdf;

  ltexi(); // Print errors and warnings from LoopTools
}




//////////////////
/// With Error ///
//////////////////
void compute_xsec_with_errs(double epsrel, double maxeval) {
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

  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double m_min = 100.;
  const double m_max = 1000.;
  const double dm = 200.;
  const double nm = std::floor((m_max - m_min) / dm) + 1;
  
  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/xsec_mass_err_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# mass(GeV) | lo(fb) | lo_scale- | lo_scale+ | lo_pdf_err | nlo(fb) | nlo_scale- | nlo_scale+ | nlo_pdf_err" << std::endl;
    
    for (int im=0; im < nm; ++im) {
      Utils::print_progress(im+1, nm);
      
      const double slepton_mass = m_min + im*dm;
      const double mass_tot = slepton_mass + slepton_mass;
      const double Q2_min = mass_tot * mass_tot;
      const double Q2_max = s;

      const double mu_0 = 0.5 * mass_tot;
      const double mu_min = mu_0/2.;
      const double mu_max = 2.*mu_0;
      const std::vector<double> mu2s = {
        mu_min * mu_min,
        mu_0 * mu_0,
        mu_max * mu_max
      };

      const CSParams params_0 {
        .sleptonA_id = slepton_id,
        .sleptonB_id = slepton_id,
        .mA = slepton_mass,
        .mB = slepton_mass,
        .s = s,
        .Q2_min = Q2_min,
        .Q2_max = Q2_max,
        .muR2 = mu_0*mu_0,
        .muF2 = mu_0*mu_0,
        .pdf = pdf_0,
        .mix_cos = 1.0
      };
      
      std::array<double, 3> xsec_los;
      std::array<double, 3> xsec_nlos;
      for (int i=0; i<3; ++i) {
        const double muR2 = mu2s.at(i);
        const double muF2 = mu2s.at(i);
        setmudim(muR2);

        CSParams params = params_0;
        params.muR2 = muR2;
        params.muF2 = muF2;

        xsec_los.at(i) = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
        const double xsec_hadrons_i = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
        const double xsec_sleptons_i = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
        xsec_nlos.at(i) = xsec_los.at(i) + xsec_hadrons_i + xsec_sleptons_i;
      }
      const double xsec_lo = xsec_los.at(1);
      const double xsec_nlo = xsec_nlos.at(1);

      double lo_scale_plus;
      double lo_scale_minus;
      double nlo_scale_plus;
      double nlo_scale_minus;
      
      if (xsec_los.at(2) > xsec_los.at(0)) {
        lo_scale_plus = xsec_los.at(2);
        lo_scale_minus = xsec_los.at(0);
      } else {
        lo_scale_plus = xsec_los.at(0);
        lo_scale_minus = xsec_los.at(2);
      }

      if (xsec_nlos.at(2) > xsec_nlos.at(0)) {
        nlo_scale_plus = xsec_nlos.at(2);
        nlo_scale_minus = xsec_nlos.at(0);
      } else {
        nlo_scale_plus = xsec_nlos.at(0);
        nlo_scale_minus = xsec_nlos.at(2);
      }

      // PDF ERROR
      setmudim(mu_0*mu_0);
      double pdf_variance_lo = 0.0;
      double pdf_variance_nlo = 0.0;
      for (int i=0; i<n_mem-1; ++i) {
        // Utils::print_progress(i+1, n_mem-1);
        const LHAPDF::PDF* pdf_i = err_pdfs.at(i);
        CSParams params_i = params_0;
        params_i.pdf = pdf_i;

        const double xsec_lo_i = CrossSection::full_xsec(params_i, quark_ids, 0, epsrel, maxeval);
        const double xsec_diff_lo = xsec_lo_i - xsec_lo;
        pdf_variance_lo += xsec_diff_lo * xsec_diff_lo;

        const double xsec_hadron_i = CrossSection::full_xsec(params_i, quark_ids, 1, epsrel, maxeval);
        const double xsec_slepton_i = CrossSection::full_xsec(params_i, quark_ids, 2, epsrel, maxeval);
        const double xsec_nlo_i = xsec_lo_i + xsec_hadron_i + xsec_slepton_i;
        const double xsec_diff_nlo = xsec_nlo_i - xsec_nlo;
        pdf_variance_nlo += xsec_diff_nlo * xsec_diff_nlo;
      }

      const double lo_pdf_err = sqrt(pdf_variance_lo);
      const double nlo_pdf_err = sqrt(pdf_variance_nlo);
      
      outfile << slepton_mass << " "
              << xsec_lo << " " << lo_scale_minus << " " << lo_scale_plus << " " << lo_pdf_err << " "
              << xsec_nlo << " " << nlo_scale_minus << " " << nlo_scale_plus << " " << nlo_pdf_err << std::endl;
    }
    outfile.close();
  }
  
  delete pdf_0;
  for (LHAPDF::PDF* pdf : err_pdfs) {
    delete pdf;
  }

  ltexi(); // Print errors and warnings from LoopTools
}



///////////////////
/// Scale Error ///
///////////////////
void compute_xsec_with_scale_err(double epsrel, double maxeval) {
  ltini(); // Initialize LoopTools
  setlambda(0.0);

  LHAPDF::setVerbosity(0);
  const std::string setname = "PDF4LHC21_40";
  
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, 0);

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
    
    std::string filename = "output/xsec_mass_scale_err_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# mass(GeV) | lo(fb) | lo_scale- | lo_scale+ | nlo(fb) | nlo_scale- | nlo_scale+" << std::endl;
    
    for (int im=0; im < nm; ++im) {
      Utils::print_progress(im+1, nm);
      
      const double slepton_mass = m_min + im*dm;
      const double mass_tot = slepton_mass + slepton_mass;
      const double Q2_min = mass_tot * mass_tot;
      const double Q2_max = s;
      // const double muF_0 = 0.5 * mass_tot;
      // const double muF_min = muF_0/2.;
      // const double muF_max = 2.*muF_0;
      // const std::vector<double> muF2s = {
      //   muF_min * muF_min,
      //   muF_0 * muF_0,
      //   muF_max * muF_max
      // };
      // const double mu_0 = 0.5 * mass_tot;
      // const double mu_min = mu_0/2.;
      // const double mu_max = 2.*mu_0;
      // const std::vector<double> mu2s = {
      //   mu_min * mu_min,
      //   mu_0 * mu_0,
      //   mu_max * mu_max
      // };

      const double mu_0 = 0.5 * mass_tot;
      const double mu_half = 0.5 * mu_0;
      const double mu_double = 2. * mu_0;
      const double mu2_0 = mu_0*mu_0;
      const double mu2_half = mu_half*mu_half;
      const double mu2_double = mu_double*mu_double;
      // const std::vector<std::vector<double>> mu2RFs = {
      //   {1., 1.},
      //   {.5, .5},
      //   {.5, 1.},
      //   {1., .5},
      //   {1., 2.},
      //   {2., 1.},
      //   {2., 2.}
      // };
      
      const CSParams params_0 {
        .sleptonA_id = slepton_id,
        .sleptonB_id = slepton_id,
        .mA = slepton_mass,
        .mB = slepton_mass,
        .s = s,
        .Q2_min = Q2_min,
        .Q2_max = Q2_max,
        .muR2 = mu2_0,
        .muF2 = mu2_0,
        .pdf = pdf,
        .mix_cos = 1.0
      };
      
      //// Central scale
      setmudim(params_0.muR2);
      const double xsec_lo_0 = CrossSection::full_xsec(params_0, quark_ids, 0, epsrel, maxeval);
      const double xsec_hadron_0 = CrossSection::full_xsec(params_0, quark_ids, 1, epsrel, maxeval);
      const double xsec_slepton_0 = CrossSection::full_xsec(params_0, quark_ids, 2, epsrel, maxeval);
      const double xsec_nlo_0 = xsec_lo_0 + xsec_hadron_0 + xsec_slepton_0;
      
      // const std::vector<std::vector<double>> mu2RFs = {
      //   {mu2_half, mu2_half},
      //   {mu2_half, mu2_0},
      //   {mu2_0, mu2_half},
      //   {mu2_0, mu2_double},
      //   {mu2_double, mu2_0},
      //   {mu2_double, mu2_double}
      // };
      
      // Cross section turns out to be independent of muR, so only need to vary muF
      const std::vector<std::vector<double>> mu2RFs = {
        {mu2_0, mu2_half},
        {mu2_0, mu2_double},
      };
      
      //// Scale uncertainty
      double lo_scale_minus = xsec_lo_0;
      double lo_scale_plus = xsec_lo_0;
      double nlo_scale_minus = xsec_nlo_0;
      double nlo_scale_plus = xsec_nlo_0;
      
      for (int i=0; i<mu2RFs.size(); ++i) {
        const double muR2 = mu2RFs.at(i).at(0);
        const double muF2 = mu2RFs.at(i).at(1);

        setmudim(muR2);
        CSParams params = params_0;
        params.muR2 = muR2;
        params.muF2 = muF2;
        
        const double xsec_lo_i = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
        const double xsec_hadrons_i = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
        const double xsec_sleptons_i = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
        const double xsec_nlo_i = xsec_lo_i + xsec_hadrons_i + xsec_sleptons_i;

        if (xsec_lo_i < lo_scale_minus) {lo_scale_minus = xsec_lo_i;}
        if (xsec_lo_i > lo_scale_plus) {lo_scale_plus = xsec_lo_i;}
        if (xsec_nlo_i < nlo_scale_minus) {nlo_scale_minus = xsec_nlo_i;}
        if (xsec_nlo_i > nlo_scale_plus) {nlo_scale_plus = xsec_nlo_i;}
      }

      outfile << slepton_mass << " "
              << xsec_lo_0 << " " << lo_scale_minus << " " << lo_scale_plus << " "
              << xsec_nlo_0 << " " << nlo_scale_minus << " " << nlo_scale_plus << std::endl;
    }
    outfile.close();
  }
  
  delete pdf;

  ltexi(); // Print errors and warnings from LoopTools
}




/////////////////////
/// xsec vs scale ///
/////////////////////
// Always varies muF, but only varies muR if varyR is true
void compute_xsec_over_scale(double slepton_mass, bool varyR, double epsrel, double maxeval) {
  ltini(); // Initialize LoopTools
  setlambda(0.0);

  LHAPDF::setVerbosity(0);
  const std::string setname = "PDF4LHC21_40";
  
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, 0);

  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double mass_tot = slepton_mass + slepton_mass;
  const double Q2_min = mass_tot * mass_tot;
  const double Q2_max = s;

  // std::vector<int> slepton_ids = {1000011, 2000011};
  std::vector<int> slepton_ids = {1000011}; // Sufficient to consider left-handed selectrons for this
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    const double mu_0 = 0.5 * mass_tot;
    const double mu2_0 = mu_0 * mu_0;
    
    const double mu_mass_log2_min = -3.;
    const double mu_mass_log2_max = 3.;
    const int n_mu_mass_log2 = 7;
    // const double mu_mass_log2_min = -4.;
    // const double mu_mass_log2_max = 4.;
    // const int n_mu_mass_log2 = 9;
    const double dmu_mass = (mu_mass_log2_max - mu_mass_log2_min) / (double) (n_mu_mass_log2 - 1);
    
    const CSParams params_0 {
      .sleptonA_id = slepton_id,
      .sleptonB_id = slepton_id,
      .mA = slepton_mass,
      .mB = slepton_mass,
      .s = s,
      .Q2_min = Q2_min,
      .Q2_max = Q2_max,
      .muR2 = mu2_0,
      .muF2 = mu2_0,
      .pdf = pdf,
      .mix_cos = 1.0
    };
    
    std::string filenameF = "output/xsec_scaleF_m" + std::to_string((int) slepton_mass) + "_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfileF(filenameF);
    outfileF << "# SLEPTON_MASS = " << slepton_mass << std::endl;
    outfileF << "# mu/mass | lo(fb) | nlo(fb) | hadronside(fb)"
            << "| sleptonside(fb)" << std::endl;
    
    // Vary muF
    std::cout << "Varying Factorization Scale" << std::endl;
    for (int imu=0; imu<n_mu_mass_log2; ++imu) {
      Utils::print_progress(imu+1, n_mu_mass_log2);
      const double muF_mass_log2 = mu_mass_log2_min + (double) imu * dmu_mass;
      const double muF_mass = pow(2., muF_mass_log2);
      const double muF = muF_mass * slepton_mass;
      const double muF2 = muF * muF;
      
      setmudim(params_0.muR2);
      clearcache();

      CSParams params = params_0;
      params.muF2 = muF2;

      const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
      const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
      const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
      const double xsec_nlo = xsec_lo + xsec_hadron + xsec_slepton;
      
      outfileF << muF_mass << " " << xsec_lo << " " << xsec_nlo << " "
      << xsec_lo+xsec_hadron << " " << xsec_lo+xsec_slepton << std::endl;
    }
    
    outfileF.close();

    if (varyR) {
      std::string filenameR = "output/xsec_scaleR_m" + std::to_string((int) slepton_mass) + "_" + std::to_string(slepton_id) + ".dat";
      std::ofstream outfileR(filenameR);
      outfileR << "# SLEPTON_MASS = " << slepton_mass << std::endl;
      outfileR << "# mu/mass | lo(fb) | nlo(fb) | hadronside(fb)"
              << "| sleptonside(fb)" << std::endl;
      
      // Vary muR
      std::cout << "Varying Renormalization Scale" << std::endl;
      for (int imu=0; imu<n_mu_mass_log2; ++imu) {
        Utils::print_progress(imu+1, n_mu_mass_log2);
        const double muR_mass_log2 = mu_mass_log2_min + (double) imu * dmu_mass;
        const double muR_mass = pow(2., muR_mass_log2);
        const double muR = muR_mass * slepton_mass;
        const double muR2 = muR * muR;
        
        CSParams params = params_0;
        params.muR2 = muR2;
        setmudim(params.muR2);
        clearcache();
        
        const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
        const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
        const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
        const double xsec_nlo = xsec_lo + xsec_hadron + xsec_slepton;
        
        outfileR << muR_mass << " " << xsec_lo << " " << xsec_nlo << " "
                << xsec_lo+xsec_hadron << " " << xsec_lo+xsec_slepton << std::endl;
      }
      outfileR.close();
    }
  }
  
  
  delete pdf;

  ltexi(); // Print errors and warnings from LoopTools
}




//////////////////
/// PDF ERRORS ///
//////////////////
void compute_with_pdf_err(double epsrel, double maxeval) {
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
    
    std::string filename = "output/xsec_mass_pdf_err_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# mass(GeV) | lo(fb) | +-PDFerr | nlo(fb) | +-PDFerr" << std::endl;
    
    for (int im=0; im < nm; ++im) {
      std::cout << "Mass: " << im+1 << "/" << nm << std::endl;
      
      const double slepton_mass = m_min + im*dm;
      const double mass_tot = slepton_mass + slepton_mass;
      const double Q2_min = mass_tot * mass_tot;
      const double Q2_max = s;
      const double mu = 0.5 * mass_tot;
      const double muR2 = mu * mu;
      const double muF2 = muR2;
      setmudim(muR2);
      const CSParams params {
        .sleptonA_id = slepton_id,
        .sleptonB_id = slepton_id,
        .mA = slepton_mass,
        .mB = slepton_mass,
        .s = s,
        .Q2_min = Q2_min,
        .Q2_max = Q2_max,
        .muR2 = muR2,
        .muF2 = muF2,
        .pdf = pdf_0,
        .mix_cos = 1.0
      };
      
      // const double epsrel = 1e-1;
      // const double maxeval = 1e8;
      const double xsec_lo = CrossSection::full_xsec(params, quark_ids, 0, epsrel, maxeval);
      const double xsec_hadron = CrossSection::full_xsec(params, quark_ids, 1, epsrel, maxeval);
      const double xsec_slepton = CrossSection::full_xsec(params, quark_ids, 2, epsrel, maxeval);
      const double xsec_nlo = xsec_lo + xsec_hadron + xsec_slepton;

      double pdf_variance_lo = 0.0;
      double pdf_variance_nlo = 0.0;
      for (int i=0; i<n_mem-1; ++i) {
        Utils::print_progress(i+1, n_mem-1);
        const LHAPDF::PDF* pdf_i = err_pdfs.at(i);
        CSParams params_i = params;
        params_i.pdf = pdf_i;

        const double xsec_lo_i = CrossSection::full_xsec(params_i, quark_ids, 0, epsrel, maxeval);
        const double xsec_diff_lo = xsec_lo_i - xsec_lo;
        pdf_variance_lo += xsec_diff_lo * xsec_diff_lo;

        const double xsec_hadron_i = CrossSection::full_xsec(params_i, quark_ids, 1, epsrel, maxeval);
        const double xsec_slepton_i = CrossSection::full_xsec(params_i, quark_ids, 2, epsrel, maxeval);
        const double xsec_nlo_i = xsec_lo_i + xsec_hadron_i + xsec_slepton_i;
        const double xsec_diff_nlo = xsec_nlo_i - xsec_nlo;
        pdf_variance_nlo += xsec_diff_nlo * xsec_diff_nlo;
      }

      const double pdf_std_lo = sqrt(pdf_variance_lo);
      const double pdf_std_nlo = sqrt(pdf_variance_nlo);

      outfile << slepton_mass << " " << xsec_lo << " " << pdf_std_lo << " "
              << xsec_nlo << " " << pdf_std_nlo << std::endl;
    }
    outfile.close();
  }
  
  delete pdf_0;
  for (LHAPDF::PDF* pdf : err_pdfs) {
    delete pdf;
  }

  ltexi(); // Print errors and warnings from LoopTools
}