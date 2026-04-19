import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NOMAD'S ADVENTURE", layout="wide")

# Le moteur de jeu inspiré du code source des RPG 8-bit
zelda_engine = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; background: #111; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; touch-action: none; }
        
        #game-screen { 
            position: relative; 
            width: 320px; height: 320px; 
            border: 4px solid #444; 
            background: #1a1a1a; 
            image-rendering: pixelated;
        }

        canvas { width: 100%; height: 100%; }

        /* HUD style rétro */
        #hud {
            width: 320px; background: #000; color: #fff; 
            padding: 10px; font-family: 'Courier New', monospace; 
            display: flex; justify-content: space-between; border: 4px solid #444; border-bottom: none;
        }

        /* Contrôles tactiles optimisés */
        #dpad { display: grid; grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(2, 60px); gap: 10px; margin-top: 20px; }
        .btn { 
            width: 60px; height: 60px; background: #333; border: 2px solid #fff; 
            border-radius: 10px; color: #fff; display: flex; justify-content: center; 
            align-items: center; font-size: 24px; user-select: none; 
        }
        .btn:active { background: #666; }
    </style>
</head>
<body>

    <div id="hud">
        <div>❤️ x <span id="hp">3</span></div>
        <div>LVL <span id="lvl">1</span></div>
    </div>

    <div id="game-screen">
        <canvas id="canvas"></canvas>
    </div>

    <div id="dpad">
        <div style="grid-column: 2" class="btn" id="up">↑</div>
        <div class="btn" id="left">←</div>
        <div class="btn" id="down">↓</div>
        <div class="btn" id="right">→</div>
    </div>

<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 160; canvas.height = 160; // Basse résolution pour le look NES

    const TILE_SIZE = 16;
    let player = { x: 5, y: 5, color: '#00ff41' };
    
    // 0 = Herbe, 1 = Arbre (Collision), 2 = Sortie
    const worldMap = [
        [1,1,1,1,1,2,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,0,1,1,0,1],
        [1,0,1,1,0,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ];

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Rendu de la Tilemap (Code type Zelda NES)
        for(let y=0; y<10; y++) {
            for(let x=0; x<10; x++) {
                let tile = worldMap[y][x];
                if(tile === 1) { // Arbre
                    ctx.fillStyle = '#0a4d0a';
                    ctx.fillRect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE);
                    ctx.fillStyle = '#147a14';
                    ctx.fillRect(x*TILE_SIZE+2, y*TILE_SIZE+2, TILE_SIZE-4, TILE_SIZE-4);
                } else if(tile === 2) { // Sortie
                    ctx.fillStyle = '#555';
                    ctx.fillRect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE);
                } else { // Herbe
                    ctx.fillStyle = '#1e3d1e';
                    ctx.fillRect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE);
                }
            }
        }

        // Joueur (Link)
        ctx.fillStyle = player.color;
        ctx.fillRect(player.x*TILE_SIZE+2, player.y*TILE_SIZE+2, TILE_SIZE-4, TILE_SIZE-4);
        // Épée (directionnelle)
        ctx.fillStyle = '#fff';
        ctx.fillRect(player.x*TILE_SIZE+10, player.y*TILE_SIZE+4, 4, 2);
    }

    function move(dx, dy) {
        let nextX = player.x + dx;
        let nextY = player.y + dy;

        // GESTION DES COLLISIONS (Le coeur du code Zelda)
        if(nextX >= 0 && nextX < 10 && nextY >= 0 && nextY < 10) {
            if(worldMap[nextY][nextX] !== 1) {
                player.x = nextX;
                player.y = nextY;
            }
        }
        
        // GESTION DU CHANGEMENT DE ZONE
        if(worldMap[player.y][player.x] === 2) {
            alert("Tu quittes la forêt... Bienvenue dans le Désert !");
            // Ici on chargerait la nouvelle worldMap
        }
        
        draw();
    }

    // Handlers Tactiles
    document.getElementById('up').onclick = () => move(0, -1);
    document.getElementById('down').onclick = () => move(0, 1);
    document.getElementById('left').onclick = () => move(-1, 0);
    document.getElementById('right').onclick = () => move(1, 0);

    draw();
</script>
</body>
</html>
"""

components.html(zelda_engine, height=650)
