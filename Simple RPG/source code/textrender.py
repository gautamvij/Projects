import pygame,random,sys

class RenderText(pygame.sprite.Sprite):
    def __init__(self, font_name, font_size, font_colour):
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.SysFont(font_name, font_size)
            self.color = font_colour
            self.render_text = "FPS: 0.0"
            self.rerender(5,5)
    def update(self):
            pass
    def print_text(self, text_string, x, y):
            self.render_text = text_string
            self.rerender(x,y)
    def rerender(self, x, y):
            self.image = self.font.render(self.render_text, 0, self.color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
