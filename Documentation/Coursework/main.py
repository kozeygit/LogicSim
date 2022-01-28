# import pygame
import flask

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()

'''from Logic_Gates import *

# pygame.init()
# screen = pygame.display.set_mode((300, 300))
# clock = pygame.time.Clock()
# FPS = 60

s1 = Switch()
s2 = Switch()
a1 = And_Gate()
n1 = Not_Gate()

a1.connectNode(1, s1)
a1.connectNode(2, s2)

print(a1.getOutput())

s1.flip()
print(a1.getOutput())

s2.flip()
print(a1.getOutput())

n1.connectNode(1, a1)

print(n1.getOutput())






# run = True
# and_gate = Gate()
# while run:
#   clock.tick(FPS)
#   screen.fill((255, 0, 0))
#   and_gate.blitSelf()
#   pygame.display.update()
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       run = False
#     if event.type == pygame.MOUSEBUTTONDOWN:
#       pos = pygame.mouse.get_pos()
#       if and_gate.rect.collidepoint(pos):
#         and_gate.enableDrag(1)
#     if event.type == pygame.MOUSEBUTTONUP:
#       and_gate.enableDrag(0)
# pygame.quit()





'''

