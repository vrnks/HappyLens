import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HappyMap", layout="wide")
st.title("🌍 HappyMap - Country Clustering and Personalized Ranking")

# --- Load data ---
@st.cache_data
def load_clustered_data():
    return pd.read_csv("./data/clustered_happiness.csv")

@st.cache_data
def load_happiness_data():
    df = pd.read_csv("./data/happiness_data.csv")
    df = df[df["Year"] == 2024]
    df = df.drop(columns=["Year", "Rank", "upperwhisker", "lowerwhisker"])
    return df

cluster_df = load_clustered_data()
happiness_df = load_happiness_data()

# --- Colors for clusters ---
cluster_colors = {
    0: "#66c2a5",  # green
    1: "#fc8d62",  # orange
    2: "#8da0cb",  # blue
    3: "#e78ac3"   # pink
}

# --- Cluster descriptions ---
cluster_descriptions = {
    0: {
        "emoji": "🟡",
        "title": "Cluster 0 — Moderately Happy",
        "desc": "Balanced countries with decent GDP, support, and health. Often upper-middle-income with improving quality of life.",
        "examples": "Poland, Czechia, Brazil, Taiwan",
        "avg_score": 6.07
    },
    1: {
        "emoji": "🟠",
        "title": "Cluster 1 — Under Pressure",
        "desc": "Lower income and health, but notable civic freedom and generosity. Often politically or economically strained.",
        "examples": "Ukraine, India, Iran, Nigeria",
        "avg_score": 4.93
    },
    2: {
        "emoji": "🟢",
        "title": "Cluster 2 — Most Prosperous",
        "desc": "High scores across GDP, health, and freedom. Strong institutions and high trust levels.",
        "examples": "Finland, Netherlands, Australia, Canada",
        "avg_score": 6.81
    },
    3: {
        "emoji": "🔴",
        "title": "Cluster 3 — Struggling Nations",
        "desc": "Low across all indicators. Includes fragile or conflict-affected countries with systemic issues.",
        "examples": "Afghanistan, Lebanon, DR Congo, Ethiopia",
        "avg_score": 4.09
    }
}

# --- Cluster map ---
st.subheader("Country Clustering by Happiness Level")

fig = px.choropleth(
    cluster_df,
    locations="iso_alpha",
    color="Cluster",
    hover_name="Country",
    color_discrete_map=cluster_colors,
    projection="natural earth",
    height=700
)
# --- Additional labels on the map ---
fig.add_scattergeo(
    lon=[105.0],  
    lat=[57.5],   
    text=["<b>Ukrainian Ocean</b>"],  
    mode='text',
    showlegend=False,  
    textfont=dict(size=10, color='black')
)

fig.add_scattergeo(
    lon=[37.6176], 
    lat=[55.7558],
    text=["<b>Kharkiv lagoon</b>"],
    mode='text',
    showlegend=False,  
    textfont=dict(size=6, color='black')
)

fig.add_scattergeo(
    lon=[34.0],  
    lat=[44.9], 
    text=["<b>Crimea is Ukraine🇺🇦</b>"],
    mode='text',
    showlegend=False,
    textfont=dict(size=2, color='darkblue')
)
st.plotly_chart(fig, use_container_width=True)

# --- Interactive "CLI" ---
st.subheader("🧠 Choose weights for happiness factors")

factors = ['GDP', 'SocialSupport', 'LifeExpectancy', 'Freedom', 'Generosity', 'Corruption']
weights = {}
cols = st.columns(3)

for i, factor in enumerate(factors):
    with cols[i % 3]:
        weights[factor] = st.slider(factor, 0.0, 1.0, 0.5, 0.05)

if st.button("🔍 Show personalized ranking"):
    df = happiness_df.copy()
    for factor in factors:
        df[factor] = pd.to_numeric(df[factor], errors='coerce')
    df["Score"] = sum(df[factor] * weights[factor] for factor in factors)
    top10 = df[["Country", "HappinessScore", "Score"]].sort_values(by="Score", ascending=False).head(10)

    st.success("🎉 Your personalized ranking:")
    st.dataframe(top10, use_container_width=True)

# --- Cluster view by button ---
st.subheader("📊 View countries by cluster")

cluster_options = sorted(cluster_df["Cluster"].unique())
cluster_id = st.radio("Select a cluster:", cluster_options, horizontal=True)
filtered = cluster_df[cluster_df["Cluster"] == cluster_id]

# --- Description of the selected cluster ---
desc = cluster_descriptions[cluster_id]
st.markdown(f"""
**{desc['emoji']} {desc['title']}**

- **Avg. Score**: {desc['avg_score']}
- **Examples**: {desc['examples']}
- **Summary**: {desc['desc']}
""")

st.dataframe(filtered[["Country", "Cluster"]])
