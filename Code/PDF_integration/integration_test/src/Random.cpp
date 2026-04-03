#include "Random.h"

namespace Random {
  std::random_device rd;
  std::mt19937 mt(rd());

  void set_seed(std::optional<int> seed) {
    if (seed.has_value()) {
      mt.seed(seed.value());
    }
    else {
      mt.seed(std::random_device()());
    }
  }

  double uniform_double(double min, double max) {
    std::uniform_real_distribution<double> dist(min, max);
    return dist(mt);
  }
}