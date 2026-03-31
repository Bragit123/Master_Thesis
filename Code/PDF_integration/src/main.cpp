#include "LHAPDF/LHAPDF.h"
#include <iostream>
#include <fstream>

using string = std::string;

int main(int argc, char* argv[]) {
    
  if (argc < 3) {
		std::cerr << "You must specify a PDF set and member number." << std::endl;
		return 1;
	}

	// Extract PDF set name and member number from command line input
	const string setname = argv[1];
	const string smem = argv[2];
	const int imem = LHAPDF::lexical_cast<int>(smem);

	const LHAPDF::PDF* pdf = LHAPDF::mkPDF(setname, imem);
	std::vector<int> pids = pdf->flavors();

	const double MINLOGX = -10;
	const double MAXLOGX = 0;
	const double DX = 0.01;
	const int NX = (int) std::floor((MAXLOGX - MINLOGX)/DX) + 1;

	const double MINLOGQ2 = 1;
	const double MAXLOGQ2 = 8;
	const double DQ2 = 0.01;
	const int NQ2 = (int) std::floor((MAXLOGQ2 - MINLOGQ2)/DQ2) + 1;

	const string OUTPUT_DIR = "output/";
	for (int pid : pids) {
		const string spid = LHAPDF::lexical_cast<string>(pid);
		const string filename = OUTPUT_DIR + setname + "_" + smem + "_" + spid + ".dat";

		std::ofstream out_file(filename);
		for (int ix=0; ix < NX; ++ix) {
			// If log10x is very close to 0, set it to 0
			const double log10x = (MINLOGX + ix*DX < -1e-3) ? (MINLOGX + ix*DX) : 0;
			const double x = std::pow(10, log10x);
			for (int iq2=0; iq2 < NQ2; ++iq2) {
				const double log10q2 = MINLOGQ2 + iq2*DQ2;
				const double q2 = std::pow(10, log10q2);
				const double xf = pdf->xfxQ2(pid, x, q2);

				out_file << x << " " << q2 << " "  << xf << std::endl;
			}
		}
		out_file.close();
	}

	delete pdf;
	return 0;
}