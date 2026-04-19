import pygame
import sys

# --- 1. CONFIGURATION GÉNÉRALE ---
pygame.init()

# Couleurs (Format RGB)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT_HERBE = (34, 139, 34)
BLEU_EAU = (65, 105, 225)
BRUN_TERRE = (139, 69, 19)
JAUNE_JOUEUR = (255, 215, 0)

# Paramètres de l'écran
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
TAILLE_TUILE = 40  # Taille d'une case (ex: 40x40 pixels)
FENETRE = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Le Délire Zelda-like v0.1")

# Contrôle du temps (FPS)
HORLOGE = pygame.time.Clock()
FPS = 60


# --- 2. CLASSES DES OBJETS DU JEU ---

class Joueur:
    def __init__(self, x, y):
        self.x = x * TAILLE_TUILE
        self.y = y * TAILLE_TUILE
        self.vitesse = 4
        # Création d'un carré pour représenter le joueur pour l'instant
        self.rect = pygame.Rect(self.x, self.y, TAILLE_TUILE, TAILLE_TUILE)

    def deplacer(self, touches):
        dx, dy = 0, 0
        if touches[pygame.K_LEFT] or touches[pygame.K_q]: # Gauche ou Q
            dx = -self.vitesse
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]: # Droite ou D
            dx = self.vitesse
        if touches[pygame.K_UP] or touches[pygame.K_z]:    # Haut ou Z
            dy = -self.vitesse
        if touches[pygame.K_DOWN] or touches[pygame.K_s]:  # Bas ou S
            dy = self.vitesse
            
        # Mise à jour de la position (sans gestion des collisions pour l'instant)
        self.rect.x += dx
        self.rect.y += dy

    def dessiner(self, surface):
        # On dessine un carré jaune pour le héros
        pygame.draw.rect(surface, JAUNE_JOUEUR, self.rect)


class Carte:
    def __init__(self):
        # 0 = Herbe, 1 = Eau (mur), 2 = Terre
        # Une petite carte d'exemple
        self.grille = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def dessiner(self, surface):
        for y, ligne in enumerate(self.grille):
            for x, tuile in enumerate(ligne):
                rect = pygame.Rect(x * TAILLE_TUILE, y * TAILLE_TUILE, TAILLE_TUILE, TAILLE_TUILE)
                if tuile == 0:
                    pygame.draw.rect(surface, VERT_HERBE, rect)
                elif tuile == 1:
                    pygame.draw.rect(surface, BLEU_EAU, rect)
                elif tuile == 2:
                    pygame.draw.rect(surface, BRUN_TERRE, rect)
                # Dessiner les contours des tuiles pour mieux voir la grille (optionnel)
                # pygame.draw.rect(surface, NOIR, rect, 1)


# --- 3. BOUCLE PRINCIPALE DU JEU ---

def main():
    # Initialisation de nos objets
    ma_carte = Carte()
    # On place le joueur à la case (5, 5)
    heros = Joueur(5, 5)

    en_cours = True
    while en_cours:
        # A. Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            # Exemple : appuye sur ESPACE pour une "action" (vide pour l'instant)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("COUCOU ! J'AI APPUYÉ SUR ESPACE (ATTACK/INTERACT) !")

        # B. Mise à jour de l'état du jeu (la logique)
        touches = pygame.key.get_pressed()
        heros.deplacer(touches)

        # C. Dessin de l'écran
        FENETRE.fill(NOIR)  # On efface tout
        ma_carte.dessiner(FENETRE)  # On dessine le fond (carte)
        heros.dessiner(FENETRE)   # On dessine le joueur par-dessus

        # D. Rafraîchissement de l'écran
        pygame.display.flip()

        # E. Limiter la vitesse (FPS)
        HORLOGE.tick(FPS)

    # Quitter proprement
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
