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


#######################
####               ####
####   FUNCTIONS   ####
####               ####
#######################

def id2label(id: int) -> str:
    if id == 1000011:
        return "$\\tilde{e}_L^*\\tilde{e}_L$"
    if id == 2000011:
        return "$\\tilde{e}_R^*\\tilde{e}_R$"
    else:
        print(f"WARNING: Unrecognized particle ID: {id}")
        return ""


#################
### LOAD DATA ###
#################
def load_qed_data(s_sqrt=13600, slepton_ids=[1000011, 2000011]):
    qed_col_names = ["mass", "lo", "nlo", "hadron", "slepton"]
    slepton_ids = [1000011, 2000011]
    dfs = []

    for slepton_id in slepton_ids:
        filename = f"xsec_{s_sqrt}_mass_{slepton_id}.dat"
        filepath = OUTPUT_DIR/filename
        df = pd.read_csv(filepath, comment="#", names=qed_col_names, delimiter=r"\s+")

        dfs.append(df)
    return dfs

def load_qed_err_data(s_sqrt=13600, slepton_ids=[1000011, 2000011]):
    qed_err_col_names = [
        "mass",
        "lo", "lo_scale_minus", "lo_scale_plus", "lo_pdf",
        "nlo", "nlo_scale_minus", "nlo_scale_plus", "nlo_pdf"
    ]
    dfs = []
    for slepton_id in slepton_ids:
        filename = f"xsec_{s_sqrt}_mass_err_{slepton_id}.dat"
        filepath = OUTPUT_DIR/filename
        df = pd.read_csv(filepath, comment="#", names=qed_err_col_names, delimiter=r"\s+")
        
        dfs.append(df)
    return dfs

def load_qed_scale_data(
    s_sqrt=13600,
    slepton_id=1000011,
    mass_R = 600,
    masses_F=[400, 600, 800, 1000]
):
    col_names = ["scale", "lo", "nlo", "hadron", "slepton"]

    dfR = []
    filename = f"xsec_{s_sqrt}_scaleR_m{mass_R}_{slepton_id}.dat"
    filepath = OUTPUT_DIR/filename
    dfR = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")

    dfsF = []
    for mass in masses_F:
        filename = f"xsec_{s_sqrt}_scaleF_m{mass}_{slepton_id}.dat"
        filepath = OUTPUT_DIR/filename
        df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
        dfsF.append(df)
    
    return (dfR, dfsF)

def load_qcd_data(s_sqrt=13600):
    qcd_col_names = [
        "mass", "lo", "lo_scale_plus", "lo_scale_minus", "lo_pdf", "lo_alphas",
        "nlo", "nlo_scale_plus", "nlo_scale_minus", "nlo_pdf", "nlo_alphas",
        "resum", "resum_scale_plus", "resum_scale_minus", "resum_pdf", "resum_alphas"
    ]
    slepton_names = ["LH", "RH"]
    dfs_lpnll = []
    dfs_nlpll = []
    for slepton_name in slepton_names:
        filename_lpnll = f"LHC_total_{slepton_name}_LPNLL_PDFerr_{s_sqrt}.txt"
        filepath_lpnll = OUTPUT_DIR/"qcd_smoking"/filename_lpnll
        df = pd.read_csv(filepath_lpnll, skiprows=1, names=qcd_col_names, delimiter=r"\s+\|\s+", engine="python")
        df.loc[:,df.columns != "mass"] *= 1e3 # pb to fb to match QED results
        dfs_lpnll.append(df)

        filename_nlpll = f"LHC_total_{slepton_name}_LPNLL_NLPLL_PDFerr_{s_sqrt}.txt"
        filepath_nlpll = OUTPUT_DIR/"qcd_smoking"/filename_nlpll
        df = pd.read_csv(filepath_nlpll, skiprows=1, names=qcd_col_names, delimiter=r"\s+\|\s+", engine="python")
        df.loc[:,df.columns != "mass"] *= 1e3 # pb to fb to match QED results
        dfs_nlpll.append(df)
    return (dfs_lpnll, dfs_nlpll)




##################
### PLOT STUFF ###
##################
def plot_qed_err(
    s_sqrt=13600,
    slepton_ids=[1000011, 2000011]
):
    dfs = load_qed_err_data(s_sqrt, slepton_ids)
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
        df = dfs[i]
        
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
    # handles.insert(2, handles.pop())
    # labels.insert(2, labels.pop())
    # leg1 = fig.legend(handles[:4], labels[:4], frameon=False, loc="lower left", bbox_to_anchor=(0.17, 0.42), ncol=1)
    # leg2 = fig.legend(handles[4:], labels[4:], frameon=False, loc="lower left", bbox_to_anchor=(0.42, 0.42), ncol=1)
    # leg1 = fig.legend(handles[:4], labels[:4], frameon=False, loc="upper right", bbox_to_anchor=(0.97, 0.95), ncol=2)
    # leg2 = fig.legend(handles[4:], labels[4:], frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.83), ncol=1)
    leg1 = fig.legend(handles[:4], labels[:4], frameon=False, loc="upper right", bbox_to_anchor=(0.97, 0.95), ncol=1)
    leg2 = fig.legend(handles[4:], labels[4:], frameon=False, loc="upper right", bbox_to_anchor=(0.7, 0.95), ncol=1)
    fig.add_artist(leg1)

    # fig.legend(handles=handles, labels=labels, frameon=False, loc="upper right", bbox_to_anchor=(0.97,0.95), ncol=1)
    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"xsec_over_mass_{s_sqrt}.pdf")
    print(f"Plotted: xsec_over_mass_{s_sqrt}.pdf")

def plot_scale_dep(
    s_sqrt=13600,
    slepton_id=1000011,
    mass_R=600,
    masses_F=[400, 600, 800, 1000]
):
    dfR, dfsF = load_qed_scale_data(s_sqrt, slepton_id, mass_R, masses_F)
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

    axs["R"].set_xlabel("$\\mu_R/\\mu_0$")
    axs["R"].set_ylabel("$\\frac{\\sigma(\\mu_R)}{\\sigma(\\mu_0)}$")

    for axi in (axs["A"], axs["C"]):
        axi.set_ylabel("$\\frac{\\sigma(\\mu_F)}{\\sigma(\\mu_0)}$")

    for axi in (axs["C"], axs["D"]):
        axi.set_xlabel("$\\mu_F/\\mu_0$")


    mu_R_arr = dfR["scale"]
    xsec_R_lo = dfR["lo"]
    xsec_R_nlo = dfR["nlo"]

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
    # axs["R"].text(mu_R_arr[0], txtboxy, "$m_{\\tilde{e}_L} = " + str(mass_R) + "$GeV", bbox=box_dict)
    axs["R"].text(mu_R_arr[0], txtboxy, "$m_{\\tilde{e}_L} = " + str(mass_R) + "$GeV", bbox=box_dict)

    inds = ["A", "B", "C", "D"]
    for i, mass in enumerate(masses_F):
        sid = slepton_id
        df = dfsF[i]
        mu_arr = df["scale"]
        
        xsec_lo = df["lo"]
        xsec_nlo = df["nlo"]
        
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
        
        txtboxy = 1.28
        axs[inds[i]].text(0.5, txtboxy, "$m_{\\tilde{e}_L} = " + str(mass) + "$GeV", bbox=box_dict)

    fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 1.05), ncol=2)
    fig.savefig(PLOT_DIR/f"xsec_scale_ratio_{s_sqrt}.pdf")
    print(f"Plotted: xsec_scale_ratio_{s_sqrt}.pdf")

def plot_xsec_with_err(
    s_sqrt=13600,
    slepton_ids=[1000011, 2000011]
):
    dfs = load_qed_err_data(s_sqrt, slepton_ids)

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
        
        lo_pdf_err = df["lo_pdf"]
        nlo_pdf_err = df["nlo_pdf"]
        
        lo_pdf_err_rel = lo_pdf_err/xsec_lo
        nlo_pdf_err_rel = nlo_pdf_err/xsec_nlo

        label = id2label(sid)
        
        nlo_line, = axs[0].plot(m_arr, xsec_nlo, linestyle="solid", marker="x", label=label+" (NLO)")
        axs[0].fill_between(m_arr, nlo_scale_minus, nlo_scale_plus, linestyle="dashed", color=nlo_line.get_color(), alpha=0.3)
        axs[0].fill_between(m_arr, xsec_nlo - nlo_pdf_err, xsec_nlo + nlo_pdf_err, linestyle="dotted", color=nlo_line.get_color(), alpha=0.3)
        
        lo_line, = axs[0].plot(m_arr, xsec_lo, linestyle="solid", marker=".", label=label+" (LO)")
        axs[0].fill_between(m_arr, lo_scale_minus, lo_scale_plus, linestyle="dashed", color=lo_line.get_color(), alpha=0.3)
        axs[0].fill_between(m_arr, xsec_lo - lo_pdf_err, xsec_lo + lo_pdf_err, linestyle="dotted", color=lo_line.get_color(), alpha=0.3)
        
        axs[1].plot(m_arr, nlo_pdf_err_rel, linestyle="solid", marker="x", color=nlo_line.get_color())
        axs[1].plot(m_arr, lo_pdf_err_rel, linestyle="solid", marker=".", color=lo_line.get_color())
        # line, = ax.plot(m_arr, ratio, label=label)
        # ax.fill_between(m_arr, ratio-ratio_err, ratio+ratio_err, linestyle="dashed", color=line.get_color(), alpha=0.1)
    axs[0].fill_between([],[],[],color="k",linestyle="dotted", alpha=0.2, label="Scale error")
    axs[0].fill_between([],[],[],color="k",linestyle="dashed", alpha=0.2, label="PDF error")

    handles, labels = axs[0].get_legend_handles_labels()
    leg1 = fig.legend(handles[:4], labels[:4], frameon=False, loc="upper right", bbox_to_anchor=(0.97, 0.95), ncol=1)
    leg2 = fig.legend(handles[4:], labels[4:], frameon=False, loc="upper right", bbox_to_anchor=(0.7, 0.95), ncol=1)
    fig.add_artist(leg1)
    # fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95, 0.95), ncol=1)
    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"xsec_err_{s_sqrt}.pdf")
    print(f"Plotted: xsec_err_{s_sqrt}.pdf")

def plot_Kfactor(
    s_sqrt=13600,
    slepton_ids=[1000011, 2000011]
):
    dfs_qed = load_qed_data(s_sqrt, slepton_ids)
    dfs_lpnll, dfs_nlpll = load_qcd_data(s_sqrt)
    
    fig, (ax_qcd, ax) = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        figsize=(fig_width, fig_width/1.3),
        gridspec_kw={"height_ratios": [1,3]}
    )
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
        
        marker = "." if i==0 else "x"
        linestyle = "solid" if i==0 else "dashed"
        plt.gca().set_prop_cycle(None)
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
    leg1 = fig.legend(handles[:6], labels[:6], frameon=False, loc="lower left", bbox_to_anchor=(0.05, 0.95), ncol=2)
    leg2 = fig.legend(handles[6:], labels[6:], frameon=False, loc="lower left", bbox_to_anchor=(0.8, 0.95), ncol=1)
    fig.add_artist(leg1)
    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"xsec_Kfactor_{s_sqrt}.pdf")
    print(f"Plotted: xsec_Kfactor_{s_sqrt}.pdf")

def plot_ratio_qed_qcd(
    s_sqrt=13600,
    slepton_ids=[1000011, 2000011]
):
    dfs_qed = load_qed_data(s_sqrt, slepton_ids)
    dfs_lpnll, dfs_nlpll = load_qcd_data(s_sqrt)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
    ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
    ax.set_ylabel("$\\sigma^{\\mathrm{NLO}}_{\\mathrm{QED}}/\\sigma^{\\mathrm{NLO}}_{\\mathrm{QCD}}$")

    for i in range(len(slepton_ids)):
        sid = slepton_ids[i]
        df_qed = dfs_qed[i]
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
    fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.17, 0.57), ncol=2)

    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"ratio_qed_qcd_{s_sqrt}.pdf")
    print(f"Plotted: ratio_qed_qcd_{s_sqrt}.pdf")

def plot_qed_vs_pdf(
    s_sqrt=13600,
    slepton_ids=[1000011, 2000011],
    legend_placement=(0.17, 0.8)
):
    dfs = load_qed_err_data(s_sqrt, slepton_ids)
    fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
    ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
    ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")

    for i, sid in enumerate(slepton_ids):
        df = dfs[i]

        mass = np.array(df["mass"])
        lo = np.array(df["lo"])
        nlo = np.array(df["nlo"]) - np.array(df["lo"])
        pdf_err = np.array(df["lo_pdf"])

        ratio_nlo = nlo/lo
        ratio_pdf = pdf_err/lo
        
        linestyle = "solid" if i==0 else "dashed"
        marker = "x" if i==0 else "."

        qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$"
        pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$"
        
        plt.gca().set_prop_cycle(None)
        if i==0:
            ax.plot(mass, ratio_nlo, marker=marker, linestyle=linestyle, label=qed_label)
            ax.plot(mass, ratio_pdf, marker=marker, linestyle=linestyle, label=pdf_label)
        else:
            ax.plot(mass, ratio_nlo, marker=marker, linestyle=linestyle)
            ax.plot(mass, ratio_pdf, marker=marker, linestyle=linestyle)

    ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
    ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
    handles, labels = ax.get_legend_handles_labels()

    fig.legend(frameon=False, loc="upper left", bbox_to_anchor=legend_placement, ncol=2)
    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"ratio_qed_pdf_{s_sqrt}.pdf")
    print(f"Plotted: ratio_qed_pdf_{s_sqrt}.pdf")

def plot_lo_compare(
    s_sqrt=13600,
    slepton_ids=[1000011, 2000011]
):
    dfs_qed = load_qed_data(s_sqrt, slepton_ids)
    _, dfs_qcd = load_qcd_data(s_sqrt)    
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
    ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
    ax.set_ylabel("Relative error")

    for i, sid in enumerate(slepton_ids):
        df_qed = dfs_qed[i]
        df_qcd = dfs_qcd[i]

        mass = np.array(df_qed["mass"])
        mass_qcd = np.array(df_qcd["mass"][2:])
        if not np.all(mass == mass_qcd):
            raise ValueError("QED and QCD data do not share mass arrays.")
        
        lo_qed = np.array(df_qed["lo"])
        lo_qcd = np.array(df_qcd["lo"][2:])
        

        rel_err = np.abs(lo_qed-lo_qcd)/lo_qcd
        
        linestyle = "solid" if i==0 else "dashed"
        marker = "x" if i==0 else "."
        
        sid_label = id2label(sid)
        ax.plot(mass, rel_err, marker=marker, linestyle=linestyle, label=sid_label)

    fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.2, 0.8), ncol=1)
    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"qed_rel_err_{s_sqrt}.pdf")
    print(f"Plotted: qed_rel_err_{s_sqrt}.pdf")

def plot_pdf_err_s(s_sqrts=[13000, 13600, 20000, 50000, 80000]):
    fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
    ax.set_xlabel("$m_{\\tilde{e}}$ [GeV]")
    ax.set_ylabel("$\\delta^{\\mathrm{PDF}}\\sigma/\\sigma^{\\mathrm{LO}}$")

    for i, s_sqrt in enumerate(s_sqrts):
        dfs = load_qed_err_data(s_sqrt, [1000011])
        df = dfs[0]

        mass = np.array(df["mass"])
        lo = np.array(df["lo"])
        # nlo = np.array(df["nlo"]) - np.array(df["lo"])
        pdf_err = np.array(df["lo_pdf"])

        # ratio_nlo = nlo/lo
        ratio_pdf = pdf_err/lo
        
        # linestyle = "solid" if i==0 else "dashed"
        # marker = "x" if i==0 else "."

        # qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$"
        # pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$"
        label = "$\\sqrt{s} = " + str(s_sqrt) + "$"
        # plt.gca().set_prop_cycle(None)
        ax.plot(mass, ratio_pdf, marker=".", linestyle="solid", label=label)

    # ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
    # ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
    # handles, labels = ax.get_legend_handles_labels()

    fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.17, 0.9), ncol=1)
    fig.tight_layout()
    fig.savefig(PLOT_DIR/f"pdf_over_s.pdf")
    print(f"Plotted: pdf_over_s.pdf")
        



if __name__=="__main__":
    plot_qed_err(s_sqrt=13000)
    plot_scale_dep(s_sqrt=13000)
    plot_xsec_with_err(s_sqrt=13000)
    plot_Kfactor(s_sqrt=13000)
    plot_ratio_qed_qcd(s_sqrt=13000)
    plot_qed_vs_pdf(s_sqrt=13000, legend_placement=(0.17, 0.95))
    plot_lo_compare(s_sqrt=13000)
    
    plot_qed_err(s_sqrt=13600)
    plot_scale_dep(s_sqrt=13600)
    plot_xsec_with_err(s_sqrt=13600)
    plot_Kfactor(s_sqrt=13600)
    plot_ratio_qed_qcd(s_sqrt=13600)
    plot_qed_vs_pdf(s_sqrt=13600, legend_placement=(0.17, 0.95))
    plot_lo_compare(s_sqrt=13600)
    
    plot_pdf_err_s()
    plot_qed_err(s_sqrt=80000)
    plot_qed_vs_pdf(s_sqrt=80000)