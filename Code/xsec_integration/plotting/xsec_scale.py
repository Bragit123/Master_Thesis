from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
# sns.set_theme()


FILE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FILE_DIR.parent / "output"
PLOT_DIR = FILE_DIR / "plots" / "scale_plots"

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

col_names = ["scale", "lo", "nlo", "hadron", "slepton"]
slepton_ids = [1000011, 2000011]
dfs = []
for slepton_id in slepton_ids:
  filename = "xsec_scale_" + str(slepton_id) + ".dat"
  filepath = OUTPUT_DIR/filename
  df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
  dfs.append(df)

scale_slepton_id = 1000011
# scale_mass = 100
scale_masses = [100, 500]
scales = ["R", "F"]
dfs_scale = []
for mass in scale_masses:
    dfs_scale_m = []
    for scale in scales:
        filename = "xsec_scale" + scale + "_m" + str(mass) + "_" + str(scale_slepton_id) + ".dat"
        filepath = OUTPUT_DIR/filename
        df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
        dfs_scale_m.append(df)
    dfs_scale.append(dfs_scale_m)
  
#   filename = "xsec_scaleF_" + str(slepton_id) + ".dat"
#   filepath = OUTPUT_DIR/filename
#   df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
#   dfFs.append(df)


##################
### LO and NLO ###
##################
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
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


# #########################
# ### (LO+NLO)/LO Ratio ###
# #########################
# fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$\\mu_F/m_{\\tilde\\ell}$")
# ax.set_ylabel("$\\sigma/\\sigma^{\\text{LO}}$")
# # ax.set_xscale("log")
# for i in range(len(slepton_ids)):
#   sid = slepton_ids[i]
#   df = dfs[i]
#   mu_arr = df["scale"]
#   xsec_lo = df["lo"]
#   xsec_nlo = df["nlo"]
#   ratio = xsec_nlo/xsec_lo
#   # ratio = df["ratio"]
#   # color = ("blue" if i==0 else "green")
#   # marker = ("o" if i==0 else "x")
#   marker = "."
#   label = id2label(sid)
#   plt.plot(mu_arr, ratio, linestyle="solid", marker=marker, label=label)

# fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=3)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/"xsec_scale_ratio.pdf")

#########################
### (LO+NLO)/LO Ratio ###
#########################
fig, axs = plt.subplots(
    nrows=2,
    ncols=2,
    sharex=True,
    figsize=(fig_width, fig_width/1.3)
)
# axs[0].set_xlabel("$\\mu_R/m_{\\tilde\\ell}$")
# axs[1].set_xlabel("$\\mu_F/m_{\\tilde\\ell}$")
# axs[1].set_xlabel("$\\mu/m_{\\tilde\\ell}$")
axs[1,0].set_xlabel("$\\mu/m_{\\tilde\\ell}$")
axs[1,1].set_xlabel("$\\mu/m_{\\tilde\\ell}$")
# for axi in axs:
#     axi.set_ylabel("$\\sigma/\\sigma(\\mu_0)$")
#     axi.set_xscale("log", base=2)
for axi in axs[:,0]:
    axi.set_ylabel("$\\sigma/\\sigma(\\mu_0)$")
for axrow in axs:
    for axcol in axrow:
        axcol.set_xscale("log", base=2)
handle_common = [None, None]
handle_specific = [None, None]
# for i in range(len(slepton_ids)):
# for i in range(1):
#     sid = slepton_ids[i]
#     dfR = dfRs[i]
#     dfF = dfFs[i]
#     muR_arr = dfR["scale"]
#     muF_arr = dfF["scale"]
    
#     xsecR_lo = dfR["lo"]
#     xsecF_lo = dfF["lo"]
#     xsecR_nlo = dfR["nlo"]
#     xsecF_nlo = dfF["nlo"]
#     xsecR_hadron = dfR["hadron"]
#     xsecF_hadron = dfF["hadron"]
#     xsecR_slepton = dfR["slepton"]
#     xsecF_slepton = dfF["slepton"]
    
#     xsecR_lo_0 = xsecR_lo[2]
#     xsecF_lo_0 = xsecF_lo[2]
#     xsecR_nlo_0 = xsecR_nlo[2]
#     xsecF_nlo_0 = xsecF_nlo[2]
#     xsecR_hadron_0 = xsecR_hadron[2]
#     xsecF_hadron_0 = xsecF_hadron[2]
#     xsecR_slepton_0 = xsecR_slepton[2]
#     xsecF_slepton_0 = xsecF_slepton[2]
#     # ratioR = xsecR_nlo/xsecR_lo
#     # ratioF = xsecF_nlo/xsecF_lo
#     ratioR_lo = xsecR_lo/xsecR_lo_0
#     ratioF_lo = xsecF_lo/xsecF_lo_0
#     ratioR_nlo = xsecR_nlo/xsecR_nlo_0
#     ratioF_nlo = xsecF_nlo/xsecF_nlo_0
#     ratioR_hadron = xsecR_hadron/xsecR_hadron_0
#     ratioF_hadron = xsecF_hadron/xsecF_hadron_0
#     ratioR_slepton = xsecR_slepton/xsecR_slepton_0
#     ratioF_slepton = xsecF_slepton/xsecF_slepton_0
#     # ratio = df["ratio"]
#     # color = ("blue" if i==0 else "green")
#     # marker = ("o" if i==0 else "x")
#     marker = "."
#     label = id2label(sid)
#     axs[0].plot(muR_arr, ratioR_lo, linestyle="solid", marker=marker, label=f"LO")
#     axs[0].plot(muR_arr, ratioR_nlo, linestyle="solid", marker=marker, label=f"NLO")
#     axs[0].plot(muR_arr, ratioR_hadron, linestyle="dashed", marker=marker, label=f"NLO initial-state")
#     axs[0].plot(muR_arr, ratioR_slepton, linestyle="dashed", marker=marker, label=f"NLO final-state")
#     # axs[0].plot(muR_arr, xsecR_lo, linestyle="solid", marker=marker, label=f"LO")
#     # axs[0].plot(muR_arr, xsecR_nlo, linestyle="solid", marker=marker, label=f"NLO")
#     # axs[0].plot(muR_arr, xsecR_hadron, linestyle="dashed", marker=marker, label=f"NLO initial-state")
#     # axs[0].plot(muR_arr, xsecR_slepton, linestyle="dashed", marker=marker, label=f"NLO final-state")
#     # line, = axs[0].plot(muR_arr, ratioR, linestyle="solid", marker=marker)
#     axs[1].plot(muF_arr, ratioF_lo, linestyle="solid", marker=marker)
#     axs[1].plot(muF_arr, ratioF_nlo, linestyle="solid", marker=marker)
#     axs[1].plot(muF_arr, ratioF_hadron, linestyle="dashed", marker=marker)
#     axs[1].plot(muF_arr, ratioF_slepton, linestyle="dashed", marker=marker)
#     # handle_common[i], = axs[0].plot([], [], color=line.get_color(), marker=marker, label=id2label(slepton_ids[0]))
    
#     axs[0].text(0.3, 0.994, "$\\mu_R = \\mu$\n$\\mu_F = m_{\\tilde{\\ell}}$")
#     axs[1].text(0.3, 1, "$\\mu_R = m_{\\tilde{\\ell}}$\n$\\mu_F = \\mu$")
for im in range(len(scale_masses)):
    for i in range(len(scales)):
        sid = scale_slepton_id
        df = dfs_scale[im][i]
        mu_arr = df["scale"]
        
        xsec_lo = df["lo"]
        xsec_nlo = df["nlo"]
        xsec_hadron = df["hadron"]
        xsec_slepton = df["slepton"]
        
        xsec_lo_0 = xsec_lo[2]
        xsec_nlo_0 = xsec_nlo[2]
        xsec_hadron_0 = xsec_hadron[2]
        xsec_slepton_0 = xsec_slepton[2]
        ratio_lo = xsec_lo/xsec_lo_0
        ratio_nlo = xsec_nlo/xsec_nlo_0
        ratio_hadron = xsec_hadron/xsec_hadron_0
        ratio_slepton = xsec_slepton/xsec_slepton_0
        marker = "."
        label = id2label(sid)
        if i==0 and im==0:
            axs[im,i].plot(mu_arr, ratio_lo, linestyle="solid", marker=marker, label=f"LO")
            axs[im,i].plot(mu_arr, ratio_nlo, linestyle="solid", marker=marker, label=f"NLO")
            axs[im,i].plot(mu_arr, ratio_hadron, linestyle="dashed", marker=marker, label=f"NLO initial-state")
            axs[im,i].plot(mu_arr, ratio_slepton, linestyle="dashed", marker=marker, label=f"NLO final-state")
        else:
            axs[im,i].plot(mu_arr, ratio_lo, linestyle="solid", marker=marker)
            axs[im,i].plot(mu_arr, ratio_nlo, linestyle="solid", marker=marker)
            axs[im,i].plot(mu_arr, ratio_hadron, linestyle="dashed", marker=marker)
            axs[im,i].plot(mu_arr, ratio_slepton, linestyle="dashed", marker=marker)
        
        # axs[0].plot(muR_arr, xsecR_lo, linestyle="solid", marker=marker, label=f"LO")
        # axs[0].plot(muR_arr, xsecR_nlo, linestyle="solid", marker=marker, label=f"NLO")
        # axs[0].plot(muR_arr, xsecR_hadron, linestyle="dashed", marker=marker, label=f"NLO initial-state")
        # axs[0].plot(muR_arr, xsecR_slepton, linestyle="dashed", marker=marker, label=f"NLO final-state")
        # line, = axs[0].plot(muR_arr, ratioR, linestyle="solid", marker=marker)
        # axs[1].plot(muF_arr, ratioF_lo, linestyle="solid", marker=marker)
        # axs[1].plot(muF_arr, ratioF_nlo, linestyle="solid", marker=marker)
        # axs[1].plot(muF_arr, ratioF_hadron, linestyle="dashed", marker=marker)
        # axs[1].plot(muF_arr, ratioF_slepton, linestyle="dashed", marker=marker)
        # handle_common[i], = axs[0].plot([], [], color=line.get_color(), marker=marker, label=id2label(slepton_ids[0]))
    
scale_masses = [100, 500]
# scales = ["R", "F"]
axs[0,0].text(0.3, 0.994, "$m_{\\tilde{\\ell}}=100$\n$\\mu_R = \\mu$\n$\\mu_F = m_{\\tilde{\\ell}}$")
axs[1,0].text(0.3, 0.994, "$m_{\\tilde{\\ell}}=500$\n$\\mu_R = \\mu$\n$\\mu_F = m_{\\tilde{\\ell}}$")
axs[0,1].text(0.3, 1, "$m_{\\tilde{\\ell}} = 100$\n$\\mu_F = m_{\\tilde{\\ell}}$\n$\\mu_F = \\mu$")
axs[1,1].text(0.3, 1, "$m_{\\tilde{\\ell}} = 500$\n$\\mu_F = m_{\\tilde{\\ell}}$\n$\\mu_F = \\mu$")

# handle_common, = axs[1].plot([], [], color="b", label=id2label(slepton_ids[1]))
# fig.legend(handles=handle_common, loc="upper center", 
#            bbox_to_anchor=(0.5, 1.05), ncol=2)
fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.6, 1.1), ncol=2)
fig.tight_layout()
fig.savefig(PLOT_DIR/"xsec_scale_ratio.pdf")


#######################
### Hadron--Slepton ###
#######################
fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
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
