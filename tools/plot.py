import pandas as pd
import plotly.express as px

df = pd.read_csv(
    "data.csv", sep=";", header=None, names=["code", "name", "f", "m"]
).drop(columns="code")
df["fp"] = df["f"] / (df["f"] + df["m"])
df["mp"] = df["m"] / (df["f"] + df["m"])
df["net"] = df["fp"] - df["mp"]
df = df[(df != 0).all(1)]
fig = px.scatter(
    df,
    x="net",
    y="name",
    color="net",
    title="Program Preference by Gender in Turkey",
    labels={"net": "Preference (Male–Female)", "name": "Program Name"},
    height=8000,
)
fig.update_layout(yaxis={"categoryorder": "total ascending"}, title_x=0.5)
fig.update(layout_coloraxis_showscale=False)
fig.update_traces(marker_size=10)
fig.add_vline(x=0)

fig.show()
