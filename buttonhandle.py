import pygame


class button(pygame.sprite.Sprite):
    '''class for handling buttons in pygame. when the button is hovered over it will grow (waow.)
    will tell you if it's been clicked by returning true. check this by doing if button(args): then what you want it to do'''
    def __init__(self, rect : pygame.Rect, color : tuple):
        self.rect = pygame.Rect(rect)
        self.rectcopy = rect
        self.color = color

        pygame.sprite.Sprite.__init__(self)

    def update(self, window : pygame.display, mousepos : tuple, mousebuttonup : bool):

        pygame.draw.circle(window, self.color, (self.rect[0], self.rect[1]), 10, draw_top_left=True, draw_bottom_left=False, draw_bottom_right=False, draw_top_right=False)

        pygame.draw.circle(window, self.color, (self.rect[0] + self.rect[2], self.rect[1]), 
            10, draw_top_left=False, draw_bottom_left=False, draw_bottom_right=False, draw_top_right=True)

        pygame.draw.circle(window, self.color, (self.rect[0], self.rect[1] + self.rect[3]), 
            10, draw_top_left=False, draw_bottom_left=True, draw_bottom_right=False, draw_top_right=False)

        pygame.draw.circle(window, self.color, (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]), 
            10, draw_top_left=False, draw_bottom_left=False, draw_bottom_right=True, draw_top_right=False)

        pygame.draw.rect(window, self.color, pygame.Rect(self.rect[0], self.rect[1] - 10, self.rect[2], self.rect[3] + 20))
        pygame.draw.rect(window, self.color, pygame.Rect(self.rect[0] - 10, self.rect[1], self.rect[2] + 20, self.rect[3]))

        if self.rect.collidepoint(mousepos) and mousebuttonup:
            return True