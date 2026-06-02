#include "Integrands.hpp"

#include "CrossSection.hpp"
#include "Utils.hpp"
#include "clooptools.h"


namespace Integrands {
  int LO_x1_Q(
      const int* ndim, const cubareal xx[], const int* ncomp,
      cubareal ff[], void* userdata
  ) {
    CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
    const double Q2_min = self->Q2_min;
    const double Q2_max = self->Q2_max;
    const double s = self->s;
    const int quark_id = self->quark_id;
    const double muF2 = self->muF2;
    const LHAPDF::PDF* pdf = self->pdf;
    
    const double jacobian_Q2 = Q2_max - Q2_min;
    const double Q2 = Q2_min + jacobian_Q2 * xx[0];
    const double tau = Q2/s;

    const double x1_start = tau;
    const double x1_end = 1.0;
    const double jacobian_x1 = x1_end - x1_start;
    double x1 = x1_start + jacobian_x1 * xx[1];
    double x2 = tau / x1;
    
    const double weight = 1.0;
    
    const double jacobian = jacobian_Q2 * jacobian_x1;
    
    // Making sure x1,x2 max at 1, not 1+eps, so xfxQ2 doesn't reject them:
    const double tol = 1e-10;
    if (std::abs(x1 - 1.0) < tol) x1 = 1.0;
    if (std::abs(x2 - 1.0) < tol) x2 = 1.0;
    
    const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
    const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);
    
    const double born = self->born_xsec(Q2);
    
    // Factor 2 to account for changing which particle is (anti-)quark
    const double result = born * jacobian * xfq * xfqbar / (x1 * tau) * weight;
    ff[0] = Const::GEV_TO_FB * result;
    
    return 0;
  }

  int hadron_x1_Q(
      const int* ndim, const cubareal xx[], const int* ncomp,
      cubareal ff[], void* userdata
  ) {
    CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
    const double Q2_min = self->Q2_min;
    const double Q2_max = self->Q2_max;
    const double s = self->s;
    const int quark_id = self->quark_id;
    const double muF2 = self->muF2;
    const LHAPDF::PDF* pdf = self->pdf;

    const double Qq = Utils::get_Qq(quark_id);
    
    const double jacobian_Q2 = Q2_max - Q2_min;
    const double Q2 = Q2_min + jacobian_Q2 * xx[0];
    const double tau = Q2/s;
    
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
    const double w_prefac = Const::ALPHA * Qq*Qq * M_1_PI;
    const double w_soft = w_prefac * (M_PI*M_PI/3.0 - 4.0 - 1.5 * log(muF2/Q2));
    const double w_plus_1 = -w_prefac * (1.0 + z*z) * log(muF2/Q2);
    const double w_plus_log = w_prefac * 2.0 * (1.0 + z*z);

    const double F1 = log(1.0 - tau/x1);
    const double Flog = 0.5*F1*F1;
    
    const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
    const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);
    
    const double born = self->born_xsec(Q2);
    
    // Factor 2 to account for changing which particle is (anti-)quark
    const double result = born * jacobian * xfq * xfqbar / (x1 * tau) * (w_soft + w_plus_1*F1 + w_plus_log*Flog);
    ff[0] = Const::GEV_TO_FB * result;
    
    return 0;
  }

  int hadron_x1_x2_Q(
      const int* ndim, const cubareal xx[], const int* ncomp,
      cubareal ff[], void* userdata
  ) {
    CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
    const double Q2_min = self->Q2_min;
    const double Q2_max = self->Q2_max;
    const double s = self->s;
    const int quark_id = self->quark_id;
    const double muF2 = self->muF2;
    const LHAPDF::PDF* pdf = self->pdf;

    const double Qq = Utils::get_Qq(quark_id);
    
    const double jacobian_Q2 = Q2_max - Q2_min;
    const double Q2 = Q2_min + jacobian_Q2 * xx[0];
    const double tau = Q2/s;
    
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
    const double w_prefac = Const::ALPHA * Qq*Qq * M_1_PI;
    double w_rad = 0.0;
    if (std::abs(1.0 - z) > tol) {
      w_rad = -w_prefac * (1.0 + z*z) * log(z) / (1.0 - z);
    }
    const double w_plus_1 = -w_prefac * (1.0 + z*z) * log(muF2/Q2);
    const double w_plus_1_one = -w_prefac * 2.0 * log(muF2/Q2); // z=1
    const double w_plus_log = w_prefac * 2.0 * (1.0 + z*z);
    const double w_plus_log_one = w_prefac * 4.0; // z=1
    
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
    const double result = born * jacobian * xfq / (x1*x1 * x2*x2) * (rad_term + f_term);
    ff[0] = Const::GEV_TO_FB * result;
    
    return 0;
  }

  int slepton_x1_Q(
    const int* ndim, const cubareal xx[], const int* ncomp,
    cubareal ff[], void* userdata
  ) {
    CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
    const double Q2_min = self->Q2_min;
    const double Q2_max = self->Q2_max;
    const double s = self->s;
    const int quark_id = self->quark_id;
    const double muF2 = self->muF2;
    const LHAPDF::PDF* pdf = self->pdf;
    
    const double jacobian_Q2 = Q2_max - Q2_min;
    const double Q2 = Q2_min + jacobian_Q2 * xx[0];
    const double tau = Q2/s;
    
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

    const double mB = self->mB;
    const double mA = self->mA;
    const double m12 = mB*mB;
    const double m22 = mA*mA;
    const double m_sum = m12 + m22;
    const double m_diff = m12 - m22;
    const double mt12 = m12/Q2;
    const double mt22 = m22/Q2;
    const double mt_1_sum = 1. - mt12 - mt22;
    const double s_parton = Q2/z;
    const double lambda = Utils::Kallen(1., mt12, mt22);
    const double lambda_s_inv = 1./Utils::Kallen(s_parton, m12, m22);
    const double lambda_sqrt = sqrt(lambda);
    const double lambda_sqrt_inv = 1./lambda_sqrt;
    const double lambda_z_sqrt_inv = 1./sqrt(Utils::Kallen(1., z*mt12, z*mt22));

    const double xm = mt22 - mt12 - lambda_sqrt;
    const double xp = mt22 - mt12 + lambda_sqrt;

    const double log_xpxm = log((1.+xp)/(1.+xm));
    const double log_mxm = log(1.-xm);
    const double log_pxm = log(1.+xm);
    const double log_xm2_xp2 = log((1.-xm*xm)/(1.-xp*xp));
    const double log_xmxp_xmxp = log((1.-xm)*(1.+xp)/((1.+xm)*(1.-xp)));
    const double arg_dilog1 = (1.-xp)/(1.-xm);
    const double arg_dilog2 = (1.+xm)/(1.+xp);

    const std::complex<double> Bm1 = B0(m12, 0., m12);
    const std::complex<double> Bm2 = B0(m22, 0., m22);
    const std::complex<double> Bsm12 = B0(s_parton, m12, m22);
    const std::complex<double> Csm12 = C0(m12, m22, s_parton, m12, 0., m22);

    
    const double I1 = -mt_1_sum * log((mt_1_sum - lambda_sqrt)/(2. * sqrt(mt12*mt22)))
                      - lambda_sqrt;
    const double Iv_real = Re(-(s_parton - m_sum) * Csm12
                              + 0.5 * Bm1 + 0.5 * Bm2
                              - 2.*s_parton*(s_parton - m_sum)*lambda_s_inv * Bsm12
                              + 2.*m12*(s_parton - m_diff)*lambda_s_inv * Bm1
                              + 2.*m22*(s_parton + m_diff)*lambda_s_inv * Bm2);

    const std::complex<double> dilog = Li2(arg_dilog1) + Li2(arg_dilog2);
    const double I2_bracket1 = Re(dilog);
    const double I2_bracket2 = -M_PI*M_PI/3. + 0.5*log_xpxm*log_xpxm + log_mxm*log_mxm
    - log_pxm*log_pxm + log(2.*mt12*mt22)*log(mt22/mt12);
    const double I2 = (1.-mt12-mt22) * (I2_bracket1 + I2_bracket2)
                      -lambda_sqrt * log(4.*lambda)
                      + 0.5 * (mt12-mt22)*log_xm2_xp2
                      + 0.5 * log_xmxp_xmxp;
    
    const double w_prefac = Const::ALPHA * M_1_PI;

    const double w_soft = w_prefac * (Iv_real
                            - (log(4.*lambda) + log(muF2/Q2))*lambda_sqrt_inv * I1
                            + lambda_sqrt_inv * I2);
    const double w_plus_1 = w_prefac * 2. * z * lambda_z_sqrt_inv * I1;
    const double F1 = log(1.0 - tau/x1);
    
    const double xfq = pdf->xfxQ2(quark_id, x1, muF2);
    const double xfqbar = pdf->xfxQ2(-quark_id, x2, muF2);
    
    // const double s_parton = Q2/z;
    const double born = self->born_xsec(s_parton);
    
    // Factor 2 to account for changing which particle is (anti-)quark
    const double result = born * jacobian * xfq * xfqbar / (x1 * tau) * (w_soft + w_plus_1*F1);
    ff[0] = Const::GEV_TO_FB * result;
    
    return 0;
  }

  int slepton_x1_x2_Q(
    const int* ndim, const cubareal xx[], const int* ncomp,
    cubareal ff[], void* userdata
  ) {
    CrossSection* self = static_cast<CrossSection*>(userdata); // Necessary to keep class variables while being compatible with Vegas()
    const double Q2_min = self->Q2_min;
    const double Q2_max = self->Q2_max;
    const double s = self->s;
    const int quark_id = self->quark_id;
    const double muF2 = self->muF2;
    const LHAPDF::PDF* pdf = self->pdf;
    
    const double jacobian_Q2 = Q2_max - Q2_min;
    const double Q2 = Q2_min + jacobian_Q2 * xx[0];
    const double tau = Q2/s;
    
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

    const double mB = self->mB;
    const double mA = self->mA;
    const double mt12 = mB*mB/Q2;
    const double mt22 = mA*mA/Q2;
    const double mt_1_sum = 1. - mt12 - mt22;
    const double lambda = Utils::Kallen(1., mt12, mt22);
    const double lambda_sqrt = sqrt(lambda);
    const double lambda_z_inv = 1./Utils::Kallen(1., z*mt12, z*mt22);
    const double lambda_z_sqrt_inv = sqrt(lambda_z_inv);
    
    const double I1 = -mt_1_sum * log((mt_1_sum - lambda_sqrt)/(2. * sqrt(mt12*mt22)))
                      - lambda_sqrt;

    const double w_prefac = Const::ALPHA * M_1_PI;
    const double w_rad = w_prefac * 2. * (1. - z) * lambda_sqrt * lambda_z_inv * lambda_z_sqrt_inv;
    const double w_plus_1 = w_prefac * 2. * z * lambda_z_sqrt_inv * I1;
    const double w_plus_1_one = w_prefac * 2. * z / lambda_sqrt * I1;
    
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
    const double result = born * jacobian * xfq / (x1*x1 * x2*x2) * (rad_term + f_term);
    ff[0] = Const::GEV_TO_FB * result;
    
    return 0;
  }
}