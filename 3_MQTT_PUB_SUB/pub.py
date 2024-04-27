from machine import Pin, PWM
import network
import time
import dht
import ujson
from umqtt.simple import MQTTClient
import sys


sensor = dht.DHT22(Pin(16))

MQTT_CLIENT_ID = "device-1"
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC = "sensor/weather"

SSID = "Wokwi-GUEST"
PASSWORD = ""


def on_connect_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    timeout = 10
    start_time = time.ticks_ms()

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)

        if time.ticks_diff(time.ticks_ms(), start_time) > timeout * 1000:
            print("\nFailed to connect to WiFi. Exiting.")
            sys.exit(1)

    print("\nConnected!")


def on_connect_mqtt():
    print("Connecting to MQTT server... ")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    try:
        client.connect()
        print("Connected to server")
        return client
    except Exception as err:
        print("failed to connect MQTT server :", err)


def publish_message(client):
    sensor.measure()
    message = ujson.dumps({
        "temperature": sensor.temperature(),
        "humidity" : sensor.humidity()
    })
    client.publish(MQTT_TOPIC, message, qos=0)
    print(f"data report with topic {MQTT_TOPIC} : {message}")


if __name__ == '__main__':
    on_connect_wifi()
    mqttc = on_connect_mqtt()
    while True:
        publish_message(mqttc)
        time.sleep(1)
