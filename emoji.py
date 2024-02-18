def happy():
  pygame.draw.circle(screen, (255,255,0), (400, 150), 100, 100)
  pygame.draw.circle(screen, (0,0,0), (370, 105), 25, 50)
  pygame.draw.circle(screen, (0,0,0), (440, 105), 25, 50)
  gfxdraw.arc(screen,400,155,65,0,180,(0,0,0))

def sad():
  pygame.draw.circle(screen, (255,255,0), (400, 150), 100, 100)
  pygame.draw.circle(screen, (0,0,0), (370, 105), 25, 50)
  pygame.draw.circle(screen, (0,0,0), (440, 105), 25, 50)
  gfxdraw.arc(screen,400,205,65,180,0,(0,0,0))

import pygame
from pygame import gfxdraw

screen = pygame.display.set_mode((800,650))