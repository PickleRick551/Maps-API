import pygame, requests, sys, os


class MapY(object):
    def __init__(self):
        self.x = 45.008821
        self.y = 41.923153
        self.zoom = 16
        self.type = "map"  # "sat", "sat,skl"

    def gg(self):
        return str(self.y) + "," + str(self.x)

    def update(self, event):
        if event.key == 49 and self.zoom < 19:
            self.zoom += 1
        elif event.key == 50 and self.zoom > 1:
            self.zoom -= 1

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.gg(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        sys.exit(2)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapY()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
