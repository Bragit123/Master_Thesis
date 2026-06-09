from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# sns.set_theme()


FILE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FILE_DIR.parent / "output"
PLOT_DIR = FILE_DIR / "plots"

def id2label(id: int) -> str:
  if id == 1000011:
    return "$\\tilde{e}_L^*\\tilde{e}_L$"
  if id == 2000011:
    return "$\\tilde{e}_R^*\\tilde{e}_R$"
  else:
    print(f"WARNING: Unrecognized particle ID: {id}")
    return ""

def error_plot(x, y, yerr, color=None, linestyle=None, marker=None, label=None, alpha=0.5, err_label=None):
  line, = plt.plot(x, y, color=color, linestyle=linestyle, marker=marker, label=label)
  plt.fill_between(x, y - yerr, y + yerr, color=line.get_color(), alpha=alpha, label=err_label, linestyle="dashed")

col_names = [
  "mass", "lo", "scale_err_lo", "nlo", "scale_err_nlo"
]
slepton_ids = [1000011, 2000011]
dfs = []
for slepton_id in slepton_ids:
  filename = "xsec_mass_scale_err_" + str(slepton_id) + ".dat"
  filepath = OUTPUT_DIR/filename
  df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
  dfs.append(df)


##################
### LO and NLO ###
##################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
ax.set_yscale("log")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df = dfs[i]
  m_arr = df["mass"]
  xsec_lo = df["lo"]
  xsec_nlo = df["nlo"]
  scale_err_lo = df["scale_err_lo"]
  scale_err_nlo = df["scale_err_nlo"]
  # color = ("blue" if i==0 else "green")
  marker = ("o" if i==0 else "x")
  marker = ("o" if i==0 else "x")
  # marker = "."
  label = id2label(sid)

  if i == 1:
    err_label = "Scale Errors"
  else:
    err_label = None

  error_plot(m_arr, xsec_lo, scale_err_lo, marker=marker, label=label+" (LO)")
  error_plot(m_arr, xsec_nlo, scale_err_nlo, marker=marker, label=label+" (NLO)", err_label=err_label)
ax.grid(alpha=0.3)
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_mass_scale_err_lo_nlo.pdf")


####################
### NLO/LO Ratio ###
####################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\text{LO}}$")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df = dfs[i]
  m_arr = df["mass"]
  xsec_lo = df["lo"]
  xsec_nlo = df["nlo"]
  scale_err_nlo = df["scale_err_nlo"]
  ratio = xsec_nlo/xsec_lo
  # color = ("blue" if i==0 else "green")
  # marker = ("o" if i==0 else "x")
  marker = "."
  label = id2label(sid)
  # plt.plot(m_arr, ratio, color=color, linestyle="solid", marker=marker, label=label)
  if i == 1:
    err_label = "Scale Errors"
  else:
    err_label = None

  error_plot(m_arr, ratio, scale_err_nlo, marker=marker, label=label, err_label=err_label)
fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=3)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_mass_scale_err_ratio.pdf")