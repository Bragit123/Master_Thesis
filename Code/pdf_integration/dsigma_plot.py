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

Q_arrs = []
dsigma_arrs = []
for sid in slepton_ids:
  try:
    filename = "output/dsigma_lo_" + str(sid) + ".dat"
    Q, dsigma = np.loadtxt(filename, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filename}.")
  
  Q_arrs.append(Q)
  dsigma *= gev_to_fb
  dsigma_arrs.append(dsigma)

plt.figure()
plt.title("LO slepton production | $\\sqrt{s}=13$TeV | $m_{\\tilde \\ell_i} = 100$GeV")
plt.xlabel("$Q$ [GeV]")
plt.ylabel("$\\frac{d\\sigma}{dQ^2}$ [$\\text{fb}/(\\text{GeV})^2$]")

for Q, dsigma, slabel in zip(Q_arrs, dsigma_arrs, slepton_labels):
  plt.plot(Q, dsigma, label=slabel)

plt.xscale("log")
plt.tight_layout()
plt.legend()
plt.savefig("dsigma.pdf")