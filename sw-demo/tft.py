from ST7735 import TFT, TFTColor

def init_tfts(tft1, tft2):
  ## init
  tft1.initr()
  tft1.rgb(True)
  tft1.invertcolor(True)
  tft1.fill(TFT.BLACK)
  tft2.initr()
  tft2.rgb(True)
  tft2.invertcolor(True)
  tft2.fill(TFT.BLACK)

# TODO: The one corner is not at [0,0]; make this a paramter (?)
def tft_splash(tft1, tft2):
  print("SPI TFT display rectangles")
  # tft1
  tft1.rect([26,1], [80,160], TFT.PURPLE)
  tft1.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
  tft1.fillrect([40,50], [25,15], TFT.RED)
  tft1.fillrect([50,70], [25,15], TFT.BLUE)
  tft1.fillrect([60,90], [25,15], TFT.GREEN)
  tft1.fillrect([85,140], [20,20], TFTColor(123, 111, 42))

  # tft2
  tft2.rect([26,1], [80,160], TFT.PURPLE)
  tft2.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
  tft2.fillrect([40,50], [25,15], TFT.GREEN)
  tft2.fillrect([50,70], [25,15], TFT.RED)
  tft2.fillrect([60,90], [25,15], TFT.BLUE)
  tft2.fillrect([85,140], [20,20], TFTColor(123, 111, 42))
