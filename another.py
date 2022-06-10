import pygame
from Variables import *
screen = pygame.display.set_mode((1200,660))
pygame.display.set_caption('Platform Template')
clock = pygame.time.Clock()
# Importing my level.py which contains my game set up

class Level():
    # setting up the map with the data entered in settings.py
    def __init__(self, level_data,surface):
        self.display_surface = surface
        self.setup_level(level_data)

        # This will allow the map to move with player
        self.world_shift = 0


    # This is allowing me to make a grid.  by using my For loop I can loop through my Level array and add my Tile Class blocks to each space that contains a 'X' and a player to the place that has a 'P'
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            # print(row)
            # print(row_index)
            for column_index, column in enumerate(row):
                # print(f'{row_index},{column_index}:{column}')
                if column == 'X':
                    x = column_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if column == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    # This will stop my player from moving through a block when its hit
    def horizontal_move_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
    # Same for this one
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0


    # This is what allows for my screen to move.  When the screen moves the players speed actually stops and the screen moves which gives it the effect that the whole thing is moving
    def scroll_x(self):
        player = self.player.sprite  
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.update()
        self.horizontal_move_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.scroll_x() 

level = Level(level_map,screen)
class Player(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = pygame.Surface((32,60))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = position)

        # Player movement
        self.direction = pygame.math.Vector2(0,0)
        self.gravity_value = 0.9
        self.jump_speed = -8
        self.speed = 3

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1 
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def gravity(self):
        self.direction.y += self.gravity_value
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed


    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        self.gravity()

class Tile(pygame.sprite.Sprite):
    def __init__(self,position,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft= position)

    def update(self, x_shift):
        self.rect.x += x_shift    


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')
    level.run()
    # test_tile.draw(screen)

    pygame.display.update()
    clock.tick(60)  