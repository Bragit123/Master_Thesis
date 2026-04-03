#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>
#include "Random.h"
#include "Integration.h"

using string = std::string;

int main(int argc, char* argv[]) {
	const string setname = "PDF4LHC21_40";
	const int mem = 0;

	const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, mem);
	std::vector<int> pids = pdf->flavors();

	const double MINLOGX = -10;
	const double MAXLOGX = 0;
	const double DX = 0.01;
	const int NX = (int) std::floor((MAXLOGX - MINLOGX)/DX) + 1;

	const double MINLOGQ2 = 1;
	const double MAXLOGQ2 = 8;
	const double DQ2 = 0.01;
	const int NQ2 = (int) std::floor((MAXLOGQ2 - MINLOGQ2)/DQ2) + 1;

	std::vector<double> dsigma_dq2_total(NQ2);

	const double tau = 1e-10; // Arbitrary value, should be replaced!

	for (int iq2=0; iq2 < NQ2; ++iq2) {
		const double log10q2 = MINLOGQ2 + iq2*DQ2;
		const double q2 = std::pow(10, log10q2);
		double dsigma = 0;
		for (int pid1 : pids) {
			for (int pid2 : pids) {
				for (int ix=0; ix < NX; ++ix) {
					const double log10x = (MINLOGX + ix*DX < -1e-3) ? (MINLOGX + ix*DX) : 0.0;
					const double x1 = std::pow(10, log10x);
					const double x2 = tau/x1;

					// Note: Using Q^2 as the factorization scale mu_R:
					const double xf1 = pdf->xfxQ2(pid1, x1, q2);
					const double xf2 = pdf->xfxQ2(pid2, x2, q2);
					
					double dsigma_partonic = 1.0; // Set to unity for now. Should be replaced!
					
					// So far assuming that partonic cross section is proportional to delta(1-z)
					// (and not including delta(1-z) in dsigma_partonic)
					dsigma += xf1/x1 * xf2 * dsigma_partonic;
				}
			}
		}
		dsigma_dq2_total.at(iq2) = dsigma;

		std::ofstream out_file("dsigma_test.dat");
		for (int i=0; i<NQ2; ++i) {
			const double log10q2 = MINLOGQ2 + i*DQ2;
			const double q2 = std::pow(10, log10q2);
			out_file << q2 << " " << dsigma_dq2_total.at(i) << std::endl;
		}
		out_file.close();
	}
  
	return 0;
}