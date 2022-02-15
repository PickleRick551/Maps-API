import pygame, requests, sys, os

step = 0.005
FPS = 60
WIDTH = 600
HEIGHT = 450

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ymap!")
clock = pygame.time.Clock()


class MapY(object):
    def __init__(self):
        self.x = 45.008821
        self.y = 41.923153
        self.zoom = 16
        self.type = "map"  # "sat", "sat,skl"

    def gg(self):
        return str(self.y) + "," + str(self.x)

    def update(self, event):
        if event.key == pygame.K_PAGEUP and self.zoom < 19:
            self.zoom += 1
        elif event.key == pygame.K_PAGEDOWN and self.zoom > 1:
            self.zoom -= 1
        elif event.key == pygame.K_LEFT:
            self.y -= step
        elif event.key == pygame.K_RIGHT:
            self.y += step
        elif event.key == pygame.K_UP:
            self.x += step
        elif event.key == pygame.K_DOWN:
            self.x -= step

        elif event.key == pygame.K_1:
            self.type = 'map'
        elif event.key == pygame.K_2:
            self.type = 'sat'
        elif event.key == pygame.K_3:
            self.type = 'sat,skl'


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.gg(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError:
        sys.exit(2)
    return map_file

running = True
mp = MapY()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            mp.update(event)
    map_file = load_map(mp)
    pygame.display.update()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
