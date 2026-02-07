import streamlit as st
import pymongo
import pandas as pd
import scraper

st.set_page_config(page_title="Pokedex Analytics", layout="wide", page_icon="⚡")

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["pokedex_db"]
collection = db["pokemons"]

st.title("Pokedex Analytics")

if st.button("🔄 Update Data"):
    with st.spinner("Catching them all..."):
        count = scraper.run_scraper()
    st.success(f"{count} Pokemon loaded!")

data = list(collection.find({}, {"_id": 0}))

if data:
    df = pd.DataFrame(data)
    
    st.sidebar.header("Filters")
    selected_type = st.sidebar.selectbox("Type", ["All"] + list(df["type"].unique()))
    
    if selected_type != "All":
        df = df[df["type"] == selected_type]
        
    df = df.sort_values("total", ascending=False)
    
    st.metric("Pokemon Count", len(df))
    
    cols = st.columns(4)
    for i, row in enumerate(df.head(8).itertuples()):
        with cols[i % 4]:
            st.image(row.image)
            st.subheader(row.nom)
            st.caption(f"Type: {row.type}")
            st.progress(min(row.attaque / 150, 1.0), text=f"Atk: {row.attaque}")
            st.progress(min(row.defense / 150, 1.0), text=f"Def: {row.defense}")
            st.divider()

    st.subheader("Stats Analysis")
    st.scatter_chart(df, x="attaque", y="defense", color="type")
    
    with st.expander("Full Data"):
        st.dataframe(df)

else:
    st.info("Click the button to start!")