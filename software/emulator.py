import sys
import pygame

class FrameBuffer:
    'Framebuffer as in http://docs.micropython.org/en/latest/library/framebuf.html'

    def __init__(self, buffer, width, height, format=None):
        self.buffer = buffer
        self.width = width
        self.height = height
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
        self.draw:ImageDraw.ImageDraw = None
        pygame.init()
        self.virt_screen = pygame.Surface((width, height))
        self.display:pygame.Surface = pygame.display.set_mode(
            (2*width,2*height), pygame.RESIZABLE)

    def fill(self, c):
        self.fill_rect(0,0, self.width, self.height, c)

    def pixel(self, x, y, c=None):
        self.virt_screen.set_at((x,y), c)

    def hline(self, x, y, w, c):
        self.line(x,y, x+w, y, c)

    def vline(self, x, y, h, c):
        self.line(x,y,x,y+h, c)
        
    def line(self, x1, y1, x2, y2, c):
        pygame.draw.line(self.virt_screen, c, (x1,y1), (x2,y2))

    def rect(self, x, y, w, h, c):
        pygame.draw.rect(self.virt_screen, c, (x,y,w,h), width=1)

    def fill_rect(self, x, y, w, h, c):
        pygame.draw.rect(self.virt_screen, c, (x,y,w,h), width=0)

    def text(self, s, x, y, c=None):
        fontsize = 10
        font = pygame.font.Font(pygame.font.get_default_font(), fontsize)
        antialias = True
        surf = font.render(s, antialias, c)
        self.virt_screen.blit(surf, (x,y))

    def scroll(self, xstep, ystep):
        self.virt_screen.scroll(xstep, ystep)
    
    def blit(self, fbuf, x, y, key=None):
        #assert False, "Not Implemented"
        self.virt_screen.blit(fbuf.virt_screen, (x,y))


class SSD1306(FrameBuffer):
    'taken from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py'

    def __init__(self, width=128, height=64, external_vcc=None):
        self.external_vcc = external_vcc
        self.pages = height // 8
        buffer = bytearray(self.pages * width)
        super().__init__(buffer, width, height)

    def show(self):
        # clear event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # upscale the image        
        pygame.transform.scale(
            self.virt_screen, self.display.get_size(), self.display)
        pygame.display.flip()

class SSD1306_I2C(SSD1306):
    def __init__(self, width=128, height=64, i2c=None, addr=0x3C, external_vcc=False):
        super().__init__(width, height, external_vcc)
        self.i2c = i2c