import Led
from Led import *


class colorchange:
    def __init__(self):
        self.LED = Led()

    def run(self, last):
        while True:
            if last == 'red':
                for i in range(self.LED.strip.numPixels()):
                    self.LED.strip.setPixelColor(i, Color(255, 0, 0))
                    self.LED.strip.show()
            elif last == 'green':
                for i in range(self.LED.strip.numPixels()):
                    self.LED.strip.setPixelColor(i, Color(0, 255, 0))
                    self.LED.strip.show()
            elif last == 'blue':
                for i in range(self.LED.strip.numPixels()):
                    self.LED.strip.setPixelColor(i, Color(0, 0, 255))
                    self.LED.strip.show()
            elif last == 'yellow':
                for i in range(self.LED.strip.numPixels()):
                    self.LED.strip.setPixelColor(i, Color(0, 255, 255))
                    self.LED.strip.show()

    def destroy(self):
         for i in range(self.LED.strip.numPixels()):
                self.LED.strip.setPixelColor(i, Color(0, 0, 0))
                self.LED.strip.show()

thing = colorchange()
if __name__ == '__main__':
    try:
        thing.run('red')
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        thing.destroy()
            




        