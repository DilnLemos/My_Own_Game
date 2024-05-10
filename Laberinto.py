import os
import pygame
import subprocess

# SE INICIALIZA PYGAME
pygame.init()

# SE CREA LA CLASE DE DIBUJO DE LA PARED
class Pared(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('Muro.jpg').convert_alpha()
        self.rect = self.image.get_rect()



# SE CREA LA CLASE DEL JUGADOR
class Sofi(pygame.sprite.Sprite):

    # SE INICIALIZA LA CLASE
    def __init__(self):
        super().__init__()

        # SE CARGA LA IMAGEN DEL JUGADOR Y SE OBTIENE SU RECTANGULO
        self.image = pygame.image.load("P_Stay_Down.png").convert_alpha()
        self.rect = self.image.get_rect()

# FUNCION PARA CONSTRUIR EL MAPA
def construir_mapa(mapa):
    listaMuros = []

    x = 0
    y = 0

    # CICLO PARA COGER LAS FILAS DEL MAPA
    for fila in mapa:

        # CICLO PARA COGER CADA ELEMENTO DEL MAPA
        for muro in fila:

            # CONDICIONAL PARA DETECTAR MUROS
            if muro == "X":

                # SE INSERTA LA LISTA PARED Y SE DIBUJA
                listaMuros.append(pygame.Rect(x, y, 80, 80))

            x += 80
        x = 0
        y += 80
    return listaMuros

# FUNCION PARA DIBUJAR MUROS
def dibujar_muro(superficie, rectangulo):
    pygame.draw.rect(superficie, COLOR_VERDE, rectangulo)

# FUNVION PARA DIBUJAR MAPA
def dibujar_mapa(superficie, listaMuros):
    for muro in listaMuros:
        dibujar_muro(superficie, muro)

def ganaste_amor():
    # Se define la fuente con su tamaño
    fuente = pygame.font.SysFont("Arial", 72)

    # Se define el texto renderizando la fuente con su color
    texto = fuente.render("Has Ganado mi cielito", True, COLOR_BLANCO)

    # Se Obtiene su rectangulo
    texto_rect = texto.get_rect()

    #Se centra el texto en la pantalla
    texto_rect.center = (ANCHO / 2, ALTO / 2)

    # Se dibuja el texto en la pantalla
    ventana.blit(texto, texto_rect)

# DIMENSIONES DE LA PANTALLA

ANCHO = 1350
ALTO = 900

inicio_meta = (1340,480)
final_meta = (1340, 560)

archivo_a_abrir = "CartaParaSofi.pdf"


def abrir_Archivo():
    if os.name == 'nt':  # For Windows
        os.startfile("CartaParaSofi.pdf")

# COLOR DE FONDO

COLOR_NEGRO =(0,0,0)
COLOR_VERDE = (0, 255, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_ROJO = (255, 0, 0)

# RECTANFULO CON POSICI[ON 600, 400 Y DIMESIONES 40, 40
movil = pygame.Rect(350, 750, 40, 40)

# POSICIONES EN "X" Y "Y"

x = 0
y = 0

# VARIABLES DE VELOCIDAD 
vel = 0 
altura = 0


# SE CREA LA VENTANA
ventana = pygame.display.set_mode((ANCHO, ALTO))

# TITULO DE LA VENTANA
pygame.display.set_caption("Laberinto para MiGomitaDFresa")

# RELOJ PARA LOS FRAMES
reloj = pygame.time.Clock()


# SE CREA LA LISTA DE LAS PAREDES Y LA LISTA DE SOFI

listaPared = pygame.sprite.Group()
pared = Pared()
listaPared.add(pared)

listaSofi = pygame.sprite.Group()
sofi = Sofi()
listaSofi.add(sofi)


# SE CREA EL MAPA
mapa = [
        "XXXXXXXXXXXXXXXXX",
        "X         X   X X",
        "X XXXXXX XX X   X",
        "X     X     X X X",
        "XXXXX X XXXXX XXX",
        "      X X   X X X",
        "X XXX X X X X X  ",
        "X X     X X   X X",
        "X XXXXXXX XXXXX X",
        "X    X          X",
        "XXXXXXXXXXXXXXXXX",
]

listaMuros = construir_mapa(mapa)
# VARIABLE PARA SABER SI SE PERDIÓ EL JUEGO
juego_perdido = False


# CICLO PRINCIPAL DE LA VENTANA
while not juego_perdido:

    
    # SE CREA EL RELOJ A 60 FPS
    reloj.tick(60)

    if movil.colliderect(pygame.Rect(inicio_meta[0], inicio_meta[1], 1, final_meta[1] - inicio_meta[1])):
        ventana.fill(COLOR_NEGRO)
        ganaste_amor()
        pygame.display.flip()
        pygame.time.wait(3000)  # wait 3 seconds before quitting
        abrir_Archivo()
        juego_perdido = True
        
    # SE CREA EL CICLO QUE EVALUA LOS EVENTOS DE PYGAME
    for event in pygame.event.get():

        # EVENTO QUE EVALUA EL CIERRE DEL JUEGO
        if event.type == pygame.QUIT:
            juego_perdido = True

        # EVENTO QUE EVALUA LAS TECLAS PRESIONADAS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                altura = -5
            if event.key == pygame.K_DOWN:
                altura = 5
            if event.key == pygame.K_LEFT:
                vel = -5
            if event.key == pygame.K_RIGHT:
                vel = 5
            if event.key == pygame.K_ESCAPE:
                movil = pygame.Rect(1300, 500, 40, 40)

        else:
            vel = 0
            altura = 0

    movil.x += vel
    movil.y += altura

    sofi.rect.x = movil.x
    sofi.rect.y = movil.y

    # CICLO PARA LAS COLISIONES DEL JUGADOR CON EL MURO
    for muro in listaMuros:
        if movil.colliderect(muro):
            movil.x -= vel
            movil.y -= altura

    ventana.fill(COLOR_NEGRO)

    x = 0
    y = 0

    # CICLO PARA COGER LAS FILAS DEL MAPA
    for fila in mapa:

        # CICLO PARA COGER CADA ELEMENTO DEL MAPA
        for muro in fila:

            # CONDICIONAL PARA DETECTAR MUROS
            if muro == "X":

                # PON LAS COORDENADAS DE LA PARED EN X Y EN Y
                pared.rect.x = x
                pared.rect.y = y

                # SE INSERTA LA LISTA PARED Y SE DIBUJA
                listaPared.add(pared)
                listaPared.draw(ventana)
            x += 80
        x = 0
        y += 80
    listaSofi.draw(ventana)
    #dibujar_mapa(ventana, listaMuros)

    pygame.draw.line(ventana, COLOR_ROJO, inicio_meta, final_meta)

    pygame.display.flip()

pygame.quit()
