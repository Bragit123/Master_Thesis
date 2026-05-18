from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

FILE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FILE_DIR.parent / "output"
PLOT_DIR = FILE_DIR / "plots"

gev_to_fb = 0.389379e12 # https://en.wikipedia.org/wiki/Barn_(unit)

slepton_ids = [1000011, 2000011]

mass_arrs = []
sigma_arrs = []
for sid in slepton_ids:
  try:
    filename = "sigma_lo_" + str(sid) + ".dat"
    filepath = OUTPUT_DIR/filename
    m, sigma = np.loadtxt(filepath, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filepath}.")
  
  ## Convert from GeV^(-2) to fb
  sigma *= gev_to_fb
  mass_arrs.append(m)
  sigma_arrs.append(sigma)

cern_mass_arrs = []
cern_sigma_arrs = []
for sid in slepton_ids:
  try:
    filename = "cern_data/cern_" + str(sid) + ".txt"
    filepath = OUTPUT_DIR/filename
    m, sigma = np.loadtxt(filepath, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filepath}.")
  
  sigma *= 1e3 # pb -> fb
  cern_mass_arrs.append(m)
  cern_sigma_arrs.append(sigma)


################################
## Plot cross section vs mass ##
################################
plt.figure()
plt.title("LO slepton production | $\\sqrt{s}=13$TeV")
plt.xlabel("$m_{\\tilde \\ell_i}$ [GeV]")
plt.ylabel("$\\sigma$ [fb]")

all_mass_arrs = mass_arrs + cern_mass_arrs
all_sigma_arrs = sigma_arrs + cern_sigma_arrs
slepton_labels = [
  "$\\tilde e_L \\tilde e_L^*$ (My code)",
  "$\\tilde e_R \\tilde e_R^*$ (My code)",
  "$\\tilde e_L \\tilde e_L^*$ (CERN: NLO-NLL)",
  "$\\tilde e_R \\tilde e_R^*$ (CERN: NLO-NLL)"
]
colors = ["blue", "green", "blue", "green"]
line_styles = ["solid", "solid", "dashed", "dashed"]

# My data
for m, sigma, color, style, label in zip(all_mass_arrs, all_sigma_arrs, colors, line_styles, slepton_labels):
  plt.plot(m, sigma, color=color, linestyle=style, marker=".", label=label)

plt.yscale("log")
plt.tight_layout()
plt.legend()
plt.savefig(PLOT_DIR / "sigma.pdf")


####################################
## Plot ratio cern/mycode vs mass ##
####################################
plt.figure()
plt.title("Ratio $\\sigma_{\\text{NLO-NLL}}^{\\text{CERN}} / \\sigma_{\\text{LO}}^{\\text{mycode}}$ | $\\sqrt{s}=13$TeV")
plt.xlabel("$m_{\\tilde \\ell_i}$ [GeV]")
plt.ylabel("$\\sigma^{\\text{CERN}} / \\sigma^{\\text{mycode}}$")

slepton_labels = [
  "$\\tilde e_L \\tilde e_L^*$",
  "$\\tilde e_R \\tilde e_R^*$"
]
colors = ["blue", "green"]
line_styles = ["solid", "solid"]
ratio = [
  cern_sigma_arrs[0] / sigma_arrs[0],
  cern_sigma_arrs[1] / sigma_arrs[1]
]

for m_arr, cern_m_arr in zip(mass_arrs, cern_mass_arrs):
  assert np.all(m_arr == cern_m_arr), "Masses of mycode and CERN do not match."

# My data
for m_arr, ratio, color, style, label in zip(mass_arrs, ratio, colors, line_styles, slepton_labels):
  plt.plot(m, ratio, color=color, linestyle=style, marker=".", label=label)

plt.tight_layout()
plt.legend()
plt.savefig(PLOT_DIR / "ratio_sigma.pdf")