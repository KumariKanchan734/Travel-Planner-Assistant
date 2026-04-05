import streamlit as st
import pandas as pd
import re

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Travel Planner", page_icon="✈️", layout="wide")

# ---------------------------
# Custom CSS (for cards UI 🔥)
# ---------------------------
st.markdown("""
<style>
.card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.4);
    transition: transform 0.3s;
    border: 1px solid #333;
}
.card:hover {
    transform: translateY(-5px);
    border-color: #00ffd5;
}
.title {
    font-size: 22px;
    font-weight: bold;
    color: #00ffd5;
    margin-bottom: 15px;
}
.text {
    font-size: 15px;
    color: #e0e0e0;
    margin-bottom: 8px;
}
.btn-container {
    margin-top: 15px;
}
.search-btn {
    background-color: #00ffd5;
    color: #000 !important;
    padding: 8px 15px;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    display: inline-block;
    transition: background 0.3s;
}
.search-btn:hover {
    background-color: #00ccaa;
}
.image-container {
    width: 100%;
    height: 180px;
    border-radius: 10px;
    object-fit: cover;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Title & Instructions
# ---------------------------
st.title("✈️ Travel Planner Assistant 🇮🇳")
st.markdown("### Plan your perfect trip with smart recommendations")
st.markdown("Use the filters on the left to find the best destinations matching your budget, preferred travel style, and desired rating. Click 'Search on Google' to learn more about a destination.")

# ---------------------------
# Load Dataset
# ---------------------------
@st.cache_data
def load_data():
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent_dir, "travel_india.csv")
    df = pd.read_csv(file_path)
    # Strip whitespace from column names just to be safe
    df.columns = df.columns.str.strip()
    df = df.dropna()
    return df

df = load_data()

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Righteous&display=swap');
</style>
<div style='text-align: center; margin-bottom: 30px; margin-top: 10px;'>
    <div style='margin-bottom: 20px;'>
        <h1 style='margin:0; font-family: "Righteous", cursive; font-size: 38px; font-weight: 400; background: -webkit-linear-gradient(45deg, #00c6ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1.5px;'>🎒 TravelWise</h1>
    </div>
    <div style='padding: 15px; background: rgba(255, 255, 255, 0.03); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
        <p style='margin:0; color:#888888; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Developed By</p>
        <p style='margin: 8px 0 5px 0; color:#00ffd5; font-size: 20px; font-weight: bold;'>Kanchan Kumari</p>
        <div style='background: rgba(0, 255, 213, 0.1); display: inline-block; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(0, 255, 213, 0.2);'>
            <p style='margin:0; color:#e0e0e0; font-size: 13px; font-weight: 500;'>🎓 B24BS1184</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h4 style='color: #00ffd5; margin-bottom: 0px;'>🎯 Personalize Search</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #aaaaaa; font-size: 13px; margin-bottom: 15px;'>Looking for a specific trip?</p>", unsafe_allow_html=True)

location = st.sidebar.selectbox(
    "📍 State/Region",
    ["All"] + sorted(df['location'].unique())
)

budget = st.sidebar.number_input(
    "💰 Max Budget (₹)",
    min_value=int(df['cost'].min()),
    max_value=int(df['cost'].max()),
    value=int(df['cost'].mean()),
    step=500
)

travel_type = st.sidebar.selectbox(
    "🧭 Travel Type",
    ["All"] + sorted(df['type'].unique())
)

min_rating = st.sidebar.slider("⭐ Rating", 1.0, 5.0, 4.0, 0.1)

# ---------------------------
# Filtering Logic
# ---------------------------
filtered = df[
    (df['cost'] <= budget) &
    (df['rating'] >= min_rating)
]

if location != "All":
    filtered = filtered[filtered['location'] == location]

if travel_type != "All":
    filtered = filtered[filtered['type'].str.lower() == travel_type.lower()]

# Sort by rating
filtered = filtered.sort_values(by='rating', ascending=False)

# ---------------------------
# Results Section (Grid Layout)
# ---------------------------
st.subheader(f"🎯 Recommended Destinations ({len(filtered)} found)")

if filtered.empty:
    st.warning("No destinations found matching your criteria 😢 Try adjusting the filters.")
else:
    cols = st.columns(3)

    for i, (_, row) in enumerate(filtered.head(12).iterrows()):
        with cols[i % 3]:
            # Clean up destination name (remove trailing numbers if any)
            dest_name = re.sub(r'\s*\d+$', '', row['destination_name'])
            
            search_query = f"{dest_name} {row['location']} tourism".replace(' ', '+')
            search_url = f"https://www.google.com/search?q={search_query}"
            
            # Using picsum for a reliable placeholder distinct per destination
            seed = dest_name.replace(' ', '')
            image_url = f"https://picsum.photos/seed/{seed}/400/300"
            
            st.markdown(f"""
            <div class="card">
                <img src="{image_url}" class="image-container" alt="{dest_name}">
                <div class="title">🌍 {dest_name}</div>
                <div class="text">📍 <b>State:</b> {row['location']}</div>
                <div class="text">🧭 <b>Type:</b> {row['type'].title()}</div>
                <div class="text">⏳ <b>Duration:</b> {row['days']} Days</div>
                <div class="text">🏡 <b>Stay:</b> {row['stay']} &nbsp;|&nbsp; 🚌 <b>Transport:</b> {row['transport']}</div>
                <div class="text">💰 <b>Cost:</b> ₹{row['cost']}</div>
                <div class="text">⭐ <b>Rating:</b> {row['rating']} / 5.0</div>
                <div class="btn-container">
                    <a href="{search_url}" target="_blank" class="search-btn">🔍 Search on Google</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>✨ Built with ❤️ using Pandas + Streamlit for a seamless travel planning experience.</div>", unsafe_allow_html=True)