import pygame
import random
import sys

# --- INICIALIZACIÓN ---
pygame.init()
pygame.mixer.init()

# --- PANTALLA ---
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("♻️ Recicla y Gana")

# --- COLORES ---
VERDE = (50, 200, 50)
AZUL = (80, 160, 255)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
ROJO = (220, 50, 50)

# --- FUENTE ---
fuente = pygame.font.SysFont("Arial", 28)

# --- MÚSICA DE FONDO ---
# Asegúrate de tener un archivo "musica_fondo.mp3" en la misma carpeta del juego
try:
    pygame.mixer.music.load("Ce.mp3")
    pygame.mixer.music.play(-1)  # -1 = loop infinito
except:
    print("⚠️ No se encontró el archivo 'musica_fondo.mp3'.")

# --- OBJETOS Y VARIABLES ---
contenedor = pygame.Rect(350, 520, 100, 50)
velocidad = 8

objetos = []
TAM_OBJETO = 40
tiempo_nuevo = 1000
ultimo_tiempo = pygame.time.get_ticks()

puntos = 0
reloj = pygame.time.Clock()

# --- LOOP PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento del contenedor ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and contenedor.left > 0:
        contenedor.x -= velocidad
    if teclas[pygame.K_RIGHT] and contenedor.right < ANCHO:
        contenedor.x += velocidad

    # --- Generar objetos nuevos ---
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_tiempo > tiempo_nuevo:
        x = random.randint(0, ANCHO - TAM_OBJETO)
        tipo = random.choice(["reciclable", "basura"])
        color = VERDE if tipo == "reciclable" else ROJO
        objetos.append({
            "rect": pygame.Rect(x, 0, TAM_OBJETO, TAM_OBJETO),
            "tipo": tipo,
            "color": color
        })
        ultimo_tiempo = tiempo_actual

    # --- Mover objetos ---
    for obj in objetos:
        obj["rect"].y += 5

    # --- Colisiones ---
    for obj in objetos[:]:
        if contenedor.colliderect(obj["rect"]):
            if obj["tipo"] == "reciclable":
                puntos += 1
            else:
                puntos -= 1
            objetos.remove(obj)

    # --- Eliminar los que salen de pantalla ---
    objetos = [o for o in objetos if o["rect"].y < ALTO]

    # --- Dibujar ---
    pantalla.fill(AZUL)
    pygame.draw.rect(pantalla, VERDE, (0, 570, ANCHO, 30))  # Césped
    pygame.draw.rect(pantalla, GRIS, contenedor)  # Contenedor

    for obj in objetos:
        pygame.draw.circle(pantalla, obj["color"], obj["rect"].center, TAM_OBJETO // 2)

    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    reloj.tick(60)
