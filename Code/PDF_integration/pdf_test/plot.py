import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors
sns.set_theme()
# sns.set_context("paper")

try:
  file_path = "output/PDF4LHC21_40_0_2.dat"
  df = pd.read_csv(file_path, sep=" ", names=["x","Q2","xf"])
except:
  raise FileNotFoundError(f"Unable to load {file_path}.")


## Plot using seaborn
q2_values = df["Q2"].unique()[::100]
df_filtered = df[df["Q2"].isin(q2_values)]

nQ2 = df["Q2"].nunique()

fig, ax = plt.subplots(figsize=(8,6))
fig.suptitle("PDF $x f_u(x,Q^2)$")
sns.lineplot(
  ax=ax,
  data=df,
  x="x",
  y="xf",
  hue="Q2",
  palette=sns.color_palette("crest", nQ2),
  legend=False
)

## Add colorbar
q2min = df["Q2"].unique().min()
q2max = df["Q2"].unique().max()
norm = mcolors.LogNorm(vmin=q2min, vmax=q2max)
sm = cm.ScalarMappable(cmap="crest", norm=norm)
fig.colorbar(sm, ax=ax, label="Q2")

ax.set(
  xscale="log",
  xlabel="$x$",
  ylabel="$xf$"
)
fig.savefig("pdf2.pdf")