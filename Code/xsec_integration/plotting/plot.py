from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

FILE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FILE_DIR.parent / "output"
PLOT_DIR = FILE_DIR / "plots"

STYLE_FILE = FILE_DIR/"thesis.mplstyle"
plt.style.use(STYLE_FILE)
mpl.rcParams["text.usetex"] = True
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=plt.cm.Dark2.colors)
# plt.rcParams["axes.prop_cycle"] = plt.cycler(color=plt.cm.Set2.colors)
# print(plt.colormaps())

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











################
### ONLY QED ###
################
## Load QED data
qed_col_names = ["mass", "lo", "nlo", "hadron", "slepton"]
slepton_ids = [1000011, 2000011]
dfs_qed = []

for slepton_id in slepton_ids:
    filename = "xsec_mass_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")

    dfs_qed.append(df)

## Plot total xsec
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
ax.set_yscale("log")
for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df = dfs_qed[i]
    m_arr = df["mass"]
    xsec_lo = df["lo"]
    xsec_nlo = df["nlo"]
    label = id2label(sid)
    ax.plot(m_arr, xsec_nlo, linestyle="solid", marker="x", label=label+" (NLO)")
    ax.plot(m_arr, xsec_lo, linestyle="dashed", marker=".", label=label+" (LO)")
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95,0.95), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_over_mass.pdf")

## Plot K-factor (xsec/xsecLO) and separate contributions
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")
for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df = dfs_qed[i]
    m_arr = df["mass"]
    xsec_lo = df["lo"]
    K_nlo = df["nlo"]/xsec_lo
    K_hadron = df["hadron"]/xsec_lo
    K_slepton = df["slepton"]/xsec_lo
    label = id2label(sid)
    marker = "." if i==0 else "x"
    linestyle = "solid" if i==0 else "dashed"
    plt.gca().set_prop_cycle(None)
    ax.plot(m_arr, K_nlo, linestyle=linestyle, marker=marker, label=label+" (NLO)")
    ax.plot(m_arr, K_hadron, linestyle=linestyle, marker=marker, label=label+" (IS only)")
    ax.plot(m_arr, K_slepton, linestyle=linestyle, marker=marker, label=label+" (FS only)")
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.85, 0.65), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_Kfactor.pdf")






# ########################
# ### Scale Dependence ###
# ########################
# col_names = ["scale", "lo", "nlo", "hadron", "slepton"]

# scale_slepton_id = 1000011
# # scale_masses = [100, 500]
# scale_mass = 100
# scales = ["R", "F"]
# dfs_scale = []
# for scale in scales:
#     filename = "xsec_scale" + scale + "_m" + str(scale_mass) + "_" + str(scale_slepton_id) + ".dat"
#     filepath = OUTPUT_DIR/filename
#     df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
#     dfs_scale.append(df)

# ## Plot
# fig, axs = plt.subplots(
#     nrows=2,
#     ncols=1,
#     sharex=True,
#     figsize=(fig_width, fig_width/1.3)
# )
# axs[1].set_xlabel("$\\mu/m_{\\tilde{e}_L}$")

# for axi in axs:
#     # axi.set_ylabel("$\\sigma/\\sigma(\\mu_0)$")
#     axi.set_ylabel("$\\sigma/\\sigma_{\\mu_0}$")
#     axi.set_xscale("log", base=2)
#     axi.xaxis.set_major_formatter(ScalarFormatter())

# for i in range(len(scales)):
#     sid = scale_slepton_id
#     df = dfs_scale[i]
#     mu_arr = df["scale"]
    
#     xsec_lo = df["lo"]
#     xsec_nlo = df["nlo"]
#     xsec_hadron = df["hadron"]
#     xsec_slepton = df["slepton"]
    
#     ind0 = np.argwhere(mu_arr==1).item()
#     xsec_lo_0 = xsec_lo[ind0]
#     xsec_nlo_0 = xsec_nlo[ind0]
#     xsec_hadron_0 = xsec_hadron[ind0]
#     xsec_slepton_0 = xsec_slepton[ind0]
#     ratio_lo = xsec_lo/xsec_lo_0
#     ratio_nlo = xsec_nlo/xsec_nlo_0
#     ratio_hadron = xsec_hadron/xsec_hadron_0
#     ratio_slepton = xsec_slepton/xsec_slepton_0
#     marker = "."
#     label = id2label(sid)
#     if i==0:
#         axs[i].plot(mu_arr, ratio_nlo, linestyle="solid", marker=marker, label=f"NLO")
#         axs[i].plot(mu_arr, ratio_lo, linestyle="dashed", marker=marker, label=f"LO")
#         # axs[i].plot(mu_arr, ratio_hadron, linestyle="dashed", marker=marker, label=f"NLO initial-state")
#         # axs[i].plot(mu_arr, ratio_slepton, linestyle="dashed", marker=marker, label=f"NLO final-state")
#     else:
#         axs[i].plot(mu_arr, ratio_nlo, linestyle="solid", marker=marker)
#         axs[i].plot(mu_arr, ratio_lo, linestyle="dashed", marker=marker)
#         # axs[i].plot(mu_arr, ratio_hadron, linestyle="dashed", marker=marker)
#         # axs[i].plot(mu_arr, ratio_slepton, linestyle="dashed", marker=marker)

# box_dict = {
#     "boxstyle": "round",
#     "facecolor": "wheat",
#     "alpha": 0.2
# }
# axs[0].text(0.3, 0.994, "$\\mu_R = \\mu$\n$\\mu_F = m_{\\tilde{e}_L}$", bbox=box_dict)
# axs[1].text(0.3, 1, "$\\mu_R = m_{\\tilde{e}_L}$\n$\\mu_F = \\mu$", bbox=box_dict)

# fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.6, 1.1), ncol=2)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/f"xsec_scale_ratio_m{scale_mass}.pdf")


########################
### Scale Dependence ###
########################
col_names = ["scale", "lo", "nlo", "hadron", "slepton"]

scale_slepton_id = 1000011
masses = [50, 100, 500, 1000]
# scale_mass = 100
# scales = ["R", "F"]
dfs_mass = []
for mass in masses:
    filename = "xsec_scaleF_m" + str(mass) + "_" + str(scale_slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
    dfs_mass.append(df)

## Plot
rows = 2
cols = 2
fig, axs = plt.subplots(
    nrows=rows,
    ncols=cols,
    sharex=True,
    sharey=True,
    figsize=(fig_width, fig_width/1.3),
    layout="constrained"
)
# axs[1].set_xlabel("$\\mu_F/m_{\\tilde{e}_L}$")
fig.supxlabel("$\\mu_F/m_{\\tilde{e}_L}$")
fig.supylabel("$\\sigma(\\mu_F)/\\sigma(\\mu_0)$")

for axi in axs.flatten():
    # axi.set_ylabel("$\\sigma/\\sigma(\\mu_0)$")
    # axi.set_ylabel("$\\sigma(\\mu_F)/\\sigma(\\mu_0)$")
    axi.set_xscale("log", base=2)
    axi.xaxis.set_major_formatter(ScalarFormatter())

for i, mass in enumerate(masses):
    r = i // cols
    c = i % rows
    sid = scale_slepton_id
    df = dfs_mass[i]
    mu_arr = df["scale"]
    
    xsec_lo = df["lo"]
    xsec_nlo = df["nlo"]
    xsec_hadron = df["hadron"]
    xsec_slepton = df["slepton"]
    
    ind0 = np.argwhere(mu_arr==1).item()
    xsec_lo_0 = xsec_lo[ind0]
    xsec_nlo_0 = xsec_nlo[ind0]
    xsec_hadron_0 = xsec_hadron[ind0]
    xsec_slepton_0 = xsec_slepton[ind0]
    ratio_lo = xsec_lo/xsec_lo_0
    ratio_nlo = xsec_nlo/xsec_nlo_0
    ratio_hadron = xsec_hadron/xsec_hadron_0
    ratio_slepton = xsec_slepton/xsec_slepton_0
    label = id2label(sid)
    if i==0:
        # axs[i].plot(mu_arr, ratio_nlo, linestyle="solid", marker="x", label=f"NLO")
        # axs[i].plot(mu_arr, ratio_lo, linestyle="dashed", marker=".", label=f"LO")
        axs[r,c].plot(mu_arr, ratio_nlo, linestyle="solid", marker="x", label=f"NLO")
        axs[r,c].plot(mu_arr, ratio_lo, linestyle="dashed", marker=".", label=f"LO")
    else:
        axs[r,c].plot(mu_arr, ratio_nlo, linestyle="solid", marker="x")
        axs[r,c].plot(mu_arr, ratio_lo, linestyle="dashed", marker=".")
    
    box_dict = {
        "boxstyle": "round",
        "facecolor": "wheat",
        "alpha": 0.2
    }
    # axs[i].text(mu_arr[0], 1, "$m_{\\tilde{e}_L} = " + str(mass) + "$", bbox=box_dict)
    
    # Place textbox displaying mass to the left and furthest away from the graph
    txtboxy = 1.25 if (np.abs(1.25-ratio_nlo[0]) > np.abs(0.75-ratio_nlo[0])) else 0.75
    axs[r,c].text(mu_arr[0], txtboxy, "$m_{\\tilde{e}_L} = " + str(mass) + "$", bbox=box_dict)

# axs[0].text(0.3, 0.994, "$\\mu_R = \\mu$\n$\\mu_F = m_{\\tilde{e}_L}$", bbox=box_dict)
# axs[1].text(0.3, 1, "$\\mu_R = m_{\\tilde{e}_L}$\n$\\mu_F = \\mu$", bbox=box_dict)

fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 1.05), ncol=2)
# fig.tight_layout()
fig.savefig(PLOT_DIR/f"xsec_muF_ratio.pdf")










#############################
### Xsec with Scale Error ###
#############################
col_names = [
    "mass", "lo", "lo_scale_minus", "lo_scale_plus", "nlo", "nlo_scale_minus", "nlo_scale_plus"
]
slepton_ids = [1000011, 2000011]
dfs = []
for slepton_id in slepton_ids:
    filename = "xsec_mass_scale_err_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
    dfs.append(df)

fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\text{LO}}$")
# ax.set_yscale("log")
for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df = dfs[i]
    
    m_arr = df["mass"]
    xsec_lo = df["lo"]
    xsec_nlo = df["nlo"]
    
    # scale_err_lo = df["lo_scale_err"]
    # scale_err_nlo = df["nlo_scale_err"]
    lo_scale_minus = df["lo_scale_minus"]
    lo_scale_plus = df["lo_scale_plus"]
    nlo_scale_minus = df["nlo_scale_minus"]
    nlo_scale_plus = df["nlo_scale_plus"]
    
    K_central = xsec_nlo/xsec_lo
    K_minus = nlo_scale_minus/lo_scale_minus
    K_plus = nlo_scale_plus/lo_scale_plus
    
    Ks = [K_central, K_minus, K_plus]
    K_max = np.maximum.reduce(Ks)
    K_min = np.minimum.reduce(Ks)
    
    # ratio = xsec_nlo/xsec_lo
    # ratio_err = ratio * np.sqrt((scale_err_lo/xsec_lo)**2 + (scale_err_nlo/xsec_nlo)**2)
    
    # ratio = scale_err_nlo/xsec_nlo
    # ratio_err = 0
    # ratio = xsec_nlo/(xsec_nlo-xsec_lo)
    # ratio_err = np.abs(xsec_nlo * xsec_lo/(xsec_nlo-xsec_lo)**2) * np.sqrt((scale_err_lo/xsec_lo)**2 + (scale_err_nlo/xsec_nlo)**2)
    
    # color = ("blue" if i==0 else "green")
    linestyle = ("solid" if i==0 else "dashed")
    marker = ("." if i==0 else "x")


    label = id2label(sid)
    # plt.plot(m_arr, ratio, color=color, linestyle="solid", marker=marker, label=label)
    if i == 1:
        err_label = "Scale Errors"
    else:
        err_label = None

    # ax.plot(m_arr, scale_err_lo/xsec_lo, marker=marker, linestyle=linestyle, label="LO")
    # ax.plot(m_arr, scale_err_nlo/xsec_nlo, marker=marker, linestyle=linestyle, label="NLO")
    # ax.plot(m_arr, scale_err_ratio, marker=marker, linestyle=linestyle, label="Ratio")
    # ax.plot(m_arr, ratio, marker=marker, linestyle=linestyle, label="ratio")
    # error_plot(ax, m_arr, ratio, scale_err_ratio, linestyle=linestyle, marker=marker, label=label, err_label=err_label)
    line, = ax.plot(m_arr, K_central, marker=".", label=label)
    ax.fill_between(m_arr, K_min, K_max, linestyle="dashed", color=line.get_color(), alpha=0.3)
    # line, = ax.plot(m_arr, ratio, label=label)
    # ax.fill_between(m_arr, ratio-ratio_err, ratio+ratio_err, linestyle="dashed", color=line.get_color(), alpha=0.1)
fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_scale_err_ratio.pdf")




###########################
### Xsec with PDF Error ###
###########################
col_names = [
    "mass", "lo", "lo_pdf_err", "nlo", "nlo_pdf_err"
]
slepton_ids = [1000011, 2000011]
dfs = []
for slepton_id in slepton_ids:
    filename = "xsec_mass_pdf_err_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
    dfs.append(df)

fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$")
ax.set_yscale("log")
for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df = dfs[i]
    
    m_arr = df["mass"]
    xsec_lo = df["lo"]
    xsec_nlo = df["nlo"]
    
    lo_pdf_err = df["lo_pdf_err"]
    nlo_pdf_err = df["nlo_pdf_err"]

    label = id2label(sid)
    
    line, = ax.plot(m_arr, xsec_nlo, marker=".", label=label)
    ax.fill_between(m_arr, xsec_nlo - nlo_pdf_err, xsec_nlo + nlo_pdf_err, linestyle="dotted", color=line.get_color(), alpha=0.3)
    # line, = ax.plot(m_arr, ratio, label=label)
    # ax.fill_between(m_arr, ratio-ratio_err, ratio+ratio_err, linestyle="dashed", color=line.get_color(), alpha=0.1)
fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_pdf_err.pdf")










########################
### Xsec with Errors ###
########################
col_names = [
    "mass",
    "lo", "lo_scale_minus", "lo_scale_plus", "lo_pdf_err",
    "nlo", "nlo_scale_minus", "nlo_scale_plus", "nlo_pdf_err"
]
slepton_ids = [1000011, 2000011]
dfs = []
for slepton_id in slepton_ids:
    # filename = "xsec_mass_err_" + str(slepton_id) + ".dat"
    filename = "xsec_mass_err_1e-3_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
    dfs.append(df)

fig, axs = plt.subplots(
    nrows=2,
    ncols=1,
    sharex=True,
    figsize=(fig_width, fig_width/1.3),
    gridspec_kw={"height_ratios": [3,1]}
)
axs[1].set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
axs[0].set_ylabel("$\\sigma$")
axs[1].set_ylabel("$\\delta\\sigma^{\\mathrm{PDF}}/\\sigma$")
axs[0].set_yscale("log")
for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df = dfs[i]
    
    m_arr = df["mass"]
    xsec_lo = df["lo"]
    xsec_nlo = df["nlo"]
    
    lo_scale_minus = df["lo_scale_minus"]
    lo_scale_plus = df["lo_scale_plus"]
    nlo_scale_minus = df["nlo_scale_minus"]
    nlo_scale_plus = df["nlo_scale_plus"]
    
    lo_pdf_err = df["lo_pdf_err"]
    nlo_pdf_err = df["nlo_pdf_err"]
    
    lo_pdf_err_rel = lo_pdf_err/xsec_lo
    nlo_pdf_err_rel = nlo_pdf_err/xsec_nlo

    label = id2label(sid)
    
    nlo_line, = axs[0].plot(m_arr, xsec_nlo, linestyle="solid", marker=".", label=label+" (NLO)")
    axs[0].fill_between(m_arr, nlo_scale_minus, nlo_scale_plus, linestyle="dashed", color=nlo_line.get_color(), alpha=0.3)
    axs[0].fill_between(m_arr, xsec_nlo - nlo_pdf_err, xsec_nlo + nlo_pdf_err, linestyle="dotted", color=nlo_line.get_color(), alpha=0.3)
    
    lo_line, = axs[0].plot(m_arr, xsec_lo, linestyle="dashed", marker=".", label=label+" (LO)")
    axs[0].fill_between(m_arr, lo_scale_minus, lo_scale_plus, linestyle="dashed", color=lo_line.get_color(), alpha=0.3)
    axs[0].fill_between(m_arr, xsec_lo - lo_pdf_err, xsec_lo + lo_pdf_err, linestyle="dotted", color=lo_line.get_color(), alpha=0.3)
    
    axs[1].plot(m_arr, nlo_pdf_err_rel, linestyle="solid", marker=".", color=nlo_line.get_color())
    axs[1].plot(m_arr, lo_pdf_err_rel, linestyle="dashed", marker=".", color=lo_line.get_color())
    # line, = ax.plot(m_arr, ratio, label=label)
    # ax.fill_between(m_arr, ratio-ratio_err, ratio+ratio_err, linestyle="dashed", color=line.get_color(), alpha=0.1)
fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.65, 0.95), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_err.pdf")














#####################
### Load QCD data ###
#####################
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



###################
### QED and QCD ###
###################
## Plot K-factor (xsec/xsecLO) and separate contributions
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")
# for i in range(len(slepton_ids)):
for i in range(1):
    sid = slepton_ids[i]
    df_qed = dfs_qed[i]
    df_qcd = dfs_nlpll[i]
    
    m_qed_arr = df_qed["mass"]
    xsec_qed_lo = df_qed["lo"]
    K_qed_nlo = df_qed["nlo"]/xsec_qed_lo
    
    m_qcd_arr = df_qcd["mass"]
    xsec_qcd_lo = df_qcd["lo"]
    xsec_qcd_resum = df_qcd["resum"]
    
    K_qcd = xsec_qcd_resum/xsec_qcd_lo
    K_scale_plus = df_qcd["resum_scale_plus"]/df_qcd["lo_scale_plus"]
    K_scale_minus = df_qcd["resum_scale_minus"]/df_qcd["lo_scale_minus"]
    
    K_scales = [K_qcd, K_scale_plus, K_scale_minus]
    K_scale_min = np.minimum.reduce(K_scales)
    K_scale_max = np.maximum.reduce(K_scales)
    
    # K_pdf_plus = (df_qcd["resum"] + df_qcd["resum_pdf"])/(df_qcd["lo"] + df_qcd["lo_pdf"])
    # K_pdf_minus = (df_qcd["resum"] - df_qcd["resum_pdf"])/(df_qcd["lo"] - df_qcd["lo_pdf"])
    
    # K_pdfs = [K_qcd, K_pdf_plus, K_pdf_minus]
    # K_pdf_min = np.minimum.reduce(K_pdfs)
    # K_pdf_max = np.maximum.reduce(K_pdfs)
    
    label = id2label(sid)
    marker = "." if i==0 else "x"
    linestyle = "solid" if i==0 else "dashed"
    plt.gca().set_prop_cycle(None)
    ax.plot(m_qed_arr, K_qed_nlo, linestyle=linestyle, marker=marker, label=label+" (NLO QED)")
    qcd_line, = ax.plot(m_qcd_arr, K_qcd, linestyle=linestyle, marker=marker, label=label+" (QCD NLO+LP NLL+NLP LL)")
    # ax.fill_between(m_qcd_arr, K_qcd - dK_scale_plus, K_qcd + dK_scale_plus, linestyle="dashed", alpha=0.2, color=qcd_line.get_color())
    # ax.fill_between(m_qcd_arr, K_qcd - dK_scale_minus, K_qcd + dK_scale_minus, linestyle="dotted", alpha=0.2, color=qcd_line.get_color())
    ax.fill_between(m_qcd_arr, K_scale_min, K_scale_max, linestyle="dashed", alpha=0.2, color=qcd_line.get_color())
    # ax.fill_between(m_qcd_arr, K_pdf_min, K_pdf_max, linestyle="dotted", alpha=0.2, color=qcd_line.get_color())
fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.85, 0.55), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_Kfactor_qed_qcd.pdf")


###############
### QED/QCD ###
###############
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
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
    ax.text(80, 0.032, "$\\alpha Q_q^2 / (\\alpha_s C_F) \\sim 0.025$")
    ax.axhline(0.1, color="black", linestyle="dotted")
    ax.text(450, 0.105, "$\\alpha/\\alpha_s \\sim 0.1$")

fig.legend(frameon=False, loc="center", bbox_to_anchor=(0.55, 0.45), ncol=2)

fig.tight_layout()
fig.savefig(PLOT_DIR/"ratio_qed_qcd.pdf")


#############################
### NLO QED vs QCD Errors ###
#############################
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")

for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df_qed = dfs_qed[i]
    df_lpnll = dfs_lpnll[i]
    df_nlpll = dfs_nlpll[i]

    qed_nlo_only = df_qed["nlo"] - df_qed["lo"]
    qed_hadron_only = df_qed["hadron"] - df_qed["lo"]
    qed_slepton_only = df_qed["slepton"] - df_qed["lo"]
    
    qcd_lo = df_nlpll["lo"]
    qcd_resum = df_nlpll["resum"]

    # ratio_qed = qed_nlo_only / qcd_resum
    # qcd_pdf_rel_err = df_nlpll["resum_pdf"] / qcd_resum
    # qcd_scale_rel_err = (df_nlpll["resum_scale_plus"] - df_nlpll["resum_scale_minus"]) / qcd_resum
    ratio_qed = qed_nlo_only / qcd_lo
    ratio_qcd = qcd_resum / qcd_lo
    qcd_pdf_rel_err = df_nlpll["resum_pdf"] / qcd_lo
    qcd_scale_rel_err = (df_nlpll["resum_scale_plus"] - df_nlpll["resum_scale_minus"]) / qcd_lo

    linestyle = "solid" if i==0 else "dashed"
    marker = "x" if i==0 else "."

    sid_label = id2label(sid)
    # qed_label = f"QED ({sid_label})"
    # pdf_label = f"PDF ({sid_label})"
    # scale_label = f"Scale ({sid_label})"
    qed_label = "$\\sigma^{\\mathrm{NLO}}_{\\mathrm{QED}}$" + f" ({sid_label})"
    pdf_label = "$\\delta\\sigma^{\\mathrm{PDF}}$" + f" ({sid_label})"
    scale_label = "$\\delta\\sigma^{\\mu}$" + f" ({sid_label})"
    
    # plt.gca().set_prop_cycle(None)
    ax.plot(df_qed["mass"], ratio_qed, marker=marker, label=qed_label, linestyle=linestyle)
    ax.plot(df_qed["mass"], qcd_pdf_rel_err, marker=marker, label=pdf_label, linestyle=linestyle)
    ax.plot(df_qed["mass"], qcd_scale_rel_err, marker=marker, label=scale_label, linestyle=linestyle)

fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.2, 0.9), ncol=2)

fig.tight_layout()
fig.savefig(PLOT_DIR/"ratio_qed_qcdnlo.pdf")