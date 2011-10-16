import pygame
class InputHandler():
    def input(self):
        currentEvent = pygame.event.poll()
        return currentEvent
    
    def checkInput(self, input):
        if input.type != pygame.NOEVENT:
            return True
        else:
            return False
    
    def checkMouseInput(self, input):
        if input.type == pygame.MOUSEBUTTONUP:
            return pygame.mouse.get_pos()
        else:
            return None
    
    def checkDirectionInput(self, input):
        if input.type == pygame.KEYDOWN:
            if input.key == pygame.K_DOWN: return 1
            elif input.key == pygame.K_UP: return 2
            elif input.key == pygame.K_LEFT: return 3
            elif input.key == pygame.K_RIGHT: return 4
        else:
            return None
    
    def quit(self, input):
        if input.type == pygame.QUIT:
            return True
        else:
            return False