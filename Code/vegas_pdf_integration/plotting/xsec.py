from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

FILE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FILE_DIR.parent / "output"
PLOT_DIR = FILE_DIR / "plots"

# gev_to_fb = 0.389379e12 # https://en.wikipedia.org/wiki/Barn_(unit)

def id2label(id: int) -> str:
  if id == 1000011:
    return "$\\tilde{e}_L^*\\tilde{e}_L$"
  if id == 2000011:
    return "$\\tilde{e}_R^*\\tilde{e}_R$"
  else:
    print(f"WARNING: Unrecognized particle ID: {id}")
    return ""

filename = "xsec_mass.dat"
filepath = OUTPUT_DIR/filename

slepton_ids = [1000011, 2000011]

m_arrs = []
xsec_lo_arrs = []
xsec_nlo_arrs = []
xsec_hadron_arrs = []
xsec_slepton_arrs = []
for slepton_id in slepton_ids:
  filename = "xsec_mass_" + str(slepton_id) + ".dat"
  filepath = OUTPUT_DIR/filename
  m_arr, xsec_lo, xsec_nlo, xsec_hadron, xsec_slepton = np.loadtxt(filepath, unpack=True)
  m_arrs.append(m_arr)
  xsec_lo_arrs.append(xsec_lo)
  xsec_nlo_arrs.append(xsec_nlo)
  xsec_hadron_arrs.append(xsec_hadron)
  xsec_slepton_arrs.append(xsec_slepton)


##################
### LO and NLO ###
##################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
ax.set_yscale("log")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  m = m_arrs[i]
  xsec_lo = xsec_lo_arrs[i]
  xsec_nlo = xsec_nlo_arrs[i]
  color = ("blue" if i==0 else "green")
  marker = ("o" if i==0 else "x")
  label = id2label(sid)
  plt.plot(m_arr, xsec_lo, color=color, linestyle="dashed", marker=marker, label=label+" (LO)")
  plt.plot(m_arr, xsec_nlo, color=color, linestyle="solid", marker=marker, label=label+" (NLO)")
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_mass_lo_nlo.pdf")


####################
### NLO/LO Ratio ###
####################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma^{\\text{NLO}}/\\sigma^{\\text{LO}}$")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  m = m_arrs[i]
  xsec_lo = xsec_lo_arrs[i]
  xsec_nlo = xsec_nlo_arrs[i]
  ratio = xsec_nlo/xsec_lo
  color = ("blue" if i==0 else "green")
  marker = ("o" if i==0 else "x")
  label = id2label(sid)
  plt.plot(m_arr, ratio, color=color, linestyle="solid", marker=marker, label=label)
fig.legend(frameon=False, loc="lower right", bbox_to_anchor=(0.95, 0.2), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_mass_ratio.pdf")


#########################
### (LO+NLO)/LO Ratio ###
#########################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma^{\\text{LO}+\\text{NLO}}/\\sigma^{\\text{LO}}$")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  m = m_arrs[i]
  xsec_lo = xsec_lo_arrs[i]
  xsec_nlo = xsec_nlo_arrs[i]
  ratio = (xsec_nlo+xsec_lo)/xsec_lo
  color = ("blue" if i==0 else "green")
  marker = ("o" if i==0 else "x")
  label = id2label(sid)
  plt.plot(m_arr, ratio, color=color, linestyle="solid", marker=marker, label=label)
fig.legend(frameon=False, loc="lower right", bbox_to_anchor=(0.95, 0.2), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_mass_ratio_full.pdf")


#######################
### Hadron--Slepton ###
#######################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
ax.set_yscale("log")
for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  m = m_arrs[i]
  xsec_hadron = xsec_hadron_arrs[i]
  xsec_slepton = xsec_slepton_arrs[i]
  xsec_nlo = xsec_nlo_arrs[i]
  color = ("blue" if i==0 else "green")
  marker = ("o" if i==0 else "x")
  label = id2label(sid)
  # plt.plot(m_arr, xsec_nlo, color=color, linestyle="solid", marker=marker, label=label+" (NLO)")
  plt.plot(m_arr, xsec_slepton, color=color, linestyle="solid", marker=marker, label=label+" (Sleptonside)")
  plt.plot(m_arr, xsec_hadron, color=color, linestyle="dashed", marker=marker, label=label+" (Hadronside)")
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_mass_hadron_slepton.pdf")
