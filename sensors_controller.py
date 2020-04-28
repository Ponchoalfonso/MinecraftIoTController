import paho.mqtt.client as mqtt
import time
import sys
from touch_sensor import GroveTouchSensor
from sound_sensor import GroveSoundSensor
from temperature_sensor import GroveTemperatureSensor
from light_sensor import GroveLightSensor

# The Grove shield pin configuration
# Modify this if sensors pin was changed
sensor_pins = {
    "temperature": 0,
    "sound": 2,
    "touch": 12,
    "light": 4,
}


def on_connect(client, userdata, flags, rc):
    """The MQTT on connect handler"""
    if rc == 0:
        print(f"MQTT Client[code {rc}]: Connection established!")
    elif rc > 0:
        print(f"MQTT Client[code {rc}]: Connection refused!")

        print("\nQuitting controller...")
        sys.exit(1)


def init_mqttt_client(host):
    """Creates a new MQTT client"""
    print(f"Connecting to MQTT broker in: {host}")

    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(host)
    client.loop_start()

    return client


def init_sensors():
    """Creates a dictionary that holds several sensor instances"""
    sensors = {
        "temperature": GroveTemperatureSensor(sensor_pins["temperature"]),
        "sound": GroveSoundSensor(sensor_pins["sound"]),
        "touch": GroveTouchSensor(sensor_pins["touch"]),
        "light": GroveLightSensor(sensor_pins["light"])
    }

    return sensors


def main():
    """The main executed function of this file"""
    # Validating usage
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <mqtt_host>")
        sys.exit(1)

    # Grabbing values from arguments
    verbose = False  # Verbose output
    if len(sys.argv) > 2:
        verbose = sys.argv[2] == "-v" or sys.argv[2] == "--verbose"
    mqtt_broker = sys.argv[1]  # MQTT broker host address

    # Welcome message
    print("Minecraft IoT Controller!\n")

    # Initialize client and sensors
    mqtt_client = init_mqttt_client(mqtt_broker)
    print("Initializing sensors")
    sensors = init_sensors()

    # Touch handling
    def touch_handler():
        topic, value = "minecraft/sensors/touch", True
        mqtt_client.publish(topic, value)

        if verbose:
            print(f"{topic}: {value}")

    print("Data is now being published!")
    sensors["touch"].on_press = touch_handler

    # All the sensors but touch sensor are handled every second
    while True:
        for sensor_name in sensors:
            if sensor_name != "touch":
                sensor_value = sensors[sensor_name].value
                topic = f"minecraft/sensors/{sensor_name}"

                mqtt_client.publish(topic, str(sensor_value))

                if verbose:
                    print(f"{topic}: {sensor_value}")

        time.sleep(1)


if __name__ == "__main__":
    main()
