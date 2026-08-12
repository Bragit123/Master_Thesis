# ## Plot total xsec
# fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
# ax.set_ylabel("$\\sigma$ [fb]")
# ax.set_yscale("log")
# for i in range(len(slepton_ids)):
#     sid = slepton_ids[i]
#     df = dfs_qed[i]
#     m_arr = df["mass"]
#     xsec_lo = df["lo"]
#     xsec_nlo = df["nlo"]
#     label = id2label(sid)
#     ax.plot(m_arr, xsec_nlo, linestyle="solid", marker="x", label=label+" (NLO)")
#     ax.plot(m_arr, xsec_lo, linestyle="dashed", marker=".", label=label+" (LO)")
# fig.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.95,0.95), ncol=1)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/"xsec_over_mass.pdf")




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



# ########################################
# ### Scale Dependence Renormalization ###
# ########################################
# col_names = ["scale", "lo", "nlo", "hadron", "slepton"]

# scale_slepton_id = 1000011
# mass = 100

# filename = "xsec_scaleR_m" + str(mass) + "_" + str(scale_slepton_id) + ".dat"
# filepath = OUTPUT_DIR/filename
# df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")

# ## Plot
# fig, ax = plt.subplots(
#     figsize=(fig_width, fig_width/2)
# )

# ax.set_xscale("log", base=2)
# ax.xaxis.set_major_formatter(ScalarFormatter())

# ax.set_ylabel("$\\frac{\\sigma(\\mu_R)}{\\sigma(\\mu_0)}$")
# ax.set_xlabel("$\\mu_R/m_{\\tilde{e}_L}$")

# mu_arr = df["scale"]

# xsec_lo = df["lo"]
# xsec_nlo = df["nlo"]

# ind0 = np.argwhere(mu_arr==1).item()
# xsec_lo_0 = xsec_lo[ind0]
# xsec_nlo_0 = xsec_nlo[ind0]
# ratio_lo = xsec_lo/xsec_lo_0
# ratio_nlo = xsec_nlo/xsec_nlo_0

# ax.plot(mu_arr, ratio_nlo, linestyle="solid", marker="x", label=f"NLO")
# ax.plot(mu_arr, ratio_lo, linestyle="dashed", marker=".", label=f"LO")

# box_dict = {
#     "boxstyle": "round",
#     "facecolor": "wheat",
#     "alpha": 0.2
# }
# txtboxy = 1.03
# ax.text(mu_arr[0], txtboxy, "$m_{\\tilde{e}_L} = " + str(mass) + "$GeV", bbox=box_dict)

# fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 1.05), ncol=2)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/f"xsec_muR_ratio.pdf")







# #############################
# ### Xsec with Scale Error ###
# #############################
# col_names = [
#     "mass", "lo", "lo_scale_minus", "lo_scale_plus", "nlo", "nlo_scale_minus", "nlo_scale_plus"
# ]
# slepton_ids = [1000011, 2000011]
# dfs = []
# for slepton_id in slepton_ids:
#     filename = "xsec_mass_scale_err_" + str(slepton_id) + ".dat"
#     filepath = OUTPUT_DIR/filename
#     df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
#     dfs.append(df)

# fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
# ax.set_ylabel("$\\sigma/\\sigma^{\\text{LO}}$")
# # ax.set_yscale("log")
# for i in range(len(slepton_ids)):
#     sid = slepton_ids[i]
#     df = dfs[i]
    
#     m_arr = df["mass"]
#     xsec_lo = df["lo"]
#     xsec_nlo = df["nlo"]
    
#     # scale_err_lo = df["lo_scale_err"]
#     # scale_err_nlo = df["nlo_scale_err"]
#     lo_scale_minus = df["lo_scale_minus"]
#     lo_scale_plus = df["lo_scale_plus"]
#     nlo_scale_minus = df["nlo_scale_minus"]
#     nlo_scale_plus = df["nlo_scale_plus"]
    
#     K_central = xsec_nlo/xsec_lo
#     K_minus = nlo_scale_minus/lo_scale_minus
#     K_plus = nlo_scale_plus/lo_scale_plus
    
#     Ks = [K_central, K_minus, K_plus]
#     K_max = np.maximum.reduce(Ks)
#     K_min = np.minimum.reduce(Ks)
    
#     # ratio = xsec_nlo/xsec_lo
#     # ratio_err = ratio * np.sqrt((scale_err_lo/xsec_lo)**2 + (scale_err_nlo/xsec_nlo)**2)
    
#     # ratio = scale_err_nlo/xsec_nlo
#     # ratio_err = 0
#     # ratio = xsec_nlo/(xsec_nlo-xsec_lo)
#     # ratio_err = np.abs(xsec_nlo * xsec_lo/(xsec_nlo-xsec_lo)**2) * np.sqrt((scale_err_lo/xsec_lo)**2 + (scale_err_nlo/xsec_nlo)**2)
    
#     # color = ("blue" if i==0 else "green")
#     linestyle = ("solid" if i==0 else "dashed")
#     marker = ("." if i==0 else "x")


#     label = id2label(sid)
#     # plt.plot(m_arr, ratio, color=color, linestyle="solid", marker=marker, label=label)
#     if i == 1:
#         err_label = "Scale Errors"
#     else:
#         err_label = None

#     # ax.plot(m_arr, scale_err_lo/xsec_lo, marker=marker, linestyle=linestyle, label="LO")
#     # ax.plot(m_arr, scale_err_nlo/xsec_nlo, marker=marker, linestyle=linestyle, label="NLO")
#     # ax.plot(m_arr, scale_err_ratio, marker=marker, linestyle=linestyle, label="Ratio")
#     # ax.plot(m_arr, ratio, marker=marker, linestyle=linestyle, label="ratio")
#     # error_plot(ax, m_arr, ratio, scale_err_ratio, linestyle=linestyle, marker=marker, label=label, err_label=err_label)
#     line, = ax.plot(m_arr, K_central, marker=".", label=label)
#     ax.fill_between(m_arr, K_min, K_max, linestyle="dashed", color=line.get_color(), alpha=0.3)
#     # line, = ax.plot(m_arr, ratio, label=label)
#     # ax.fill_between(m_arr, ratio-ratio_err, ratio+ratio_err, linestyle="dashed", color=line.get_color(), alpha=0.1)
# fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=2)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/"xsec_scale_err_ratio.pdf")




# ###########################
# ### Xsec with PDF Error ###
# ###########################
# col_names = [
#     "mass", "lo", "lo_pdf_err", "nlo", "nlo_pdf_err"
# ]
# slepton_ids = [1000011, 2000011]
# dfs = []
# for slepton_id in slepton_ids:
#     filename = "xsec_mass_pdf_err_" + str(slepton_id) + ".dat"
#     filepath = OUTPUT_DIR/filename
#     df = pd.read_csv(filepath, comment="#", names=col_names, delimiter=r"\s+")
#     dfs.append(df)

# fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
# ax.set_ylabel("$\\sigma$")
# ax.set_yscale("log")
# for i in range(len(slepton_ids)):
#     sid = slepton_ids[i]
#     df = dfs[i]
    
#     m_arr = df["mass"]
#     xsec_lo = df["lo"]
#     xsec_nlo = df["nlo"]
    
#     lo_pdf_err = df["lo_pdf_err"]
#     nlo_pdf_err = df["nlo_pdf_err"]

#     label = id2label(sid)
    
#     line, = ax.plot(m_arr, xsec_nlo, marker=".", label=label)
#     ax.fill_between(m_arr, xsec_nlo - nlo_pdf_err, xsec_nlo + nlo_pdf_err, linestyle="dotted", color=line.get_color(), alpha=0.3)
#     # line, = ax.plot(m_arr, ratio, label=label)
#     # ax.fill_between(m_arr, ratio-ratio_err, ratio+ratio_err, linestyle="dashed", color=line.get_color(), alpha=0.1)
# fig.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.55, 0.95), ncol=2)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/"xsec_pdf_err.pdf")







# #############################
# ### NLO QED vs QCD Errors ###
# #############################
# fig, ax = plt.subplots(figsize=(fig_width, fig_width/1.3))
# ax.set_xlabel("$m_{\\tilde\\ell}$ [GeV]")
# ax.set_ylabel("$\\sigma/\\sigma^{\\mathrm{LO}}$")

# for i in range(len(slepton_ids)):
#     sid = slepton_ids[i]
#     df_qed = dfs_qed[i]
#     df_lpnll = dfs_lpnll[i]
#     df_nlpll = dfs_nlpll[i]

#     qed_lo = df_qed["lo"]
#     qed_nlo_only = df_qed["nlo"] - df_qed["lo"]
#     qed_hadron_only = df_qed["hadron"] - df_qed["lo"]
#     qed_slepton_only = df_qed["slepton"] - df_qed["lo"]
    
#     # qcd_lo = df_nlpll["lo"][2:]
#     # qcd_resum = df_nlpll["resum"][2:]

#     # ratio_qed = qed_nlo_only / qcd_resum
#     # qcd_pdf_rel_err = df_nlpll["resum_pdf"] / qcd_resum
#     # qcd_scale_rel_err = (df_nlpll["resum_scale_plus"] - df_nlpll["resum_scale_minus"]) / qcd_resum
#     # ratio_qed = np.array(qed_nlo_only) / qed_lo
#     # ratio_qcd = np.array(qcd_resum) / qcd_lo
#     # qcd_pdf_rel_err = np.array(df_nlpll["lo_pdf"][2:]) / qcd_lo
#     # qcd_scale_rel_err = np.array(df_nlpll["lo_scale_plus"][2:] - df_nlpll["lo_scale_minus"][2:]) / qcd_lo

#     ratio_nlo = np.array(qed_nlo_only) / qed_lo
    
#     linestyle = "solid" if i==0 else "dashed"
#     marker = "." if i==0 else "x"

#     sid_label = id2label(sid)
#     # qed_label = f"QED ({sid_label})"
#     # pdf_label = f"PDF ({sid_label})"
#     # scale_label = f"Scale ({sid_label})"
#     # qed_label = "$\\sigma^{\\mathrm{NLO}}_{\\mathrm{QED}}$" + f" ({sid_label})"
#     # pdf_label = "$\\delta\\sigma^{\\mathrm{PDF}}$" + f" ({sid_label})"
#     # scale_label = "$\\delta\\sigma^{\\mu}$" + f" ({sid_label})"
#     qed_label = "$\\sigma_{\\mathrm{QED}}^{\\mathrm{NLO}}$"
#     pdf_label = "$\\delta\\sigma_{\\mathrm{LO}}^{\\mathrm{PDF}}$"
#     scale_label = "$\\delta\\sigma^{\\mu}$"
    
#     plt.gca().set_prop_cycle(None)
#     if i==0:
#         ax.plot(df_qed["mass"], ratio_qed, marker=marker, linestyle=linestyle, label=qed_label)
#         ax.plot(df_qcd["mass"][2:], qcd_pdf_rel_err, marker=marker, linestyle=linestyle, label=pdf_label)
#     else:
#         ax.plot(df_qed["mass"], ratio_qed, marker=marker, linestyle=linestyle)
#         ax.plot(df_qcd["mass"][2:], qcd_pdf_rel_err, marker=marker, linestyle=linestyle)
#     # ax.plot(df_qcd["mass"][2:], qcd_scale_rel_err, marker=marker, label=scale_label, linestyle=linestyle)

# ax.plot([],[], linestyle="solid", marker=".", color="k", label=id2label(slepton_ids[0]))
# ax.plot([],[], linestyle="dashed", marker="x", color="k", label=id2label(slepton_ids[1]))
# handles, labels = ax.get_legend_handles_labels()
# # leg1 = fig.legend(handles[:3], labels[:3], frameon=False, loc="upper left", bbox_to_anchor=(0.2, 0.55), ncol=1)
# # leg2 = fig.legend(handles[3:], labels[3:], frameon=False, loc="upper left", bbox_to_anchor=(0.5, 0.55), ncol=1)
# # fig.add_artist(leg1)
# fig.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.2, 0.9), ncol=2)
# fig.tight_layout()
# fig.savefig(PLOT_DIR/"ratio_qed_qcdnlo.pdf")

