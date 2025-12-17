"""Visualisations Plotly."""
import plotly.express as px
import pandas as pd


def scatter_geo(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="score",
        y="code_postal",
        color="qualite",
        title="🎯 Scores de précision par zone postale",
        opacity=0.6,
        color_discrete_map={
            "excellente": "#2ecc71",
            "bonne": "#3498db",
            "acceptable": "#f39c12",
            "mauvaise": "#e74c3c"
        }
    )
    fig.update_layout(xaxis_title="Score de précision", yaxis_title="Code Postal")
    return fig

def bar_quality(df: pd.DataFrame):
    agg = df.groupby("code_postal").size().reset_index(name="count").sort_values("count", ascending=False).head(15)
    fig = px.bar(
        agg, x="code_postal", y="count",
        title="📊 Top 15 des codes postaux avec le plus d'adresses",
        color="count",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(xaxis_title="Code Postal", yaxis_title="Nombre d'adresses")
    return fig


def histogram_score(df: pd.DataFrame):
    fig = px.histogram(
        df,
        x="score",
        nbins=20,
        title="📈 Profil des scores de précision",
        color_discrete_sequence=["#9b59b6"]
    )
    fig.update_traces(marker_line_color="#8e44ad")
    return fig
