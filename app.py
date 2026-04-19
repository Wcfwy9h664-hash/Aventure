import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NOMAD'S QUEST PRO", layout="wide")

# --- INTERFACE DES STATS (PYTHON) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .hud-title { font-family: 'Monospace'; color: #cddc39; font-size: 30px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- LE MOTEUR DE JEU (HTML5 CANVAS + JAVASCRIPT) ---
# C'est ici qu'on crée le rendu "Zelda"
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #121212; font-family: 'Courier New', Courier, monospace; }
        #game-container { position: relative; width: 800px; height: 500px; margin: auto; border: 6px solid #3d3d29; border-radius: 10px; overflow: hidden; }
        canvas { display: block; image-rendering: pixelated; }
        
        /* HUD Style Image */
        #hud {
            position: absolute; top: 10px; left: 10px;
            background: rgba(0, 0, 0, 0.7); border: 2px solid #8bc34a;
            padding: 15px; color: #fff; border-radius: 5px; pointer-events: none;
        }
        .stat-val { color: #cddc39; font-weight: bold; }
        
        /* Log style Zelda */
        #log {
            position: absolute; bottom: 0; width: 100%;
            background: rgba(255, 255, 255, 0.9); color: #222;
            padding: 10px; font-weight: bold; border-top: 4px solid #555;
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="hud">
        <div style="font-size: 18px; margin-bottom: 5px;">NOMAD'S QUEST</div>
        <div>NIVEAU: <span class="stat-val" id="lvl">3</span></div>
        <div>PV: <span class="stat-val" id="hp">80/100</span></div>
        <div>EXP: <span class="stat-val" id="exp">75/150</span></div>
        <div>ARME: <span class="stat-val">ÉPÉE EN FER</span></div>
    </div>
    
    <canvas id="canvas"></canvas>
    
    <div id="log">Bienvenue ! Utilise les FLÈCHES pour bouger et ESPACE pour attaquer.</div>
</div>

<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800; canvas.height = 500;

    // --- ASSETS (Images Pixel Art réelles) ---
    const groundImg = new Image(); groundImg.src = 'https://img.itch.zone/aW1nLzI3MTYxNjAucG5n/original/7uY8P6.png'; // Texture herbe
    const heroImg = new Image(); heroImg.src = 'https://opengameart.org/sites/default/files/styles/medium/public/pipo-charachip001.png'; // Sprite Sheet
    
    let player = { x: 400, y: 250, size: 32, speed: 4 };
    let keys = {};

    window.addEventListener('keydown', e => keys[e.code] = true);
    window.addEventListener('keyup', e => keys[e.code] = false);

    function update() {
        if (keys['ArrowUp']) player.y -= player.speed;
        if (keys['ArrowDown']) player.y += player.speed;
        if (keys['ArrowLeft']) player.x -= player.speed;
        if (keys['ArrowRight']) player.x += player.speed;
        
        // Combat simple
        if (keys['Space']) {
            document.getElementById('log').innerHTML = "⚔️ Tu frappes dans le vide avec classe !";
            setTimeout(() => { document.getElementById('log').innerHTML = "En attente d'un monstre..."; }, 1000);
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dessiner le sol (Répétition de la texture)
        for(let i=0; i<canvas.width; i+=64) {
            for(let j=0; j<canvas.height; j+=64) {
                ctx.drawImage(groundImg, i, j, 64, 64);
            }
        }

        // Dessiner le Héros (On prend une portion de la sprite sheet)
        ctx.drawImage(heroImg, 32, 0, 32, 32, player.x, player.y, 48, 48);

        // Dessiner des obstacles (Arbres simples)
        ctx.fillStyle = "#2d4c1e";
        ctx.fillRect(200, 100, 40, 60);
        ctx.fillRect(500, 300, 40, 60);
    }

    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    heroImg.onload = gameLoop;
</script>
</body>
</html>
"""

# Injection du jeu dans Streamlit
components.html(game_html, height=600)

st.write("---")
st.info("💡 Utilise les touches directionnelles de ton clavier pour te déplacer en temps réel.")
