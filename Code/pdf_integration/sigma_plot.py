import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

gev_to_fb = 0.389379e12 # https://en.wikipedia.org/wiki/Barn_(unit)

slepton_ids = [1000011, 2000011]
slepton_labels = [
  "$\\tilde e_L \\tilde e_L^*$",
  "$\\tilde e_R \\tilde e_R^*$"
]
mass_arrs = []
sigma_arrs = []
for sid in slepton_ids:
  try:
    filename = "output/sigma_lo_" + str(sid) + ".dat"
    m, sigma = np.loadtxt(filename, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filename}.")
  
  ## Convert from GeV^(-2) to pb
  sigma *= gev_to_fb
  mass_arrs.append(m)
  sigma_arrs.append(sigma)


plt.figure()
plt.title("LO slepton production | $\\sqrt{s}=13$TeV")
plt.xlabel("$m_{\\tilde \\ell_i}$ [GeV]")
plt.ylabel("$\\sigma$ [fb]")

for m, sigma, slabel in zip(mass_arrs, sigma_arrs, slepton_labels):
  plt.plot(m, sigma, ".-", label=slabel)

plt.yscale("log")
plt.tight_layout()
plt.legend()
plt.savefig("plots/sigma.pdf")