import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

try:
  file_path = "dsigma_test.dat"
  df = pd.read_csv(file_path, sep=" ", names=["Q2", "dsigma"])
except:
  raise FileNotFoundError(f"Unable to load {file_path}.")

fig, ax = plt.subplots(figsize=(8,6))
fig.suptitle("$\\frac{d\\sigma}{dQ^2}$ as a function of $Q^2$")
sns.lineplot(
  ax=ax,
  data=df,
  x="Q2",
  y="dsigma"
)
ax.set(
  xscale="log",
  xlabel="$Q^2$",
  ylabel="$\\frac{d\\sigma}{dQ^2}$"
)
fig.savefig("dsigma_test.pdf")