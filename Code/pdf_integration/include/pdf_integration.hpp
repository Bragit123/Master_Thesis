#ifndef PDF_INTEGRATION_HPP
#define PDF_INTEGRATION_HPP

namespace pdf_integration {
  // Do x-loop part of integration
  double x_int_delta_dist();
  double x_int_plus_dist();
  double x_int_general();

  double parton_sum(); // Loop over partons, do x_int for each parton

  double Q_int(); // Loop over Q's (and integrate? or just return dsigma/dQ2 as vector?)

  double M_spectrum(); // Loop over masses to get spectrum
  double mixing_spectrum(); // Loop over stau-mixing angles to get spectrum

  double write_to_file(); // Maybe put in utils?
  double read_file(); // Maybe put in utils?
}


#endif