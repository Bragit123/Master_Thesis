from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.gridspec import GridSpec

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
    # filename = "xsec_mass_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")

    dfs_qed.append(df)

qed_err_col_names = [
    "mass",
    "lo", "lo_scale_minus", "lo_scale_plus", "lo_pdf",
    "nlo", "nlo_scale_minus", "nlo_scale_plus", "nlo_pdf"
]
dfs_err = []
for slepton_id in slepton_ids:
    filename = "xsec_mass_err_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_err_col_names, delimiter=r"\s+")
    
    dfs_err.append(df)

####################
### QED with err ###
####################
fig, (ax, ax_ratio) = plt.subplots(
    nrows=2,
    ncols=1,
    sharex=True,
    figsize=(fig_width, fig_width/1.3),
    gridspec_kw={"height_ratios": [3,1]}
)
ax_ratio.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
ax_ratio.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")
ax.set_yscale("log")
for i, sid in enumerate(slepton_ids):
    sid = slepton_ids[i]
    df = dfs_err[i]
    
    m_arr = df["mass"]
    
    lo = df["lo"]
    lo_scale_minus = df["lo_scale_minus"]
    lo_scale_plus = df["lo_scale_plus"]
    lo_pdf = df["lo_pdf"]
    lo_pdf_minus = lo - lo_pdf
    lo_pdf_plus = lo + lo_pdf
    
    nlo = df["nlo"]
    nlo_scale_minus = df["nlo_scale_minus"]
    nlo_scale_plus = df["nlo_scale_plus"]
    nlo_pdf = df["nlo_pdf"]
    nlo_pdf_minus = nlo - nlo_pdf
    nlo_pdf_plus = nlo + nlo_pdf
    
    label = id2label(sid)
    nlo_line, = ax.plot(m_arr, nlo, linestyle="solid", marker="x", label=label+" (NLO)")
    ax.fill_between(m_arr, nlo_pdf_minus, nlo_pdf_plus, linestyle="dashed", alpha=0.3, color=nlo_line.get_color())
    ax.fill_between(m_arr, nlo_scale_minus, nlo_scale_plus, linestyle="dotted", alpha=0.3, color=nlo_line.get_color())
    lo_line, = ax.plot(m_arr, lo, linestyle="solid", marker=".", label=label+" (LO)")
    ax.fill_between(m_arr, lo_pdf_minus, lo_pdf_plus, linestyle="dashed", alpha=0.3, color=lo_line.get_color())
    ax.fill_between(m_arr, lo_scale_minus, lo_scale_plus, linestyle="dotted", alpha=0.3, color=lo_line.get_color())
    
    lo_pdf_ratio_minus = lo_pdf_minus/lo
    lo_pdf_ratio_plus = lo_pdf_plus/lo
    nlo_pdf_ratio_minus = nlo_pdf_minus/lo
    nlo_pdf_ratio_plus = nlo_pdf_plus/lo
    lo_scale_ratio_minus = lo_scale_minus/lo
    lo_scale_ratio_plus = lo_scale_plus/lo
    nlo_scale_ratio_minus = nlo_scale_minus/nlo
    nlo_scale_ratio_plus = nlo_scale_plus/nlo
    if i==0:
        ax_ratio.plot(m_arr, lo/lo, linestyle=lo_line.get_linestyle(), color=lo_line.get_color())
        ax_ratio.fill_between(m_arr, lo_pdf_ratio_minus, lo_pdf_ratio_plus, linestyle="dashed", alpha=0.2, color=lo_line.get_color())
        ax_ratio.fill_between(m_arr, lo_scale_ratio_minus, lo_scale_ratio_plus, linestyle="dotted", alpha=0.2, color=lo_line.get_color())
        ax_ratio.plot(m_arr, nlo/lo, linestyle=nlo_line.get_linestyle(), color=nlo_line.get_color())
        ax_ratio.fill_between(m_arr, nlo_pdf_ratio_minus, nlo_pdf_ratio_plus, linestyle="dashed", alpha=0.2, color=nlo_line.get_color())
        ax_ratio.fill_between(m_arr, nlo_scale_ratio_minus, nlo_scale_ratio_plus, linestyle="dotted", alpha=0.2, color=nlo_line.get_color())

ax.fill_between([],[],[],color="k",linestyle="dotted", alpha=0.2, label="Scale error")
ax.fill_between([],[],[],color="k",linestyle="dashed", alpha=0.2, label="PDF error")

handles, labels = ax.get_legend_handles_labels()
handles.insert(2, handles.pop())
labels.insert(2, labels.pop())
# leg1 = fig.legend(handles[:4], labels[:4], frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=2)
# leg2 = fig.legend(handles[4:], labels[4:], frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.8), ncol=1)
# fig.add_artist(leg1)

fig.legend(handles=handles, labels=labels, frameon=False, loc="upper right", bbox_to_anchor=(0.97,0.95), ncol=2)
# fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95,0.95), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_over_mass.pdf")
    







########################
### Scale Dependence ###
########################
col_names = ["scale", "lo", "nlo", "hadron", "slepton"]

scale_slepton_id = 1000011

mass_R = 600
filename = "xsec_scaleR_m" + str(mass_R) + "_" + str(scale_slepton_id) + ".dat"
filepath = OUTPUT_DIR/filename
df_R = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")

masses = [400, 600, 800, 1000]
dfs_mass = []
for mass in masses:
    filename = "xsec_scaleF_m" + str(mass) + "_" + str(scale_slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
    dfs_mass.append(df)

## Plot
fig, axs = plt.subplot_mosaic(
    """
    RR
    AB
    CD
    """,
    figsize=(fig_width, fig_width),
    gridspec_kw={"hspace": 0.05, "height_ratios": [1, 2, 2]},
    constrained_layout=True
    # tight_layout=True
)
# fig.get_layout_engine().set(hspace=0.02, wspace=0.02, h_pad=0.02, w_pad=0.02)
axs["A"].sharex(axs["B"])
axs["B"].sharex(axs["C"])
axs["C"].sharex(axs["D"])
axs["A"].sharey(axs["B"])
axs["B"].sharey(axs["C"])
axs["C"].sharey(axs["D"])
for axi in (axs["A"], axs["B"]):
    plt.setp(axi.get_xticklabels(), visible=False)
for axi in (axs["B"], axs["D"]):
    plt.setp(axi.get_yticklabels(), visible=False)

for axi in axs.values():
    axi.set_xscale("log", base=2)
    axi.xaxis.set_major_formatter(ScalarFormatter())

# axs["R"].set_xlabel("$\\mu_R/m_{\\tilde{e}_L}$")
axs["R"].set_xlabel("$\\mu_R/\\mu_0$")
axs["R"].set_ylabel("$\\frac{\\sigma(\\mu_R)}{\\sigma(\\mu_0)}$")

for axi in (axs["A"], axs["C"]):
    axi.set_ylabel("$\\frac{\\sigma(\\mu_F)}{\\sigma(\\mu_0)}$")

for axi in (axs["C"], axs["D"]):
    # axi.set_xlabel("$\\mu_F/m_{\\tilde{e}_L}$")
    axi.set_xlabel("$\\mu_F/\\mu_0$")


mu_R_arr = df_R["scale"]
xsec_R_lo = df_R["lo"]
xsec_R_nlo = df_R["nlo"]

ind0 = np.argwhere(mu_R_arr==1).item()
xsec_R_lo_0 = xsec_R_lo[ind0]
xsec_R_nlo_0 = xsec_R_nlo[ind0]
ratio_R_lo = xsec_R_lo/xsec_R_lo_0
ratio_R_nlo = xsec_R_nlo/xsec_R_nlo_0

axs["R"].plot(mu_R_arr, ratio_R_nlo, linestyle="solid", marker="x")
axs["R"].plot(mu_R_arr, ratio_R_lo, linestyle="dashed", marker=".")

axs["R"].set_ylim(0.95,1.1)
box_dict = {
    "boxstyle": "round",
    "facecolor": "wheat",
    "alpha": 0.2
}
txtboxy = 1.05
axs["R"].text(mu_R_arr[0], txtboxy, "$m_{\\tilde{e}_L} = " + str(mass_R) + "$GeV", bbox=box_dict)

inds = ["A", "B", "C", "D"]
for i, mass in enumerate(masses):
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
    ratio_lo = xsec_lo/xsec_lo_0
    ratio_nlo = xsec_nlo/xsec_nlo_0
    if i==0:
        axs[inds[i]].plot(mu_arr, ratio_nlo, linestyle="solid", marker="x", label=f"NLO")
        axs[inds[i]].plot(mu_arr, ratio_lo, linestyle="dashed", marker=".", label=f"LO")
    else:
        axs[inds[i]].plot(mu_arr, ratio_nlo, linestyle="solid", marker="x")
        axs[inds[i]].plot(mu_arr, ratio_lo, linestyle="dashed", marker=".")
    
    box_dict = {
        "boxstyle": "round",
        "facecolor": "wheat",
        "alpha": 0.2
    }
    
    # Place textbox displaying mass to the left and furthest away from the graph
    txtboxy = 1.25 if (np.abs(1.25-ratio_nlo[0]) > np.abs(0.75-ratio_nlo[0])) else 0.75
    axs[inds[i]].text(mu_arr[0], txtboxy, "$m_{\\tilde{e}_L} = " + str(mass) + "$GeV", bbox=box_dict)

fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 1.05), ncol=2)
fig.savefig(PLOT_DIR/f"xsec_scale_ratio.pdf")






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
    filename = "xsec_mass_err_" + str(slepton_id) + ".dat"
    # filename = "xsec_mass_err_1e-3_" + str(slepton_id) + ".dat"
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





################
### K factor ###
################
## Plot K-factor (xsec/xsecLO) and separate contributions
fig, (ax_qcd, ax) = plt.subplots(
    nrows=2,
    ncols=1,
    sharex=True,
    figsize=(fig_width, fig_width/1.3),
    # figsize=(fig_width, fig_width),
    gridspec_kw={"height_ratios": [1,3]}
)
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")
ax_qcd.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")
for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df_qed = dfs_qed[i]
    df_lpnll = dfs_lpnll[i]
    df_nlpll = dfs_nlpll[i]
    m_arr = df_qed["mass"]
    xsec_lo_qed = df_qed["lo"]
    xsec_lo_qcd = df_nlpll["lo"][2:]
    K_nlo = df_qed["nlo"]/xsec_lo_qed
    K_hadron = df_qed["hadron"]/xsec_lo_qed
    K_slepton = df_qed["slepton"]/xsec_lo_qed
    K_lpnll = (df_lpnll["resum"][2:]-df_lpnll["nlo"][2:]+df_lpnll["lo"][2:])/xsec_lo_qcd
    K_nlpll = (df_nlpll["resum"][2:]-df_nlpll["nlo"][2:]+df_nlpll["lo"][2:])/xsec_lo_qcd
    K_nlo_qcd = df_nlpll["nlo"][2:]/xsec_lo_qcd
    label = id2label(sid)
    marker = "." if i==0 else "x"
    linestyle = "solid" if i==0 else "dashed"
    plt.gca().set_prop_cycle(None)
    # ax.plot(m_arr, K_nlo, linestyle=linestyle, marker=marker, label=label+" (NLO)")
    # ax.plot(m_arr, K_hadron, linestyle=linestyle, marker=marker, label=label+" (IS only)")
    # ax.plot(m_arr, K_slepton, linestyle=linestyle, marker=marker, label=label+" (FS only)")
    # # ax.plot(m_arr, K_lpnll, linestyle=linestyle, marker=marker, label=label+" (QCD LP NLL)")
    # # ax.plot(m_arr, K_nlpll, linestyle=linestyle, marker=marker, label=label+" (QCD NLP LL)")
    # ax.plot(m_arr, K_lpnll, linestyle=linestyle, marker=marker, label=label+" (LP NLL)")
    # ax.plot(m_arr, K_nlpll, linestyle=linestyle, marker=marker, label=label+" (LP NLL + NLP LL)")
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    if i==0:
        ax.plot(m_arr, K_nlo, linestyle=linestyle, marker=marker, color=colors[0], label="NLO QED")
        ax.plot(m_arr, K_hadron, linestyle=linestyle, marker=marker, color=colors[1], label="NLO QED (IS only)")
        ax.plot(m_arr, K_slepton, linestyle=linestyle, marker=marker, color=colors[2], label="NLO QED (FS only)")
        ax_qcd.plot(m_arr, K_nlo_qcd, linestyle=linestyle, marker=marker, color=colors[3], label="NLO QCD")
        ax.plot(m_arr, K_lpnll, linestyle=linestyle, marker=marker, color=colors[4], label="LP NLL")
        ax.plot(m_arr, K_nlpll, linestyle=linestyle, marker=marker, color=colors[5], label="LP NLL + NLP LL")
    else:
        ax.plot(m_arr, K_nlo, linestyle=linestyle, marker=marker, color=colors[0])
        ax.plot(m_arr, K_hadron, linestyle=linestyle, marker=marker, color=colors[1])
        ax.plot(m_arr, K_slepton, linestyle=linestyle, marker=marker, color=colors[2])
        ax_qcd.plot(m_arr, K_nlo_qcd, linestyle=linestyle, marker=marker, color=colors[3])
        ax.plot(m_arr, K_lpnll, linestyle=linestyle, marker=marker, color=colors[4])
        ax.plot(m_arr, K_nlpll, linestyle=linestyle, marker=marker, color=colors[5])
ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
handles, labels = ax.get_legend_handles_labels()
handle_qcd, label_qcd = ax_qcd.get_legend_handles_labels()
handles.insert(3, handle_qcd[0])
labels.insert(3, label_qcd[0])
# leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="lower left", bbox_to_anchor=(0.18, 0.38), ncol=2)
# leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="upper left", bbox_to_anchor=(0.18, 0.42), ncol=2)
# leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="lower left", bbox_to_anchor=(0.18, 0.40), ncol=2)
# leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="upper left", bbox_to_anchor=(0.18, 0.42), ncol=2)
# leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="lower left", bbox_to_anchor=(0.18, 1), ncol=2)
# leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="upper left", bbox_to_anchor=(0.18, 1.04), ncol=2)
# leg1 = fig.legend(handles, labels, frameon=False, loc="upper left", bbox_to_anchor=(0.97, 0.8), ncol=1)
# leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="upper left", bbox_to_anchor=(0.97, 0.9), ncol=1)
# leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="upper left", bbox_to_anchor=(0.97, 0.55), ncol=1)
# leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="upper left", bbox_to_anchor=(0.05, 0.04), ncol=2)
# leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="upper left", bbox_to_anchor=(0.8, 0.04), ncol=1)
leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="lower left", bbox_to_anchor=(0.05, 0.95), ncol=2)
leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="lower left", bbox_to_anchor=(0.8, 0.95), ncol=1)
fig.add_artist(leg1)
# fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.18, 0.77), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_Kfactor.pdf")



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



################################################
### xsec over mass for QED and QCD with errs ###
################################################
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_ylabel("$\\sigma$ [fb]")
# ax.set_yscale("log")
for i, sid in enumerate(slepton_ids):
    df_qed = dfs_qed[i]
    df_qcd = dfs_nlpll[i]
    
    m_qed = df_qed["mass"]
    lo_qed = df_qed["lo"]
    nlo_qed = df_qed["nlo"]
    
    m_qcd = df_qcd["mass"]
    
    lo_qcd = df_qcd["lo"]
    lo_scale_minus = df_qcd["lo_scale_minus"]
    lo_scale_plus = df_qcd["lo_scale_plus"]
    lo_pdf_alphas_err = df_qcd["resum_pdf"] + df_qcd["resum_alphas"]
    
    resum_qcd = df_qcd["resum"]
    scale_minus = df_qcd["resum_scale_minus"]
    scale_plus = df_qcd["resum_scale_plus"]
    pdf_alphas_err = df_qcd["resum_pdf"] + df_qcd["resum_alphas"]
    
    sid_label = id2label(sid)
    if i == 0:
        ax.plot(m_qed, nlo_qed/lo_qed, linestyle="solid", marker="x", label=sid_label+" (NLO QED)")
        
        resum_line, = ax.plot(m_qcd, resum_qcd/lo_qcd, linestyle="solid", marker="x", label=sid_label+" (NLO + LP NLL + NLP LL)")
        # ax.fill_between(m_qcd, scale_minus/lo_qcd, scale_plus/lo_qcd, linestyle="dashed", alpha=0.2, color=resum_line.get_color())
        ax.fill_between(m_qcd, (resum_qcd-pdf_alphas_err)/lo_qcd, (resum_qcd+pdf_alphas_err)/lo_qcd, linestyle="dotted", alpha=0.2, color=resum_line.get_color())
        
        lo_line, = ax.plot(m_qcd, lo_qcd/lo_qcd, linestyle="solid", marker="x", label=sid_label+" (LO)")
        # ax.fill_between(m_qcd, lo_scale_minus/lo_qcd, lo_scale_plus/lo_qcd, linestyle="dashed", alpha=0.2, color=lo_line.get_color())
        ax.fill_between(m_qcd, (lo_qcd-lo_pdf_alphas_err)/lo_qcd, (lo_qcd+lo_pdf_alphas_err)/lo_qcd, linestyle="dotted", alpha=0.2, color=lo_line.get_color())
    
fig.legend(frameon=False, loc="lower left", bbox_to_anchor=(0.4, 0.6), ncol=1)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_qed_qcd.pdf")


###############
### QED/QCD ###
###############
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
ax.set_ylabel("$\\sigma^{\\mathrm{NLO}}_{\\mathrm{QED}}/\\sigma^{\\mathrm{NLO}}_{\\mathrm{QCD}}$")

for i in range(len(slepton_ids)):
    sid = slepton_ids[i]
    df_qed = dfs_qed[i]
    df_lpnll = dfs_lpnll[i]
    df_nlpll = dfs_nlpll[i]

    qed_nlo_only = df_qed["nlo"] - df_qed["lo"]
    qed_hadron_only = df_qed["hadron"] - df_qed["lo"]
    qed_slepton_only = df_qed["slepton"] - df_qed["lo"]
    qcd_nlo_only = np.array(df_nlpll["nlo"][2:] - df_nlpll["lo"][2:])

    ratio_qed = qed_nlo_only / qcd_nlo_only
    ratio_hadron = qed_hadron_only / qcd_nlo_only
    ratio_slepton = qed_slepton_only / qcd_nlo_only

    linestyle = "solid" if i==0 else "dashed"
    marker = "." if i==0 else "x"

    label = id2label(sid)
    plt.gca().set_prop_cycle(None)
    if i == 0:
        ax.plot(df_qed["mass"], ratio_qed, linestyle=linestyle, marker=marker, label="NLO (full)")
        ax.plot(df_qed["mass"], ratio_hadron, linestyle=linestyle, marker=marker, label="NLO (IS only)")
        ax.plot(df_qed["mass"], ratio_slepton, linestyle=linestyle, marker=marker, label="NLO (FS only)")
    else:
        ax.plot(df_qed["mass"], ratio_qed, marker=marker, linestyle=linestyle)
        ax.plot(df_qed["mass"], ratio_hadron, marker=marker, linestyle=linestyle)
        ax.plot(df_qed["mass"], ratio_slepton, marker=marker, linestyle=linestyle)
    ax.axhline(0.025, color="black", linestyle="dotted")
    ax.text(300, 0.032, "$\\alpha Q_q^2 / (\\alpha_s C_F) \\sim 0.025$")
    ax.axhline(0.1, color="black", linestyle="dotted")
    ax.text(300, 0.105, "$\\alpha/\\alpha_s \\sim 0.1$")

ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
handles, labels = ax.get_legend_handles_labels()
# leg1 = fig.legend(handles[:3], labels[:3], frameon=False, loc="upper left", bbox_to_anchor=(0.2, 0.55), ncol=1)
# leg2 = fig.legend(handles[3:], labels[3:], frameon=False, loc="upper left", bbox_to_anchor=(0.5, 0.55), ncol=1)
# fig.add_artist(leg1)
fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.57), ncol=2)

fig.tight_layout()
fig.savefig(PLOT_DIR/"ratio_qed_qcd.pdf")











#######################
### QED vs PDF errs ###
#######################
## Load QED data
qed_col_names = [
    "mass",
    "lo", "lo_scale_minus", "lo_scale_plus", "lo_pdf",
    "nlo", "nlo_scale_minus", "nlo_scale_plus", "nlo_pdf"
]
slepton_ids = [1000011, 2000011]
dfs = []

for slepton_id in slepton_ids:
    filename = "xsec_mass_err_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")

    dfs.append(df)

fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")

for i, sid in enumerate(slepton_ids):
    df = dfs[i]

    mass = np.array(df["mass"])
    lo = np.array(df["lo"])
    # lo_plus_nlo = np.array(df["nlo"])
    # nlo = lo_plus_nlo - lo
    nlo = np.array(df["nlo"]) - np.array(df["lo"])
    pdf_err = np.array(df["lo_pdf"])
    # pdf_plus = lo+pdf_err
    # pdf_minus = lo-pdf_err

    ratio_nlo = nlo/lo
    ratio_pdf = pdf_err/lo
    # ratio_pdf_plus = pdf_plus/lo
    # ratio_pdf_minus = pdf_minus/lo
    
    linestyle = "solid" if i==0 else "dashed"
    marker = "x" if i==0 else "."

    lo_label = "$\\sigma^{\\mathrm{LO}}$"
    qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$"
    pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$"
    # qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$ (" + id2label(sid) + ")"
    # pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$ (" + id2label(sid) + ")"
    
    plt.gca().set_prop_cycle(None)
    if i==0:
        ax.plot(mass, ratio_nlo, marker=marker, linestyle=linestyle, label=qed_label)
        ax.plot(mass, ratio_pdf, marker=marker, linestyle=linestyle, label=pdf_label)
    else:
        ax.plot(mass, ratio_nlo, marker=marker, linestyle=linestyle)
        ax.plot(mass, ratio_pdf, marker=marker, linestyle=linestyle)
        # ax.plot(mass, ratio_nlo, marker=marker, linestyle=linestyle)
        # lo_line, = ax.plot(mass, lo/lo, marker=marker, linestyle=linestyle)
    # line, = ax.plot([],[])
    # if i==0:
    #     plt.fill_between(mass, ratio_pdf_minus, ratio_pdf_plus, linestyle="dashed", color=line.get_color(), alpha=0.2, label=pdf_label)
    # else:
    #     plt.fill_between(mass, ratio_pdf_minus, ratio_pdf_plus, linestyle="dotted", color=line.get_color(), alpha=0.2, label=pdf_label)

# ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
# ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
handles, labels = ax.get_legend_handles_labels()

fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.15, 0.95), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"ratio_qed_pdf.pdf")



########################
### LO me vs smoking ###
########################
qed_col_names = ["mass", "lo", "nlo", "hadron", "slepton"]
slepton_ids = [1000011, 2000011]
dfs_qed1 = []
dfs_qed2 = []
dfs_qed3 = []
dfs_qed4 = []
dfs_qed5 = []

for slepton_id in slepton_ids:
    filename = "xsec_mass1_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")
    dfs_qed1.append(df)
    
    filename = "xsec_mass2_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")
    dfs_qed2.append(df)
    
    filename = "xsec_mass3_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")
    dfs_qed3.append(df)
    
    filename = "xsec_mass4_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")
    dfs_qed4.append(df)
    
    filename = "xsec_mass5_" + str(slepton_id) + ".dat"
    filepath = OUTPUT_DIR/filename
    df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")
    dfs_qed5.append(df)

## Load QED data
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
ax.set_ylabel("Relative error")

for i, sid in enumerate(slepton_ids):
# for i, sid in enumerate([1000011]):
    df1 = dfs_qed1[i]
    df2 = dfs_qed2[i]
    df3 = dfs_qed3[i]
    df4 = dfs_qed4[i]
    df5 = dfs_qed5[i]
    df_qcd = dfs_nlpll[i]

    mass = np.array(df3["mass"])
    lo1 = np.array(df1["lo"])
    lo2 = np.array(df2["lo"])
    lo3 = np.array(df3["lo"])
    lo4 = np.array(df4["lo"])
    lo5 = np.array(df5["lo"])
    mass_qcd = np.array(df_qcd["mass"][2:])
    lo_qcd = np.array(df_qcd["lo"][2:])
    
    if not np.all(mass == mass_qcd):
        print("Different masses in arrays:")
        print(f"QED: {mass}")
        print(f"QCD:    {mass_qcd}")

    rel_err1 = np.abs(lo1-lo_qcd)/lo_qcd
    rel_err2 = np.abs(lo2-lo_qcd)/lo_qcd
    rel_err3 = np.abs(lo3-lo_qcd)/lo_qcd
    rel_err4 = np.abs(lo4-lo_qcd)/lo_qcd
    rel_err5 = np.abs(lo5-lo_qcd)/lo_qcd
    
    linestyle = "solid" if i==0 else "dashed"
    marker = "x" if i==0 else "."

    lo_label = "$\\sigma^{\\mathrm{LO}}$"
    qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$"
    pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$"
    # qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$ (" + id2label(sid) + ")"
    # pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$ (" + id2label(sid) + ")"
    
    sid_label = id2label(sid)
    ax.plot(mass, rel_err1, marker=marker, linestyle=linestyle, label=sid_label+" (1e-1)")
    ax.plot(mass, rel_err2, marker=marker, linestyle=linestyle, label=sid_label+" (1e-2)")
    ax.plot(mass, rel_err3, marker=marker, linestyle="--", label=sid_label+" (1e-3)")
    ax.plot(mass, rel_err4, marker=marker, linestyle="-.", label=sid_label+" (1e-4)")
    ax.plot(mass, rel_err5, marker=marker, linestyle=":", label=sid_label+" (1e-5)")

# ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
# ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
handles, labels = ax.get_legend_handles_labels()

fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.15, 0.95), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"qed_rel_err.pdf")