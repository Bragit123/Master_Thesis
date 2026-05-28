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

mass_arrs_lo = []
sigma_arrs_lo = []
mass_arrs_nlo_hadron = []
sigma_arrs_nlo_hadron = []
mass_arrs_nlo_slepton = []
sigma_arrs_nlo_slepton = []
mass_arrs_nlo = []
sigma_arrs_nlo = []
for sid in slepton_ids:
  ### LO ###
  try:
    filename_lo = "sigma_lo_" + str(sid) + ".dat"
    filepath_lo = OUTPUT_DIR/filename_lo
    m_lo, sigma_lo = np.loadtxt(filepath_lo, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filepath_lo}.")
  
  # Convert from GeV^(-2) to fb
  sigma_lo *= gev_to_fb
  mass_arrs_lo.append(m_lo)
  sigma_arrs_lo.append(sigma_lo)

  ### NLO Hadronside ###
  try:
    filename_nlo_hadron = "sigma_nlo_hadron_" + str(sid) + ".dat"
    filepath_nlo_hadron = OUTPUT_DIR/filename_nlo_hadron
    m_hadron, sigma_hadron = np.loadtxt(filepath_nlo_hadron, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filepath_nlo_hadron}.")
  
  # Convert from GeV^(-2) to fb
  sigma_hadron *= gev_to_fb
  mass_arrs_nlo_hadron.append(m_hadron)
  sigma_arrs_nlo_hadron.append(sigma_hadron)
  
  ### NLO Sleptonside ###
  try:
    filename_nlo_slepton = "sigma_nlo_slepton_" + str(sid) + ".dat"
    filepath_nlo_slepton = OUTPUT_DIR/filename_nlo_slepton
    m_slepton, sigma_slepton = np.loadtxt(filepath_nlo_slepton, unpack=True)
  except:
    raise FileNotFoundError(f"No file with name {filepath_nlo_slepton}.")
  
  # Convert from GeV^(-2) to fb
  sigma_slepton *= gev_to_fb
  mass_arrs_nlo_slepton.append(m_slepton)
  sigma_arrs_nlo_slepton.append(sigma_slepton)

  if not (np.all(m_hadron==m_slepton)):
    raise ValueError("m_hadron and m_slepton must be equal")
  
  mass_arrs_nlo.append(m_slepton)
  sigma_arrs_nlo.append(sigma_hadron + sigma_slepton)


################################
## Plot cross section vs mass ##
################################
plt.figure()
plt.title("Slepton production | $\\sqrt{s}=13$TeV")
plt.xlabel("$m_{\\tilde \\ell_i}$ [GeV]")
plt.ylabel("$\\sigma$ [fb]")

all_mass_arrs = mass_arrs_lo + mass_arrs_nlo_hadron + mass_arrs_nlo_slepton + mass_arrs_nlo
all_sigma_arrs = sigma_arrs_lo + sigma_arrs_nlo_hadron + sigma_arrs_nlo_slepton + sigma_arrs_nlo

slepton_labels = [
  "$\\tilde e_L \\tilde e_L^*$ (LO)",
  "$\\tilde e_R \\tilde e_R^*$ (LO)",
  "$\\tilde e_L \\tilde e_L^*$ (NLO Hadronside)",
  "$\\tilde e_R \\tilde e_R^*$ (NLO Hadronside)",
  "$\\tilde e_L \\tilde e_L^*$ (NLO Sleptonside)",
  "$\\tilde e_R \\tilde e_R^*$ (NLO Sleptonside)",
  "$\\tilde e_L \\tilde e_L^*$ (NLO)",
  "$\\tilde e_R \\tilde e_R^*$ (NLO)"
]
colors = ["blue", "green", "blue", "green", "blue", "green", "blue", "green"]
line_styles = ["solid", "solid", "dashed", "dashed", "dotted", "dotted", "dashdot", "dashdot"]

# My data
for m, sigma, color, style, label in zip(all_mass_arrs, all_sigma_arrs, colors, line_styles, slepton_labels):
  plt.plot(m, sigma, color=color, linestyle=style, marker=".", label=label)

plt.yscale("log")
plt.tight_layout()
plt.legend()
plt.savefig(PLOT_DIR / "xsec_lo_nlo.pdf")


####################################
## Plot ratio cern/mycode vs mass ##
####################################
plt.figure()
plt.title("Ratio $\\sigma^{\\text{NLO}}_{\\text{q}} / \\sigma^{\\text{LO}}$ | $\\sqrt{s}=13$TeV")
plt.xlabel("$m_{\\tilde \\ell_i}$ [GeV]")
plt.ylabel("$\\sigma^{\\text{NLO}} / \\sigma^{\\text{LO}}$")

slepton_labels = [
  "$\\tilde e_L \\tilde e_L^*$ (NLO)",
  "$\\tilde e_R \\tilde e_R^*$ (NLO)",
  "$\\tilde e_L \\tilde e_L^*$ (NLO Sleptonside)",
  "$\\tilde e_R \\tilde e_R^*$ (NLO Sleptonside)",
  "$\\tilde e_L \\tilde e_L^*$ (NLO Hadronside)",
  "$\\tilde e_R \\tilde e_R^*$ (NLO Hadronside)"
]
colors = ["blue", "green", "blue", "green", "blue", "green"]
line_styles = ["solid", "solid", "dashed", "dashed", "dotted", "dotted"]
ratio = [
  (sigma_arrs_nlo[0]) / sigma_arrs_lo[0],
  (sigma_arrs_nlo[1]) / sigma_arrs_lo[1],
  (sigma_arrs_nlo_slepton[0]) / sigma_arrs_lo[0],
  (sigma_arrs_nlo_slepton[1]) / sigma_arrs_lo[1],
  (sigma_arrs_nlo_hadron[0]) / sigma_arrs_lo[0],
  (sigma_arrs_nlo_hadron[1]) / sigma_arrs_lo[1]
]

for m_arr_lo, m_arr_nlo_hadron, m_arr_nlo_slepton, m_arr_nlo in zip(mass_arrs_lo, mass_arrs_nlo_hadron, mass_arrs_nlo_slepton, mass_arrs_nlo):
  assert np.all(m_arr_lo == m_arr_nlo_hadron), "Masses of LO and NLO do not match."

# My data
for m_arr, ratio, color, style, label in zip(all_mass_arrs, ratio, colors, line_styles, slepton_labels):
  plt.plot(m_arr, ratio, color=color, linestyle=style, marker=".", label=label)

plt.tight_layout()
plt.legend()
plt.savefig(PLOT_DIR / "xsec_ratio.pdf")