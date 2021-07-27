import pygame

class Button:
    def __init__(self, width, height, posx, posy, colorB, colorT, text = None):
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.colorB = colorB
        self.colorT = colorT
        self.text = text

    def create(self, display):
        '''
        Creates the rectangle and if self.text is not None, it puts it on the center of it
        '''
        
        pygame.draw.rect(display, self.colorB, (self.posx, self.posy, self.width, self.height), 1)

        self.txt_font = pygame.font.SysFont('Comic Sans', 22)

        if self.text != None:
            txt_render = self.txt_font.render(self.text, True, self.colorT)

            display.blit(txt_render, (
                self.posx + self.width / 2 - txt_render.get_width() / 2,
                self.posy + self.height / 2 - txt_render.get_height() / 2
            ))

    def clicked(self, posx, posy):
        '''
        Returns true if posx and posy are inside the rectangle, otherwise, returns false
        '''

        if self.posx <= posx <= self.posx + self.width:
            if self.posy <= posy <= self.posy + self.height:
                return True

        else:
            return False