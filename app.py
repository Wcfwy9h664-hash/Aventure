import streamlit as st
import random

# --- CONFIGURATION VISUELLE ---
st.set_page_config(page_title="NOMAD'S QUEST", layout="wide")

st.markdown("""
    <style>
    /* Fond global sombre */
    .stApp { background-color: #121212; }
    
    /* Le cadre du jeu */
    .game-screen {
        background-image: url('https://img.freepik.com/vecteurs-libre/fond-texture-herbe-pixel-art_1017-27161.jpg'); /* Texture herbe */
        background-size: 50px;
        border: 8px solid #3d3d29;
        border-radius: 10px;
        position: relative;
        height: 500px;
        image-rendering: pixelated;
    }

    /* Fenêtre des stats (HUD) */
    .hud-overlay {
        position: absolute;
        top: 20px;
        left: 20px;
        background: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border: 2px solid #8bc34a;
        color: #f0f0f0;
        font-family: 'Monospace';
        border-radius: 5px;
        z-index: 100;
    }

    /* Le Journal (Log) en bas */
    .log-container {
        background: rgba(255, 255, 255, 0.9);
        color: #000;
        padding: 10px;
        border-radius: 0 0 10px 10px;
        font-family: 'Courier New';
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'game' not in st.session_state:
    st.session_state.game = {
        "lvl": 3, "exp": 75, "hp": 80, "atk": 15, "def": 10,
        "pos": [200, 250], # Position en pixels pour plus de fluidité
        "logs": ["Une bave apparaît ! Appuie sur COMBAT"]
    }

g = st.session_state.game

# --- INTERFACE HUD ---
st.markdown(f"""
    <div class="game-screen">
        <div class="hud-overlay">
            <h3 style='margin:0; color:#cddc39;'>NOMAD'S QUEST</h3>
            <p>NIVEAU: {g['lvl']}<br>
            EXP: {g['exp']}/150<br>
            PV: {g['hp']}/100<br>
            ATT: {g['atk']}<br>
            DEF: {g['def']}</p>
        </div>
        <div style="position: absolute; top: {g['pos'][0]}px; left: {g['pos'][1]}px; font-size: 40px;">
            🧝‍♂️
        </div>
    </div>
    <div class="log-container">
        LOG: {g['logs'][0]}
    </div>
""", unsafe_allow_html=True)

# --- COMMANDES ---
st.write(" ")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.button("⬅️"): g['pos'][1] -= 20; st.rerun()
with c2:
    if st.button("⬆️"): g['pos'][0] -= 20; st.rerun()
with c3:
    if st.button("⬇️"): g['pos'][0] += 20; st.rerun()
with c4:
    if st.button("➡️"): g['pos'][1] += 20; st.rerun()
with c5:
    if st.button("⚔️ COMBAT"): 
        g['exp'] += 25
        g['logs'][0] = "Héros attaque ! Slime vaincu ! +10 GP"
        st.rerun()

st.button("🎒 INVENTAIRE")
