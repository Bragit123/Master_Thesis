import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

try:
  filename = "output/dsigma_lo_1000011.dat"
  QL, dsigmaL = np.loadtxt(filename, unpack=True)
  filename = "output/dsigma_lo_2000011.dat"
  QR, dsigmaR = np.loadtxt(filename, unpack=True)
except:
  raise FileNotFoundError(f"No file with name {filename}.")

plt.figure()
plt.title("LO $\\tilde e_{L/R}$ production | $\\sqrt{s}=13$TeV | $m_{\\tilde e_{L/R}} = 100$GeV")
plt.xlabel("$Q$ [GeV]")
plt.ylabel("$\\frac{d\\sigma}{dQ^2}$ [(GeV)$^{-4}$]")
plt.plot(QL, dsigmaL, label="$\\tilde e_L \\tilde e_L^*$")
plt.plot(QR, dsigmaR, label="$\\tilde e_R \\tilde e_R^*$")
plt.xscale("log")
plt.tight_layout()
plt.legend()
plt.savefig("dsigma.pdf")