#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include <math.h>

using string = std::string;

namespace Const {
  // Values taken from PDG
  const double GF = 1.16638e-5; // Fermi constant

  const double MW = 80.369;
  const double MW2 = MW*MW;

  const double MZ = 91.188;
  const double MZ2 = MZ*MZ;
  const double GAMMAZ = 2.4955;
  const double GAMMAZ2 = GAMMAZ*GAMMAZ;

  const double SW2 = 1.0 - MW2 / (MZ2); // Sin(thetaW)^2
  const double ALPHA = std::sqrt(2.0) * GF * MW2 * SW2 / M_PI;

  const double NC = 3.0;
  const double BORN_PREFAC = 8.0 * M_PI * ALPHA*ALPHA / (3.0 * NC);
}

double F_coupling(bool up_type_quark, int slepton_id, double Q2) {
  // WARNING: Assumes equal sleptons!
  double Qq;
  double Zql;
  double Zqr;
  if (up_type_quark) {
    Qq = 2.0/3.0;
    Zql = -0.25 * (1.0 - 2.0 * Qq * Const::SW2);
    Zqr = 0.5 * Qq * Const::SW2;
  } else {
    Qq = -1.0/3.0;
    Zql = 0.25 * (1.0 + 2.0 * Qq * Const::SW2);
    Zqr = 0.5 * Qq * Const::SW2;
  }
  double ZAB = -Const::SW2;
  if (slepton_id / 1'000'000 == 1) {
    // If left-handed: add mixing-matrix part
    ZAB += 0.5;
  }
  const double SW2CW2_inv = 1.0 / (Const::SW2 * (1.0-Const::SW2));
  const double Q2MZ2 = Q2 - Const::MZ2;
  const double Zprop = 1.0 / (Q2MZ2*Q2MZ2 + Const::MZ2 * Const::GAMMAZ2);
  double F = Qq*Qq - 2 * Qq * ZAB * SW2CW2_inv * (Zql+Zqr) * Q2*(Q2-Const::MZ2) * Zprop
             + 2 * ZAB*ZAB * SW2CW2_inv*SW2CW2_inv * (Zql*Zql + Zqr*Zqr) * Q2*Q2 * Zprop;
  
  return F;
}

double born_cross_section(int quark_id, int slepton_id, double s, double Q, double mass) {
  // WARNING: Assumes equal sleptons!
  const double Q2 = Q*Q;
  const double Q5 = Q2*Q2*Q;
  const double mass2 = mass*mass;
  // const double mom_squared = 0.25*Q2 - 0.5*(massA2 + massB2) + 0.25*(massA2 - massB2) / Q2;
  const double mom2 = 0.25*Q2 - mass2; // Slepton 3-momentum in slepton RF (squared)
  const double mom3 = std::pow(mom2, 3.0/2.0);

  bool up_type_quark = false;
  if (quark_id % 2 == 0) {
    up_type_quark = true;
  }
  const double F = F_coupling(up_type_quark, slepton_id, Q2);
  
  double sigmaB = Const::BORN_PREFAC * mom3 / (s * Q5) * F;

  // std::cout << mom3 << " | " << Q5 << " | " << F << " | " << sigmaB << "\n";
  
  return sigmaB;
}

int main(int argc, char* argv[]) {
  const string setname = "PDF4LHC21_40";
  const int mem = 0; // Only considering central PDF for now. Expanding laterz!
  
  const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, mem);
  std::vector<int> pids = pdf->flavors();
  
  const double s_sqrt = 13'000.0; // 13 Tev
  const double s = s_sqrt*s_sqrt;

  // Slepton mass
  const double MINM = 100.0;
  const double MAXM = 2000.0;
  const double DM = 100.0;
  const double NM = std::floor((MAXM - MINM)/DM) + 1;
  
  // const int sid = 1000011; // Left-selectron
  // const int sid = 2000011; // Right-selectron
  // const int sid = 1000013; // Left-smuon
  const int sid = 2000013; // Right-smuon
  string filename = "output/sigma_lo_" + std::to_string(sid) + ".dat";
  std::ofstream out_file(filename);
  for (int im=0; im < NM; ++im) {
    std::cout << "\rProgress: " << std::setw(3) << std::setprecision(3) << std::floor(100*im/(NM+1)) << "%" << std::flush;
    const double slepton_mass = MINM + im*DM;
    // const double slepton_mass = 100;
    const double MUF2 = slepton_mass * slepton_mass;
    
    const double MINQ = 2.0*slepton_mass;
    const double MAXQ = s_sqrt;
    // const double DQ = 1.0;
    const double DQ = 10.0;
    const double NQ = std::floor((MAXQ - MINQ)/DQ) + 1;
    
    // std::cout << "NQ = " << NQ << "\n";
    
    // string filename = "output/dsigma_lo_" + std::to_string(sid) + ".dat";
    // std::ofstream out_file(filename);
    double total_sigma = 0.0;
    for (int iQ=0; iQ < NQ; ++iQ) {
      // std::cout << "\rProgress: " << std::setw(3) << std::setprecision(3) << std::floor(100*iQ/(NQ+1)) << "%" << std::flush;
      
      const double Q = MINQ + iQ*DQ;
      const double tau = Q*Q/s;
      
      const double MINLOGX = std::log10(tau);
      const double MAXLOGX = 0;
      const double DX = 0.001;
      const int NX = (int) std::floor((MAXLOGX - MINLOGX)/DX) + 1;
      
      double dsigma_dQ2 = 0.0;
      for (int qid=1; qid <= 6; ++qid) {
        // Looping over quarks only
        const double sigmaB = born_cross_section(qid, sid, s, Q, slepton_mass);
        double sum = 0.0;
        for (int ix=1; ix < NX; ++ix) {
          double log10x = MINLOGX + ix*DX;
          double x1 = std::pow(10, log10x);
          double x2 = tau / x1;
          
          // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
          const double tol = 1e-10;
          if (std::abs(x1 - 1.0) < tol) {
            x1 = 1.0;
          }
          if (std::abs(x2 - 1.0) < tol) {
            x2 = 1.0;
          }
          
          const double xfq = pdf->xfxQ2(qid, x1, MUF2);
          const double xfqbar = pdf->xfxQ2(-qid, x2, MUF2);
          
          sum += xfq * xfqbar / tau; // x1*x2 = x1 * tau/x1 = tau
          // std::cout << xfq << " | " << xfqbar << " | " << tau << " | " << sum << "\n";
        }
        const double xfqtau = pdf->xfxQ2(qid, tau, MUF2);
        const double xfq1 = pdf->xfxQ2(qid, 1, MUF2);
        const double xfqbartau = pdf->xfxQ2(-qid, tau, MUF2);
        const double xfqbar1 = pdf->xfxQ2(-qid, 1, MUF2);
        dsigma_dQ2 += sigmaB * (0.5*(xfqtau * xfqbar1 + xfq1 * xfqbartau)/tau + sum);
        // std::cout << xfqtau << " | " << xfq1 << " | " << xfqbartau << " | " << xfqbar1 << " | " << tau << " | " << sum << " | " << sigmaB << "\n";
      }
      dsigma_dQ2 *= DX * std::log(10);
      // out_file << Q << " " << dsigma_dQ2 << "\n";
      total_sigma += dsigma_dQ2 * DQ;
      // std::cout << tau << "\n";
    }
    out_file << slepton_mass << " " << total_sigma << "\n";
    // out_file.close();
  }
  out_file.close();
  // std::cout << "total_sigma = " << total_sigma << " (GeV)^(-2)\n";
}