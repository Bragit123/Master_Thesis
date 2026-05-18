#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

#include "Utils.hpp"
#include "CrossSection.hpp"

int main(int argc, char* argv[]) {
  const std::string setname = "PDF4LHC21_40";
  const int mem = 0; // Only considering central PDF for now. Expanding laterz!

  LHAPDF::setVerbosity(0);
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, mem);
  const std::vector<int> quark_ids = {1, 2, 3, 4, 5}; // note: no top quark

  const double s_sqrt = 13'000.0; // 13 TeV
  const double s = s_sqrt*s_sqrt;

  //Slepton mass
  const double m_min = 100.0;
  const double m_max = 1000.0;
  const double dm = 100.0;
  const double nm = std::floor((m_max - m_min) / dm) + 1;

  
  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/sigma_lo_" + std::to_string(slepton_id) + ".dat";
    std::ofstream out_file(filename);
    
    // const double slepton_mass = 400;
    // CrossSection integrator = CrossSection(pdf, quark_ids, slepton_id, slepton_id, s);
    // integrator.set_masses(slepton_mass);
    
    // const double Q2_min = 2.0*slepton_mass;
    // const double Q2_max = s;
    // const double nQ2 = 1000;
    // const double dQ2 = std::floor((Q2_max - Q2_min) / (double) nQ2);
    
    // for (int iQ2=0; iQ2 < nQ2; ++iQ2) {
    //   Utils::print_progress(iQ2+1, nQ2);
      
    //   double Q2 = Q2_min + iQ2*dQ2;
    //   const double diff_xsec = integrator.diff_xsec(Q2);
      
      
    //   out_file << Q2 << " " << diff_xsec << "\n";
    // }
    
    for (int im=0; im < nm; ++im) {
      Utils::print_progress(im+1, nm);
      
      const double slepton_mass = m_min + im*dm;
      
      CrossSection integrator = CrossSection(pdf, quark_ids, slepton_id, slepton_id, s);
      integrator.set_masses(slepton_mass);
      
      const double total_xsec = integrator.full_xsec();
      
      out_file << slepton_mass << " " << total_xsec << "\n";
    }
    
    out_file.close();
  }

  delete pdf;
  
  return 0;
}