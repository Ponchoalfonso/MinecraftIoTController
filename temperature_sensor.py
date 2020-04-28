import sys
import time
from grove.factory import Factory


class GroveTemperatureSensor:

    def __init__(self, pin):
        self.__pin = pin
        self.__sensor = Factory.getTemper("NTC-ADC", pin)

    @property
    def value(self):
        return self.__sensor.temperature


def main():
    pin = 0

    sensor = GroveTemperatureSensor(pin)

    print('Detecting temperature...')
    while True:
        print('{} Celsius'.format(sensor.value))
        time.sleep(1)


if __name__ == '__main__':
    main()
