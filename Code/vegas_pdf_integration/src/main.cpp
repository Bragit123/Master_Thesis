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
  const double m_min = 100.;
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
      
      CrossSection integrator = CrossSection(pdf, quark_ids, slepton_id, slepton_id, s);
      integrator.set_masses(slepton_mass);
      const double muF2 = slepton_mass*slepton_mass;
      setmudim(muF2);
      
      const double xsec_lo = integrator.full_xsec(0);
      const double xsec_hadron = integrator.full_xsec(1);
      const double xsec_slepton = integrator.full_xsec(2);
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