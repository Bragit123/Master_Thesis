#ifndef __Random_h__
#define __Random_h__

#include <random>
#include <optional>

namespace Random {
  extern std::mt19937 mt;

  /**
   * @brief Set the RNG seed. If called with no argument, it uses
   * std::random_device() to set the seed.
   * @param seed Optional. Seed defaults to std::random_device().
   */
  void set_seed(std::optional<int> seed = std::nullopt);
  
  /**
   * @brief Creates a random double in the range [min, max)
   * @param min Lower bound.
   * @param max Upper bound.
   * @return Random double in the range [min, max)
   */
  double uniform_double(double min, double max);
}

#endif