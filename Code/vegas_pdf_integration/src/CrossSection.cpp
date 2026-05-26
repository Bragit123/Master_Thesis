#include "CrossSection.hpp"

#include "LHAPDF/LHAPDF.h"
#include "Utils.hpp"

#include <cmath>
#include <vector>
#include "clooptools.h"

// Constructor
CrossSection::CrossSection(
    const LHAPDF::PDF* pdf_,
    const std::vector<int> quark_ids_,
    const int sleptonA_id_,
    const int sleptonB_id_,
    const double s_,
    const double mix_cos_
)
  : pdf(pdf_),
    quark_ids(quark_ids_),
    sleptonA_id(sleptonA_id_),
    sleptonB_id(sleptonB_id_),
    s(s_),
    mix_cos(mix_cos_)
{}

///////////////////////
// Private functions //
///////////////////////
double CrossSection::get_ZliAB() {
  const int A = Utils::first_digit(sleptonA_id);
  const int B = Utils::first_digit(sleptonB_id);

  if (A == B && A == 1) {
    return 0.5 * mix_cos*mix_cos - Const::SW2;
  } else if (A == B && A == 2) {
    return 0.5 * (1.0 - mix_cos*mix_cos) - Const::SW2;
  } else {
    return 0.5 * mix_cos * std::sqrt(1.0 - mix_cos*mix_cos);
  }
}

double CrossSection::get_FqliAB(double Q2) {
  double Qq;
  double ZqL;
  double ZqR;
  if (quark_id % 2 == 0) {
    // up-type quark
    Qq = Const::Qu;
    ZqL = Const::ZuL;
    ZqR = Const::ZuR;
  } else {
    // down-type quark
    Qq = Const::Qd;
    ZqL = Const::ZdL;
    ZqR = Const::ZdR;
  }
  
  double deltaAB;
  if (sleptonA_id == sleptonB_id) {
    deltaAB = 1.0;
  } else {
    deltaAB = 0.0;
  }

  const double ZliAB = get_ZliAB();
  const double cwsw2inv = 1.0 / (Const::SW2 * Const::CW2);
  const double Q2MZ2 = Q2 - Const::MZ2;
  const double propagator2inv = 1.0 / (Q2MZ2*Q2MZ2 + Const::MZ2 * Const::GAMMAZ2);
  const double term1 = Qq*Qq * deltaAB;
  const double term2 = -2.0*Qq*deltaAB * ZliAB*cwsw2inv 
                        * (ZqL+ZqR) * Q2*Q2MZ2*propagator2inv;
  const double term3 = 2.0 * ZliAB*ZliAB*cwsw2inv*cwsw2inv
                        * (ZqL*ZqL + ZqR*ZqR) * Q2*Q2*propagator2inv;
  
  return term1 + term2 + term3;
}

double CrossSection::born_xsec(double q2) {
  const double q5 = q2*q2 * std::sqrt(q2);
  const double mA2 = mA*mA;
  const double mB2 = mB*mB;
  const double m2diff = mA2-mB2;

  // squared 3-momentum in slepton RF
  const double mom2 = 0.25*q2 - 0.5*(mA2+mB2) + 0.25*m2diff*m2diff / q2;
  const double mom3 = std::sqrt(mom2) * mom2;
  
  const double FqliAB = get_FqliAB(q2);
  
  const double xsec = Const::BORN_PREFAC * mom3 / (s * q5) * FqliAB;

  return xsec;
}


////////////////
// Integrands //
////////////////
int CrossSection::integrand_LO_x1_Q(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
  double Q2_min = self->Q2_min;
  double Q2_max = self->Q2_max;
  double s = self->s;
  int quark_id = self->quark_id;
  double muF2 = self->muF2;
  const LHAPDF::PDF* pdf = self->pdf;
  
  double jacobian_Q2 = Q2_max - Q2_min;
  double Q2 = Q2_min + jacobian_Q2 * xx[0];
  self->set_Q2(Q2);

  double tau = self->tau;
  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian_x1 = x1_end - x1_start;
  double x1 = x1_start + jacobian_x1 * xx[1];
  double x2 = tau / x1;
  
  double weight = self->w_LO(1.0);
  
  const double jacobian = jacobian_Q2 * jacobian_x1;
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
  
  const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
  const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);
  
  const double born = self->born_xsec(Q2);
  
  // Factor 2 to account for changing which particle is (anti-)quark
  ff[0] = 2.0 * born * jacobian * xfq * xfqbar / (x1 * tau) * weight;
  
  return 0;
}
int CrossSection::integrand_hadron_x1_Q(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
  double Q2_min = self->Q2_min;
  double Q2_max = self->Q2_max;
  double s = self->s;
  int quark_id = self->quark_id;
  double muF2 = self->muF2;
  const LHAPDF::PDF* pdf = self->pdf;
  
  double jacobian_Q2 = Q2_max - Q2_min;
  double Q2 = Q2_min + jacobian_Q2 * xx[0];
  self->set_Q2(Q2);
  double tau = self->tau;

  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian_x1 = x1_end - x1_start;
  double x1 = x1_start + jacobian_x1 * xx[1];
  double x2 = tau / x1;
  const double jacobian = jacobian_Q2 * jacobian_x1;
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
  
  const double z = 1.0;
  const double w_soft = self->w_hadron_soft(z);
  const double w_plus_1 = self->w_hadron_plus_1(z);
  const double w_plus_log = self->w_hadron_plus_log(z);
  const double F1 = log(1.0 - tau/x1);
  const double Flog = 0.5*F1*F1;
  
  const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
  const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);
  
  const double born = self->born_xsec(Q2);
  
  // Factor 2 to account for changing which particle is (anti-)quark
  ff[0] = 2.0 * born * jacobian * xfq * xfqbar / (x1 * tau) * (w_soft + w_plus_1*F1 + w_plus_log*Flog);

  return 0;
}
int CrossSection::integrand_hadron_x1_x2_Q(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
  double Q2_min = self->Q2_min;
  double Q2_max = self->Q2_max;
  double s = self->s;
  int quark_id = self->quark_id;
  double muF2 = self->muF2;
  const LHAPDF::PDF* pdf = self->pdf;
  
  double jacobian_Q2 = Q2_max - Q2_min;
  double Q2 = Q2_min + jacobian_Q2 * xx[0];
  self->set_Q2(Q2);
  double tau = self->tau;

  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian_x1 = x1_end - x1_start;
  double x1 = x1_start + jacobian_x1 * xx[1];

  const double x2_start = tau/x1;
  const double x2_end = 1.0;
  const double jacobian_x2 = x2_end - x2_start;
  double x2 = x2_start + jacobian_x2 * xx[2];
  
  const double jacobian = jacobian_Q2 * jacobian_x1 * jacobian_x2;
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
  
  const double z = tau/(x1*x2);
  const double w_rad = self->w_hadron_rad(z);
  const double w_plus_1 = self->w_hadron_plus_1(z);
  const double w_plus_log = self->w_hadron_plus_log(z);
  const double w_plus_1_one = self->w_hadron_plus_1(1.0);
  const double w_plus_log_one = self->w_hadron_plus_log(1.0);
  
  const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
  const double xfqbar_x2 = pdf->xfxQ2(-quark_id, x2, muF2);
  const double xfqbar_tau_x1 = pdf->xfxQ2(-quark_id, x2_start, muF2);
  
  const double born = self->born_xsec(Q2);

  // Remember we are using xf, not f for PDFs. Taking this into account we have
  // a common factor 1/x2 in the following terms that we include in ff[0] after
  const double rad_term = xfqbar_x2 * w_rad;
  
  const double f1_term = xfqbar_x2 * w_plus_1 - xfqbar_tau_x1 * w_plus_1_one;
  const double flog_term = xfqbar_x2 * w_plus_log - xfqbar_tau_x1 * w_plus_log_one;

  const double f1 = 1.0 / (1.0 - z);
  const double flog = log(1.0 - z) / (1.0 - z);
  
  const double f_term = f1_term * f1 + flog_term * flog;
  
  // Factor 2 to account for changing which particle is (anti-)quark
  ff[0] = 2.0 * born * jacobian * xfq / (x1*x1 * x2*x2) * (rad_term + f_term);

  return 0;
}
int CrossSection::integrand_slepton_x1_Q(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
  double Q2_min = self->Q2_min;
  double Q2_max = self->Q2_max;
  double s = self->s;
  int quark_id = self->quark_id;
  double muF2 = self->muF2;
  const LHAPDF::PDF* pdf = self->pdf;
  
  double jacobian_Q2 = Q2_max - Q2_min;
  double Q2 = Q2_min + jacobian_Q2 * xx[0];
  self->set_Q2(Q2);
  double tau = self->tau;

  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian_x1 = x1_end - x1_start;
  double x1 = x1_start + jacobian_x1 * xx[1];
  double x2 = tau / x1;
  const double jacobian = jacobian_Q2 * jacobian_x1;
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
  
  const double z = 1.0;
  const double w_soft = self->w_slepton_soft(z);
  const double w_plus_1 = self->w_slepton_plus_1(z);
  const double F1 = log(1.0 - tau/x1);
  
  const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
  const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);
  
  const double s_parton = Q2/z;
  const double born = self->born_xsec(s_parton);
  
  // Factor 2 to account for changing which particle is (anti-)quark
  ff[0] = 2.0 * born * jacobian * xfq * xfqbar / (x1 * tau) * (w_soft + w_plus_1*F1);

  return 0;
}
int CrossSection::integrand_slepton_x1_x2_Q(
    const int* ndim,
    const cubareal xx[],
    const int* ncomp,
    cubareal ff[],
    void* userdata
) {
  CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
  double Q2_min = self->Q2_min;
  double Q2_max = self->Q2_max;
  double s = self->s;
  int quark_id = self->quark_id;
  double muF2 = self->muF2;
  const LHAPDF::PDF* pdf = self->pdf;
  
  double jacobian_Q2 = Q2_max - Q2_min;
  double Q2 = Q2_min + jacobian_Q2 * xx[0];
  self->set_Q2(Q2);
  double tau = self->tau;

  const double x1_start = tau;
  const double x1_end = 1.0;
  const double jacobian_x1 = x1_end - x1_start;
  double x1 = x1_start + jacobian_x1 * xx[1];

  const double x2_start = tau/x1;
  const double x2_end = 1.0;
  const double jacobian_x2 = x2_end - x2_start;
  double x2 = x2_start + jacobian_x2 * xx[2];
  
  const double jacobian = jacobian_Q2 * jacobian_x1 * jacobian_x2;
  
  // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
  const double tol = 1e-10;
  if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
  if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
  
  const double z = tau/(x1*x2);
  const double w_rad = self->w_slepton_rad(z);
  const double w_plus_1 = self->w_slepton_plus_1(z);
  const double w_plus_1_one = self->w_slepton_plus_1(1.0);
  
  const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
  const double xfqbar_x2 = pdf->xfxQ2(-quark_id, x2, muF2);
  const double xfqbar_tau_x1 = pdf->xfxQ2(-quark_id, x2_start, muF2);
  
  const double s_parton = Q2/z;
  const double born = self->born_xsec(s_parton);

  // Remember we are using xf, not f for PDFs. Taking this into account we have
  // a common factor 1/x2 in the following terms that we include in ff[0] after
  const double rad_term = xfqbar_x2 * w_rad;
  
  const double f1_term = xfqbar_x2 * w_plus_1 - xfqbar_tau_x1 * w_plus_1_one;
  const double f1 = 1.0 / (1.0 - z);
  const double f_term = f1_term * f1;
  
  // Factor 2 to account for changing which particle is (anti-)quark
  ff[0] = 2.0 * born * jacobian * xfq / (x1*x1 * x2*x2) * (rad_term + f_term);

  return 0;
}


// Sleptonside integrals
double CrossSection::I_virt_real(double z) {
  const double m12 = mB*mB;
  const double m22 = mA*mA;
  const double s_hat = Q2/z;
  const double lambda_inv = 1.0 / Utils::Kallen(s_hat, m22, m12);
  const double m_sum = m12 + m22;
  const double m_diff = m12 - m22;

  const std::complex<double> Bm1 = B0(m12, 0.0, m12);
  const std::complex<double> Bm2 = B0(m22, 0.0, m22);
  // const std::complex<double> Bsm12 = B0(s_hat, m12, m22);
  // const std::complex<double> Csm12 = C0(m12, m22, s_hat, m12, 0.0, m22);
  // const std::complex<double> term1 = -(s_hat - m_sum) * C0(m12, m22, s_hat, m12, 0.0, m22);
  const std::complex<double> term2 = 0.5 * Bm1 + 0.5 * Bm2;
  // const std::complex<double> term3 = - 2.0*s_hat*(s_hat - m_sum)*lambda_inv * B0(s_hat, m12, m22);
  const std::complex<double> term4 = 2.0*m12*(s_hat - m_diff)*lambda_inv * Bm1;
  const std::complex<double> term5 = 2.0*m22*(s_hat + m_diff)*lambda_inv * Bm2;
  const std::complex<double> term1 = 0.0;
  // const std::complex<double> term2 = 0.0;
  const std::complex<double> term3 = 0.0;
  // const std::complex<double> term4 = 0.0;
  // const std::complex<double> term5 = 0.0;

  const double res = Re(term1 + term2 + term3 + term4 + term5);
  return res;
}
double CrossSection::I_emission_1() {
  const double mt12 = mB*mB/Q2;
  const double mt22 = mA*mA/Q2;
  const double mt_1_sum = 1.0 - mt12 - mt22;
  const double lambda_sqrt = sqrt(Utils::Kallen(1.0, mt12, mt22));

  const double term1 = -mt_1_sum * log((mt_1_sum - lambda_sqrt)/(2.0 * sqrt(mt12*mt22)));
  const double term2 = -lambda_sqrt;
  return term1 + term2;
}
double CrossSection::I_emission_2() {
  const double mt12 = mB*mB/Q2;
  const double mt22 = mA*mA/Q2;
  const double lambda = Utils::Kallen(1.0, mt12, mt22);
  const double lambda_sqrt = sqrt(lambda);
  const double xm = mt22 - mt12 - lambda_sqrt;
  const double xp = mt22 - mt12 + lambda_sqrt;
  
  const double arg_dilog1 = (1.0-xp)/(1.0-xm);
  const double arg_dilog2 = (1.0+xm)/(1.0+xp);
  
  const std::complex<double> dilog1 = Utils::safe_Li2(arg_dilog1);
  const std::complex<double> dilog2 = Utils::safe_Li2(arg_dilog2);
  const std::complex<double> bracket_dilog = dilog1 + dilog2;

  
  const double tol = 1e-10;
  const double bracket_Li2_Im = Im(bracket_dilog);
  const double bracket_Li2_Re = Re(bracket_dilog);

  if (std::abs(bracket_Li2_Im) > tol) {
    std::cout << "Warning: non-zero imaginary part encountered in I_emission_2:\n"
              << "    bracket_Li2_Im = " << bracket_Li2_Im << std::endl;
  }

  const double log_xpxm = log((1.0 + xp)/(1.0 + xm));
  const double log_mxm = log(1.0 - xm);
  const double log_pxm = log(1.0 + xm);
  const double bracket_noLi2 = -M_PI*M_PI/3.0 + 0.5*log_xpxm*log_xpxm + log_mxm*log_mxm
                          - log_pxm*log_pxm + log(2.0*mt12*mt22)*log(mt22/mt12);
  const double term1 = (1.0-mt12-mt22) * (bracket_Li2_Re + bracket_noLi2);
  const double log_xm2_xp2 = log((1.0 - xm*xm)/(1.0-xp*xp));
  const double log_xmxp_xmxp = log((1.0-xm)*(1.0+xp)/((1.0+xm)*(1.0-xp)));
  const double term2 = -lambda_sqrt * log(4.0*lambda)
                      + 0.5*(mt12-mt22)*log_xm2_xp2 + 0.5*log_xmxp_xmxp;
  return term1 + term2;
}

// Weights
double CrossSection::w_LO(double z) {
  return 1.0;
}
double CrossSection::w_hadron_soft(double z) {
  double Qq;
  if (quark_id % 2 == 0) {
    // up-type quark
    Qq = Const::Qu;
  } else {
    // down-type quark
    Qq = Const::Qd;
  }
  double res = Const::ALPHA * Qq*Qq * M_1_PI;
  res *= (M_PI*M_PI/3.0 - 4.0 - 1.5 * log(muF2/Q2));
  return res;
}
double CrossSection::w_hadron_rad(double z) {
  double Qq;
  if (quark_id % 2 == 0) {
    // up-type quark
    Qq = Const::Qu;
  } else {
    // down-type quark
    Qq = Const::Qd;
  }
  const double tol = 1e-10;
  double res = 0.0;
  if (std::abs(z - 1.0) > tol) {
    // If z=1, res=0
    res = Const::ALPHA * Qq*Qq * M_1_PI;
    res *= -(1.0 + z*z) * log(z) / (1.0 - z);
  }
  return res;
}
double CrossSection::w_hadron_plus_1(double z) {
  double Qq;
  if (quark_id % 2 == 0) {
    // up-type quark
    Qq = Const::Qu;
  } else {
    // down-type quark
    Qq = Const::Qd;
  }
  double res = Const::ALPHA * Qq*Qq * M_1_PI;
  res *= -(1.0 + z*z) * log(muF2/Q2);
  return res;
}
double CrossSection::w_hadron_plus_log(double z) {
  double Qq;
  if (quark_id % 2 == 0) {
    // up-type quark
    Qq = Const::Qu;
  } else {
    // down-type quark
    Qq = Const::Qd;
  }
  double res = Const::ALPHA * Qq*Qq * M_1_PI;
  res *= 2.0 * (1.0 + z*z);
  return res;
}
double CrossSection::w_slepton_soft(double z) {
  const double mt12 = mB*mB/Q2;
  const double mt22 = mA*mA/Q2;
  const double I1 = I_emission_1();
  const double I2 = I_emission_2();
  const double Iv_real = I_virt_real(z);
  const double lambda = Utils::Kallen(1.0, mt12, mt22);
  const double lambda_sqrt_inv = 1.0/sqrt(lambda);
  
  double res = Const::ALPHA * M_1_PI;
  res *= Iv_real - (log(4.0*lambda) + log(muF2/Q2))*lambda_sqrt_inv * I1
        + lambda_sqrt_inv * I2;
  return res;
}
double CrossSection::w_slepton_rad(double z) {
  const double mt12 = mB*mB/Q2;
  const double mt22 = mA*mA/Q2;
  const double lambda = Utils::Kallen(1.0, mt12, mt22);
  const double lambda_sqrt = sqrt(lambda);
  const double lambda_z = Utils::Kallen(1.0, z*mt12, z*mt22);
  const double lambda_z_sqrt = sqrt(lambda_z);

  double res = Const::ALPHA * M_1_PI;
  res *= 2.0 * (1.0 - z) * lambda_sqrt / (lambda_z * lambda_z_sqrt);
  return res;
}
double CrossSection::w_slepton_plus_1(double z) {
  const double mt12 = mB*mB/Q2;
  const double mt22 = mA*mA/Q2;
  const double lambda_z = Utils::Kallen(1.0, z*mt12, z*mt22);
  const double I1 = I_emission_1();

  double res = Const::ALPHA * M_1_PI;
  res *= 2.0 * z / sqrt(lambda_z) * I1;
  return res;
}


//////////////////////
// Public functions //
//////////////////////
void CrossSection::set_masses(double mA_, double mB_) {
  mA = mA_;
  if (std::isnan(mB_)) mB = mA_;
  else mB = mB_;
  double muF = 0.5 * (mA + mB);
  muF2 = muF*muF;
}
void CrossSection::set_Q2(double Q2_) {
  Q2 = Q2_;
  tau = Q2/s;
}


double CrossSection::full_xsec(
    int subset, // 0=LO, 1=Hadronside, 2=Sleptonside
    double epsrel,
    double epsabs,
    double maxeval
) {
  double m_tot = mA+mB;
  Q2_min = m_tot*m_tot;
  Q2_max = s;
  
  double xsec = 0.0;
  for (int quark_id_ : quark_ids) {
    quark_id = quark_id_;
    if (subset == 0) {
      double integral[1], error[1], prob[1];
      Utils::integrate_vegas(2, 1, integrand_LO_x1_Q, this, epsrel, epsabs,
                            maxeval, integral, error, prob);
      xsec += integral[0];
    } else if (subset == 1) {
      // Integral over x1:
      double integral1[1], error1[1], prob1[1];
      Utils::integrate_vegas(2, 1, integrand_hadron_x1_Q, this, epsrel, epsabs,
                            maxeval, integral1, error1, prob1);
      xsec += integral1[0];
      
      // Integral over x1 and x2:
      double integral2[1], error2[1], prob2[1];
      Utils::integrate_vegas(3, 1, integrand_hadron_x1_x2_Q, this, epsrel, epsabs,
                            maxeval, integral2, error2, prob2);
      xsec += integral2[0];
    } else if (subset == 2) {
      // Integral over x1:
      double integral1[1], error1[1], prob1[1];
      Utils::integrate_vegas(2, 1, integrand_slepton_x1_Q, this, epsrel, epsabs,
                            maxeval, integral1, error1, prob1);
      xsec += integral1[0];
      
      // Integral over x1 and x2:
      double integral2[1], error2[1], prob2[1];
      Utils::integrate_vegas(3, 1, integrand_slepton_x1_x2_Q, this, epsrel, epsabs,
                            maxeval, integral2, error2, prob2);
      xsec += integral2[0];

    }
  }
  
  return xsec;
}
