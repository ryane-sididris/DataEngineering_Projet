import streamlit as st
import pymongo
import pandas as pd
import scraper
import altair as alt

st.set_page_config(page_title="Pokedex Dashboard", layout="wide")

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["pokedex_db"]
collection = db["pokemons"]

col_header, col_btn = st.columns([4, 1])
with col_header:
    st.title("Pokedex Analytics Dashboard")
with col_btn:
    st.write("")
    if st.button("Update Data", type="primary"):
        with st.spinner("Fetching data..."):
            count = scraper.run_scraper()
        st.success(f"Updated: {count} Pokemon")
        st.rerun()

data = list(collection.find({}, {"_id": 0}))

if data:
    df_all = pd.DataFrame(data)
    
    st.sidebar.header("Recherche")
    search_name = st.sidebar.text_input("Nom du Pokémon")
    selected_type = st.sidebar.selectbox("Type", ["Tous"] + list(df_all["type"].unique()))
    
    st.sidebar.markdown("---")
    st.sidebar.header("Filtrer par Stats")
    min_attack = st.sidebar.slider("Attaque Minimum", 0, 200, 0)
    min_defense = st.sidebar.slider("Défense Minimum", 0, 200, 0)
    min_hp = st.sidebar.slider("PV Minimum", 0, 255, 0)
    
    st.sidebar.markdown("---")
    sort_option = st.sidebar.selectbox("Trier par", ["Pokedex ID", "Puissance Totale", "Attaque", "Défense", "Nom"])

    df_charts = df_all[
        (df_all["attaque"] >= min_attack) & 
        (df_all["defense"] >= min_defense) & 
        (df_all["hp"] >= min_hp)
    ]
    
    df_filtered = df_charts.copy()
    if search_name:
        df_filtered = df_filtered[df_filtered["nom"].str.contains(search_name, case=False)]
    if selected_type != "Tous":
        df_filtered = df_filtered[df_filtered["type"] == selected_type]
        
    if sort_option == "Puissance Totale":
        df_filtered = df_filtered.sort_values("total", ascending=False)
    elif sort_option == "Attaque":
        df_filtered = df_filtered.sort_values("attaque", ascending=False)
    elif sort_option == "Défense":
        df_filtered = df_filtered.sort_values("defense", ascending=False)
    elif sort_option == "Nom":
        df_filtered = df_filtered.sort_values("nom", ascending=True)

    st.markdown("### 📊 Stats de la sélection")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("Nombre affiché", len(df_filtered))
    if not df_filtered.empty:
        kpi2.metric("Moyenne Attaque", f"{df_filtered['attaque'].mean():.1f}", delta=f"{df_filtered['attaque'].mean() - df_all['attaque'].mean():.1f} vs Global")
        kpi3.metric("Moyenne Défense", f"{df_filtered['defense'].mean():.1f}", delta=f"{df_filtered['defense'].mean() - df_all['defense'].mean():.1f} vs Global")
        best_poke = df_filtered.loc[df_filtered['total'].idxmax()]
        kpi4.metric("Le + Fort (sélection)", best_poke['nom'], f"{best_poke['total']} pts")
    else:
        kpi2.metric("Moyenne Attaque", "0")
        kpi3.metric("Moyenne Défense", "0")
        kpi4.metric("Le + Fort", "-", "0 pts")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Galerie (Sélection)", "Vue Globale (Filtrée par Stats)", "Données Brutes"])

    with tab1:
        if not df_filtered.empty:
            cols = st.columns(5)
            for i, row in enumerate(df_filtered.itertuples()):
                with cols[i % 5]:
                    with st.container(border=True):
                        st.image(row.image, use_container_width=True)
                        st.subheader(row.nom)
                        st.caption(f"Type: {row.type}")
                        st.write(f"⚔️ **{row.attaque}** |  🛡️ **{row.defense}**")
                        st.progress(min(row.total / 800, 1.0), text=f"Total: {row.total}")
        else:
            st.warning("Aucun Pokémon ne correspond à tes critères.")

    with tab2:
        st.info(f"💡 Ces graphiques incluent tous les Pokémon respectant les critères de stats (Attaque > {min_attack}, Défense > {min_defense}, HP > {min_hp})")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Heatmap Attaque vs Défense")
            
            heatmap = alt.Chart(df_charts).mark_rect().encode(
                x=alt.X('attaque', bin=alt.Bin(maxbins=20), title='Attaque'),
                y=alt.Y('defense', bin=alt.Bin(maxbins=20), title='Défense'),
                color=alt.Color('count()', scale=alt.Scale(scheme='viridis'), title='Nombre'),
                tooltip=['attaque', 'defense', 'count()']
            ).properties(
                height=400
            )
            st.altair_chart(heatmap, use_container_width=True)
        
        with c2:
            st.subheader("Répartition par Type")
            type_counts = df_charts['type'].value_counts().reset_index()
            type_counts.columns = ['type', 'count']
            
            bar_chart = alt.Chart(type_counts).mark_bar().encode(
                x=alt.X('type', sort='-y', title='Type'),
                y=alt.Y('count', title='Nombre'),
                color=alt.Color('type', legend=None),
                tooltip=['type', 'count']
            ).properties(
                height=400
            )
            st.altair_chart(bar_chart, use_container_width=True)

    with tab3:
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("La base de données est vide. Clique sur 'Update Data'.")