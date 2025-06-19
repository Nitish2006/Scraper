import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('imdb.csv')

# Page configuration
st.set_page_config(page_title="IMDB TOP MOVIES", layout='wide')
st.title("🎬 IMDB TOP RATED MOVIES DASHBOARD")
st.markdown("Explore top-rated IMDB movies using filters and visual insights.")

# Sidebar Filters
st.sidebar.header("📊 Filter Options")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

search_query = st.sidebar.text_input("Search by Title")

# Filter Data
filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

if search_query:
    filtered = filtered[filtered['Title'].str.contains(search_query, case=False)]

# Data Table
st.subheader(f"🎞️ Movies Released Between {year_range[0]} - {year_range[1]}")
st.dataframe(filtered)

# Top 10 Movies Bar Chart
top10 = filtered.sort_values(by='Rating', ascending=False).head(10)

fig = px.bar(
    top10,
    x="Rating",
    y="Title",
    orientation="h",
    color="Rating",
    title="⭐ Top 10 IMDB Movies by Rating",
    color_continuous_scale="viridis"
)
fig.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, use_container_width=True)

# Posters Section
st.subheader("🎥 Movie Posters")
cols = st.columns(5)
for i, row in top10.iterrows():
    with cols[i % 5]:
        st.image(row["Poster"], caption=row["Title"], width=150)
