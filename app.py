import streamlit as st
import random

# 1. Configuration du jeu
st.set_page_config(page_title="THE QUEST OF NOMAD", layout="centered")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .game-container { background: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #444; text-align: center; }
    .log-box { background: #000; color: #00ff41; padding: 10px; border-radius: 5px; font-family: monospace; height: 100px; overflow-y: auto; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if 'player' not in st.session_state:
    st.session_state.player = {
        "pos": [5, 5],
        "hp": 100, "max_hp": 100,
        "level": 1, "exp": 0, "exp_next": 100,
        "weapon": "Poings", "range": 1, "atk": 10,
        "biome": "Forêt", "gold": 0
    }
    st.session_state.logs = ["Bienvenue, Voyageur. Utilise les flèches pour explorer."]
    st.session_state.monsters = []

# --- DÉFINITION DES BIOMES ---
BIOMES = {
    "Forêt": {"emoji": "🌲", "ground": "._", "monster": "👾", "boss": "🐺", "color": "#1e2e1e"},
    "Désert": {"emoji": "🌵", "ground": "..", "monster": "🦂", "boss": "🐍", "color": "#3e3e1e"},
    "Neige": {"emoji": "❄️", "ground": "__", "monster": "⛄", "boss": "🐻", "color": "#1e2e3e"}
}

def spawn_monsters():
    st.session_state.monsters = [[random.randint(1, 8), random.randint(1, 8)] for _ in range(4)]

if not st.session_state.monsters:
    spawn_monsters()

# --- MÉCANIQUES DE JEU ---
def move(dx, dy):
    p = st.session_state.player
    new_x, new_y = p["pos"][0] + dx, p["pos"][1] + dy
    
    # Changement de Map (Sortie des bords)
    if new_x < 0 or new_x > 9 or new_y < 0 or new_y > 9:
        biomes_list = list(BIOMES.keys())
        current_idx = biomes_list.index(p["biome"])
        p["biome"] = biomes_list[(current_idx + 1) % len(biomes_list)]
        p["pos"] = [5, 5] # Repositions au centre
        spawn_monsters()
        st.session_state.logs.insert(0, f"✨ Tu entres dans le biome : {p['biome']} !")
    else:
        p["pos"] = [new_x, new_y]

    # Rencontre Monstre
    if p["pos"] in st.session_state.monsters:
        m_type = BIOMES[p["biome"]]["monster"]
        dmg_done = p["atk"] + random.randint(0, 5)
        p["exp"] += 40
        p["hp"] -= random.randint(5, 15)
        st.session_state.logs.insert(0, f"⚔️ Tu attaques {m_type} avec {p['weapon']} (-{dmg_done} XP) !")
        st.session_state.monsters.remove(p["pos"])
        
        # Drop d'équipement aléatoire
        if random.random() < 0.3:
            items = [("Épée en Fer", 25, 1), ("Arc Long", 20, 3)]
            new_item, n_atk, n_range = random.choice(items)
            p["weapon"], p["atk"], p["range"] = new_item, n_atk, n_range
            st.session_state.logs.insert(0, f"🎁 TROUVÉ : {new_item} !")

    # Level Up (Style Zelda/RPG)
    if p["exp"] >= p["exp_next"]:
        p["level"] += 1
        p["exp"] = 0
        p["exp_next"] = int(p["exp_next"] * 1.5)
        p["max_hp"] += 20
        p["hp"] = p["max_hp"]
        p["atk"] += 5
        st.session_state.logs.insert(0, f"🌟 NIVEAU {p['level']} ! Tu deviens plus fort.")

# --- AFFICHAGE ---
p = st.session_state.player
st.title(f"🛡️ NOMAD'S QUEST : {p['biome']}")

# Stats Bar
cols = st.columns(4)
cols[0].metric("LVL", p["level"])
cols[1].metric("HP", f"{p['hp']}/{p['max_hp']}")
cols[2].metric("EXP", f"{p['exp']}/{p['exp_next']}")
cols[3].metric("ARME", p["weapon"])

# Rendu de la Grille
b = BIOMES[p["biome"]]
grid_html = f"<div style='font-family: monospace; font-size: 24px; background: {b['color']}; padding: 15px; border-radius: 10px; line-height: 1.2; letter-spacing: 4px; border: 3px solid #555;'>"
for r in range(10):
    row = ""
    for c in range(10):
        if [r, c] == p["pos"]:
            row += "🧙‍♂️"
        elif [r, c] in st.session_state.monsters:
            row += b["monster"]
        elif (r*c) % 7 == 0:
            row += b["emoji"]
        else:
            row += b["ground"]
    grid_html += row + "<br>"
grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

# Contrôles
st.write("")
c1, c2, c3 = st.columns([1,1,1])
if c2.button("  ▲  "): move(-1, 0); st.rerun()
c1, c2, c3 = st.columns([1,1,1])
if c1.button("  ◄  "): move(0, -1); st.rerun()
if c2.button("  ▼  "): move(1, 0); st.rerun()
if c3.button("  ►  "): move(0, 1); st.rerun()

# Logs
st.write("---")
log_text = "<div class='log-box'>" + "<br>".join(st.session_state.logs[:5]) + "</div>"
st.markdown(log_text, unsafe_allow_html=True)

if p["hp"] <= 0:
    st.error("GAME OVER")
    if st.button("Ressusciter"):
        del st.session_state.player
        st.rerun()
