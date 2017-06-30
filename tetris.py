import pygame, sys, random
from pygame.locals import *

class Pieza:
    O = (((0,0,0,0,0), (0,0,0,0,0),(0,0,1,1,0),(0,0,1,1,0),(0,0,0,0,0)),) * 4

    I = (((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,1),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(1,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)))

    L = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,1,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,1,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    J = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,0,0,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,0,0,1,0),(0,0,0,0,0)))

    Z = (((0,0,0,0,0),(0,0,0,1,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,1,0,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,1,0,0),(0,0,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    S = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,0,1,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,0,1,1,0),(0,1,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,1,0,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,1,0),(0,1,1,0,0),(0,0,0,0,0),(0,0,0,0,0)))

    T = (((0,0,0,0,0),(0,0,1,0,0),(0,0,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,0,0,0),(0,1,1,1,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,0,0),(0,0,1,0,0),(0,0,0,0,0)),
         ((0,0,0,0,0),(0,0,1,0,0),(0,1,1,1,0),(0,0,0,0,0),(0,0,0,0,0)))

    PIEZAS = {'O': O, 'I': I, 'L': L, 'J': J, 'Z': Z, 'S':S, 'T':T}

    def __init__(self, pieza_nombre=None):
        if pieza_nombre:
            self.pieza_nommbre = pieza_nombre
        else:
            self.pieza_nombre = random.choice(Pieza.PIEZAS.keys())
        self.rotacion = 0
        self.array2d = Pieza.PIEZAS[self.pieza_nombre][self.rotacion]

    def __iter__(self):
        for row in self.array2d:
            yield row

    def rotar(self, tiempo=True):
        self.rotacion = (self.rotacion + 1) % 4 if tiempo else \
                        (self.rotacion - 1) % 4
        self.array2d = Pieza.PIEZAS[self.pieza_nombre][self.rotacion]

class tablero:
    ERROR = {'no_error': 0, 'muro_derecho': 1, 'left_muro': 2,
                     'abajo': 3, 'arriba': 4}

    def __init__(self, fondo):
        self.fondo = fondo
        self.alto = 10
        self.ancho = 22
        self.tam_bloque = 25
        self.tablero = []
        for _ in xrange(self.ancho):
            self.tablero.append([0] * self.alto)
        self.genera_pieza()

    def genera_pieza(self):
        self.Pieza = Pieza()
        self.Pieza_x, self.Pieza_y = 3, 0

    def absorb_Pieza(self):
        for y, row in enumerate(self.Pieza):
            for x, bloque in enumerate(row):
                if bloque:
                    self.tablero[y+self.Pieza_y][x+self.Pieza_x] = bloque
        self.genera_pieza()

    def _bloque_choca(self, x, y):
        if x < 0: 
            return tablero.ERROR['left_muro']
        elif x >= self.alto:
            return tablero.ERROR['muro_derecho']
        elif y >= self.ancho:
            return tablero.ERROR['abajo']
        elif self.tablero[y][x]:
            return tablero.ERROR['arriba']
        return tablero.ERROR['no_error'] 

    def choca(self, dx, dy):
        for y, row in enumerate(self.Pieza):
            for x, bloque in enumerate(row):
                if bloque:
                    chocar = self._bloque_choca(x=x+dx, y=y+dy)
                    if chocar:
                        return chocar
        return tablero.ERROR['no_error']

    def _can_mover_Pieza(self, dx, dy):
        dx_ = self.Pieza_x + dx
        dy_ = self.Pieza_y + dy
        if self.choca(dx=dx_, dy=dy_):
            return False
        return True

    def _can_correr_Pieza(self):
        return self._can_mover_Pieza(dx=0, dy=1)

    def _try_rotar_Pieza(self, tiempo=True):
        self.Pieza.rotar(tiempo)
        chocar = self.choca(dx=self.Pieza_x, dy=self.Pieza_y)
        if not chocar:
            pass
        elif chocar == tablero.ERROR['left_muro']:
            if self._can_mover_Pieza(dx=1, dy=0):
                self.mover_Pieza(dx=1, dy=0)
            elif self._can_mover_Pieza(dx=2, dy=0):
                self.mover_Pieza(dx=2, dy=0)
            else:
                self.Pieza.rotar(not tiempo)
        elif chocar == tablero.ERROR['muro_derecho']:
            if self._can_mover_Pieza(dx=-1, dy=0):
                self.mover_Pieza(dx=-1, dy=0)
            elif self._can_mover_Pieza(dx=-2, dy=0):
                self.mover_Pieza(dx=-2, dy=0)
            else:
                self.Pieza.rotar(not tiempo)
        else:
            self.Pieza.rotar(not tiempo)

    def mover_Pieza(self, dx, dy):
        if self._can_mover_Pieza(dx, dy):
            self.Pieza_x += dx
            self.Pieza_y += dy

    def correr_Pieza(self):
        if self._can_correr_Pieza():
            self.mover_Pieza(dx=0, dy=1)
        else:
            self.absorb_Pieza()
            self.delete_lines()

    def full_correr_Pieza(self):
        while self._can_correr_Pieza():
            self.correr_Pieza()
        self.correr_Pieza()

    def rotar_Pieza(self, tiempo=True):
        self._try_rotar_Pieza(tiempo)

    def pos_to_pixel(self, x, y):
        return self.tam_bloque*x, self.tam_bloque*(y-2)

    def _delete_line(self, y):
        for y in reversed(xrange(1, y+1)):
            self.tablero[y] = list(self.tablero[y-1])

    def delete_lines(self):
        remover = [y for y, row in enumerate(self.tablero) if all(row)]
        for y in remover:
            self._delete_line(y)    

    def game_over(self):
        return sum(self.tablero[0]) > 0 or sum(self.tablero[1]) > 0

    def draw_bloques(self, array2d, color=(0,0,255), dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.ancho:
                for x, bloque in enumerate(row):
                    if bloque:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        pygame.draw.rect(self.fondo, color,
                                         (  x_pix, y_pix,
                                            self.tam_bloque,
                                            self.tam_bloque))
                        
                        pygame.draw.rect(self.fondo, (0, 0, 0),
                                         (  x_pix, y_pix,
                                            self.tam_bloque,
                                            self.tam_bloque), 1)

    def draw(self):
        self.draw_bloques(self.Pieza, dx=self.Pieza_x, dy=self.Pieza_y)
        self.draw_bloques(self.tablero)

class Tetris:
    correr_EVENT = USEREVENT + 1

    def __init__(self):
        self.fondo = pygame.display.set_mode((250, 500))
        self.clock = pygame.time.Clock()
        self.tablero = tablero(self.fondo)

    def handle_key(self, event_key):
        if event_key == K_DOWN:
            self.tablero.correr_Pieza()
        elif event_key == K_LEFT:
            self.tablero.mover_Pieza(dx=-1, dy=0)
        elif event_key == K_RIGHT:
            self.tablero.mover_Pieza(dx=1, dy=0)
        elif event_key == K_UP:
            self.tablero.rotar_Pieza()
        elif event_key == K_SPACE:
            self.tablero.full_correr_Pieza()
        elif event_key == K_ESCAPE:
            self.pause()

    def pause(self):
        running = True 
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

    def run(self):
        pygame.init()
        pygame.time.set_timer(Tetris.correr_EVENT, 500)

        while True:
            if self.tablero.game_over():
                print "Game over"
                pygame.quit()
                sys.exit()
            self.fondo.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == Tetris.correr_EVENT:
                    self.tablero.correr_Pieza()
            
            self.tablero.draw()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Tetris().run()
