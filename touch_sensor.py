import time
from grove.gpio import GPIO


class GroveTouchSensor(GPIO):

    def __init__(self, pin):
        super(GroveTouchSensor, self).__init__(pin, GPIO.IN)

        self._on_press = None
        self._on_release = None

    @property
    def on_press(self):
        return self._on_press

    @on_press.setter
    def on_press(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_press = callback

    @property
    def on_release(self):
        return self._on_release

    @on_release.setter
    def on_release(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_release = callback

    def _handle_event(self, pin, value):
        if value:
            if callable(self._on_press):
                self._on_press()
        else:
            if callable(self._on_release):
                self._on_release()


def main():
    import sys

    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
        sys.exit(1)

    touch = GroveTouchSensor(int(sys.argv[1]))

    def on_press():
        print('Pressed')

    def on_release():
        print("Released.")

    touch.on_press = on_press
    touch.on_release = on_release

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
