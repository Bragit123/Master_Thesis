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

col_names = [
  "scale", "lo", "nlo", "hadron", "slepton"
]
slepton_ids = [1000011, 2000011]
dfs = []
for slepton_id in slepton_ids:
  filename = "xsec_scale_" + str(slepton_id) + ".dat"
  filepath = OUTPUT_DIR/filename
  df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
  dfs.append(df)


##################
### LO and NLO ###
##################
fig, ax = plt.subplots()
ax.set_xlabel("$\\mu_F/m_{\\tilde\\ell}$")
ax.set_ylabel("$\\sigma$ [fb]")
# ax.set_yscale("log")
# ax.set_xscale("log")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df = dfs[i]
  mu_arr = df["scale"]
  xsec_lo = df["lo"]
  xsec_nlo = df["nlo"]
  # color = ("blue" if i==0 else "green")
  marker = ("o" if i==0 else "x")
  # marker = "."
  label = id2label(sid)

  plt.plot(mu_arr, xsec_lo, linestyle="solid", marker=marker, label=label+" (LO)")
  plt.plot(mu_arr, xsec_nlo, linestyle="solid", marker=marker, label=label+" (NLO)")

ax.grid(alpha=0.3)
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_scale_lo_nlo.pdf")


#########################
### (LO+NLO)/LO Ratio ###
#########################
fig, ax = plt.subplots()
ax.set_xlabel("$\\mu_F/m_{\\tilde\\ell}$")
ax.set_ylabel("$\\sigma/\\sigma^{\\text{LO}}$")
# ax.set_xscale("log")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df = dfs[i]
  mu_arr = df["scale"]
  xsec_lo = df["lo"]
  xsec_nlo = df["nlo"]
  ratio = xsec_nlo/xsec_lo
  # ratio = df["ratio"]
  # color = ("blue" if i==0 else "green")
  # marker = ("o" if i==0 else "x")
  marker = "."
  label = id2label(sid)
  plt.plot(mu_arr, ratio, linestyle="solid", marker=marker, label=label)

fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=3)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_scale_ratio.pdf")


#######################
### Hadron--Slepton ###
#######################
fig, ax = plt.subplots()
ax.set_xlabel("$\\mu_F/m_{\\tilde\\ell}$")
ax.set_ylabel("$\\sigma$ [fb]")
# ax.set_yscale("log")
# ax.set_xscale("log")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df = dfs[i]
  mu_arr = df["scale"]
  xsec_hadron = df["hadron"]
  xsec_slepton = df["slepton"]
  xsec_nlo = df["nlo"]
  # marker = ("o" if i==0 else "x")
  marker = "."
  label = id2label(sid)
  plt.plot(mu_arr, xsec_nlo, linestyle="solid", marker=marker, label=label+" (NLO)")
  plt.plot(mu_arr, xsec_slepton, linestyle="solid", marker=marker, label=label+" (Sleptonside)")
  plt.plot(mu_arr, xsec_hadron, linestyle="dashed", marker=marker, label=label+" (Hadronside)")
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_scale_hadron_slepton.pdf")
