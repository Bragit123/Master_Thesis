#include "Integration.h"


namespace Integration {
  double rect_sum(std::vector<double> x, std::vector<double> y) {
    
    const int N = x.size();
    if (y.size() != N) {
      std::cerr << "x and y must have the same length." << std::endl;
      std::exit(1);
    }
    
    double sum = 0;

    for (int i=1; i < N; ++i) {
      double dx = x.at(i) - x.at(i-1);
      sum += y.at(i) * dx;
    }

    return sum;
  }

  double trapezoid(std::vector<double> x, std::vector<double> y) {

    const int N = x.size();
    if (y.size() != N) {
      std::cerr << "x and y must have the same length." << std::endl;
      std::exit(1);
    }

    double sum = 0;

    for (int i=1; i < N; ++i) {
      double dx = x.at(i) - x.at(i-1);
      sum += (y.at(i) + y.at(i-1)) * dx / 2;
    }

    return sum;
  }

  void test() {
    // Quadratic y=3x^2 from 0 to 1
    int N = 101;
    double dx = 0.01;
    std::vector<double> x(N);
    std::vector<double> y(N);
    for (int i=0; i < N; ++i) {
      x[i] = (double) i * dx;
      y[i] = 3 * x[i]*x[i];
    }

    double analytical_res = 1.0;
    double rect_res = Integration::rect_sum(x, y);
    double trap_res = Integration::trapezoid(x, y);

    std::cout << "rect_sum:   " << rect_res << std::endl;
    std::cout << "trapezoid:  " << trap_res << std::endl;
    std::cout << "Analytical: " << analytical_res << std::endl;
  }
}