from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

FILE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FILE_DIR.parent / "output"
PLOT_DIR = FILE_DIR / "plots"

mpl.rcParams["text.usetex"] = True
STYLE_FILE = FILE_DIR/"thesis.mplstyle"
plt.style.use(STYLE_FILE)

# Get font sizes to fit document nicely (https://duetosymmetry.com/code/latex-mpl-fig-tips/)
pt = 1/72.27
fig_width = 0.8 * 418.25368 * pt
golden_ratio = (1 + np.sqrt(5)) / 2

def id2label(id: int) -> str:
  if id == 1000011:
    return "$\\tilde{e}_L^*\\tilde{e}_L$"
  if id == 2000011:
    return "$\\tilde{e}_R^*\\tilde{e}_R$"
  else:
    print(f"WARNING: Unrecognized particle ID: {id}")
    return ""

## Load QED data
qed_col_names = ["mass", "lo", "nlo", "hadron", "slepton"]
slepton_ids = [1000011, 2000011]
dfs_qed = []

for slepton_id in slepton_ids:
  filename = "xsec_mass_" + str(slepton_id) + ".dat"
  filepath = OUTPUT_DIR/filename
  df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")
  
  dfs_qed.append(df)


## Load QCD data
qcd_col_names = [
  "mass", "lo", "lo_scale_plus", "lo_scale_minus", "lo_pdf", "lo_alphas",
  "nlo", "nlo_scale_plus", "nlo_scale_minus", "nlo_pdf", "nlo_alphas",
  "resum", "resum_scale_plus", "resum_scale_minus", "resum_pdf", "resum_alphas"
]
slepton_names = ["LH", "RH"]
dfs_lpnll = []
dfs_nlpll = []
for slepton_name in slepton_names:
  filename_lpnll = "LHC_total_" + slepton_name + "_LPNLL_PDFerr_Brage.txt"
  filepath_lpnll = OUTPUT_DIR/"qcd_smoking"/filename_lpnll
  df = pd.read_csv(filepath_lpnll, skiprows=1, names=qcd_col_names, delimiter=r"\s+\|\s+", engine="python")
  df.loc[:,df.columns != "mass"] *= 1e3 # pb to fb to match QED results
  dfs_lpnll.append(df)
  
  filename_nlpll = "LHC_total_" + slepton_name + "_LPNLL_NLPLL_PDFerr_Brage.txt"
  filepath_nlpll = OUTPUT_DIR/"qcd_smoking"/filename_nlpll
  df = pd.read_csv(filepath_nlpll, skiprows=1, names=qcd_col_names, delimiter=r"\s+\|\s+", engine="python")
  df.loc[:,df.columns != "mass"] *= 1e3 # pb to fb to match QED results
  dfs_nlpll.append(df)


## Check agreement on LO and NLO QCD
for i in range(len(slepton_ids)):
  qed_lo = np.array(dfs_qed[i]["lo"])
  lpnll_lo = np.array(dfs_lpnll[i]["lo"])
  nlpll_lo = np.array(dfs_nlpll[i]["lo"])
  lpnll_nlo = np.array(dfs_lpnll[i]["nlo"])
  nlpll_nlo = np.array(dfs_nlpll[i]["nlo"])

  print("Left-Handed:" if i==0 else "Right-Handed:")
  print(np.all(np.isclose(lpnll_lo, nlpll_lo)), end=" ")
  print(np.all(np.isclose(lpnll_nlo, nlpll_nlo)))
  print((qed_lo - nlpll_lo)/nlpll_lo)
  print(np.mean((qed_lo - nlpll_lo)/nlpll_lo))
  print()


###################
## Cross section ##
###################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
ax.set_yscale("log")

for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df_qed = dfs_qed[i]
  df_lpnll = dfs_lpnll[i]
  df_nlpll = dfs_nlpll[i]

  label = id2label(sid)
  marker = "o" if i==0 else "x"
  ax.plot(df_qed["mass"], df_qed["nlo"], marker=".", label=label+" (NLO QED)")
  ax.plot(df_lpnll["mass"], df_lpnll["resum"], marker=".", label=label+" (LP NLL QCD)")
  ax.plot(df_nlpll["mass"], df_nlpll["resum"], marker=".", label=label+" (NLP LL QCD)")

fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_qcd_comparison.pdf")


###################
## Ratios NLO/LO ##
###################
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma^{\\mathrm{NLO}}/\\sigma^{\\mathrm{LO}}$")

for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df_qed = dfs_qed[i]
  df_lpnll = dfs_lpnll[i]
  df_nlpll = dfs_nlpll[i]

  ratio_qed = df_qed["nlo"] / df_qed["lo"]
  ratio_hadron = df_qed["hadron"] / df_qed["lo"]
  ratio_slepton = df_qed["slepton"] / df_qed["lo"]
  ratio_lpnll = (df_lpnll["resum"] - df_lpnll["nlo"] + df_lpnll["lo"]) / df_lpnll["lo"]
  ratio_nlpll = (df_nlpll["resum"] - df_nlpll["nlo"] + df_nlpll["lo"]) / df_nlpll["lo"]

  linestyle = "solid" if i==0 else "dashed"
  marker = "." if i==0 else "x"

  label = id2label(sid)
  plt.gca().set_prop_cycle(None)
  ax.plot(df_qed["mass"], ratio_qed, marker=marker, label=label+" (NLO QED)", linestyle=linestyle)
  ax.plot(df_qed["mass"], ratio_hadron, marker=marker, label=label+" (NLO Hadronside)", linestyle=linestyle)
  ax.plot(df_qed["mass"], ratio_slepton, marker=marker, label=label+" (NLO Sleptonside)", linestyle=linestyle)
  ax.plot(df_lpnll["mass"], ratio_lpnll, marker=marker, label=label+" (LP NLL QCD)", linestyle=linestyle)
  ax.plot(df_nlpll["mass"], ratio_nlpll, marker=marker, label=label+" (NLP LL QCD)", linestyle=linestyle)

fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.9, 0.75), ncol=2)

fig.tight_layout()
fig.savefig(PLOT_DIR/"ratio_nlo_lo.pdf")


#############################
## Ratios Corrections only ##
#############################
# fig, ax = plt.subplots(figsize=(fig_width, fig_width/golden_ratio))
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
# ax.set_ylabel("$(\\sigma^{\\mathrm{NLO}}_{\\mathrm{QED}}-\\sigma^{\\mathrm{LO}})/(\\sigma^{\\mathrm{NLO}}_{\\mathrm{QCD}}-\\sigma^{\\mathrm{LO}})$")
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma^{\\mathrm{NLO}}_{\\mathrm{QED}}/\\sigma^{\\mathrm{NLO}}_{\\mathrm{QCD}}$")

for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df_qed = dfs_qed[i]
  df_lpnll = dfs_lpnll[i]
  df_nlpll = dfs_nlpll[i]

  qed_nlo_only = df_qed["nlo"] - df_qed["lo"]
  qed_hadron_only = df_qed["hadron"] - df_qed["lo"]
  qed_slepton_only = df_qed["slepton"] - df_qed["lo"]
  qcd_nlo_only = df_nlpll["nlo"] - df_nlpll["lo"]
  
  ratio_qed = qed_nlo_only / qcd_nlo_only
  ratio_hadron = qed_hadron_only / qcd_nlo_only
  ratio_slepton = qed_slepton_only / qcd_nlo_only

  linestyle = "solid" if i==0 else "dashed"
  marker = "." if i==0 else "x"

  label = id2label(sid)
  plt.gca().set_prop_cycle(None)
  ax.plot(df_qed["mass"], ratio_qed, marker=marker, label=label+" (QED)", linestyle=linestyle)
  ax.plot(df_qed["mass"], ratio_hadron, marker=marker, label=label+" (Hadronside)", linestyle=linestyle)
  ax.plot(df_qed["mass"], ratio_slepton, marker=marker, label=label+" (Sleptonside)", linestyle=linestyle)
  ax.axhline(0.025, color="black", linestyle="dotted")
  ax.text(100, 0.03, "$\\alpha Q_q^2 / (\\alpha_s C_F) \\sim 0.025$")
  ax.axhline(0.1, color="black", linestyle="dotted")
  ax.text(400, 0.105, "$\\alpha/\\alpha_s \\sim 0.1$")

fig.legend(frameon=False, loc="center", bbox_to_anchor=(0.55, 0.45), ncol=2)

fig.tight_layout()
fig.savefig(PLOT_DIR/"ratio_qed_qcd.pdf")


############
## Errors ##
############
fig, ax = plt.subplots()
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("PDF error")

# ax.set_yscale("log")

for i in range(len(slepton_ids)):
  sid = slepton_ids[i]
  df_qed = dfs_qed[i]
  df_lpnll = dfs_lpnll[i]
  df_nlpll = dfs_nlpll[i]
  
  label = id2label(sid)
  
  ax.plot(df_lpnll["mass"], df_lpnll["resum_pdf"]/df_lpnll["resum"], marker=".", label=label+" (NLP LL)")
  ax.plot(df_nlpll["mass"], df_nlpll["resum_pdf"]/df_nlpll["resum"], marker=".", label=label+" (NLP LL)")

fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.15, 0.95), ncol=1)

fig.tight_layout()
fig.savefig(PLOT_DIR/"PDF_err.pdf")
