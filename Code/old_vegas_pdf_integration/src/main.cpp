#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include "clooptools.h"

#include "Utils.hpp"
#include "CrossSection.hpp"

int main(int argc, char* argv[]) {
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
  const double m_min = 100.0;
  const double m_max = 1000.0;
  const double dm = 100.0;
  const double nm = std::floor((m_max - m_min) / dm) + 1;
  
  std::vector<int> slepton_ids = {1000011, 2000011};
  for (int slepton_id : slepton_ids) {
    std::cout << "Slepton " << slepton_id << ":\n";
    
    std::string filename = "output/xsec_mass_" + std::to_string(slepton_id) + ".dat";
    std::ofstream outfile(filename);
    outfile << "# mass lo nlo hadronside sleptonside" << std::endl;
    
    for (int im=0; im < nm; ++im) {
      Utils::print_progress(im+1, nm);
      
      const double slepton_mass = m_min + im*dm;
      
      CrossSection integrator = CrossSection(pdf, quark_ids, slepton_id, slepton_id, s);
      integrator.set_masses(slepton_mass);
      const double muF2 = slepton_mass*slepton_mass;
      setmudim(muF2);
      
      // const double xsec_lo = integrator.full_xsec(0);

      // const double m_tot = 2.*slepton_mass;
      // const double Q2_min = m_tot*m_tot;
      // const double Q2_max = s;
      // const int NQ2 = 100;
      // const double dQ2 = (Q2_max - Q2_min + 1.) / (double) NQ2;
      // double xsec_lo = 0.0;
      // for (int i=0; i < NQ2; ++i) {
      //   const double Q2 = Q2_min + i*dQ2;
      //   integrator.Q2 = Q2;
      //   xsec_lo += dQ2*integrator.diff_xsec(0);
      //   // std::cout << xsec_lo << std::endl;
      // }

      const double xsec_lo = 0.0;
      // const double xsec_hadron = 0.0;
      const double xsec_slepton = 0.0;
      const double xsec_hadron = integrator.full_xsec(1);
      // const double xsec_slepton = integrator.full_xsec(2);
      const double xsec_nlo = xsec_hadron + xsec_slepton;
      
      outfile << slepton_mass << " " << xsec_lo << " " << xsec_nlo
              << " " << xsec_hadron << " " << xsec_slepton << "\n";
    }
    outfile.close();
  }
  
  delete pdf;

  ltexi(); // Print errors and warnings from LoopTools
  
  return 0;
}