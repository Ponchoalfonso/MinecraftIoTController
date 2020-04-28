import math
import sys
import time
from grove.adc import ADC


class GroveSoundSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def value(self):
        value = self.adc.read(self.channel)
        return value


def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)

    sensor = GroveSoundSensor(int(sys.argv[1]))

    print('Detecting sound...')
    while True:
        print('Sound value: {0}'.format(sensor.value))
        time.sleep(.3)


if __name__ == '__main__':
    main()
