#ifndef __Integration_h__
#define __Integration_h__

#include <iostream>

namespace Integration {
  double rect_sum(std::vector<double> x, std::vector<double> y);
  double trapezoid(std::vector<double> x, std::vector<double> y);
  void test();
};

#endif