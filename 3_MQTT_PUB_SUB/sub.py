import json
import logging
import sys
import time
import uuid

import paho.mqtt.client as mqttc
import mysql.connector as mysql


DATABASE_URL = "localhost"
DATABASE_USER = "root"
DATABASE_PASSWORD = "Makananku123-"
DATABASE_NAME = "monitoring"

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "sensor/weather"
CLIENT_ID = str(uuid.uuid4())

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False


def on_connect_database():
    try:
        database = mysql.connect(
            host=DATABASE_URL,
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        return database
    except Exception as err:
        logging.error(err)


def on_save(database, data):
    sql = "insert into weather (topic, humidity, temperature) values (%s, %s, %s)"

    db = database.cursor()
    try:
        topic = data.topic
        payload = data.payload.decode("utf-8")
        value = json.loads(payload)
        params = (topic, value['humidity'], value['temperature'])
        db.execute(sql, params)
    except Exception as err:
        logging.error(err)
    database.commit()
    database.close()


def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        logging.info("Connected to MQTT Broker!")
        client.subscribe(TOPIC, qos=0)
    else:
        logging.error(f'Failed to connect, return code {rc}')


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True


def on_message(client, userdata, msg):
    logging.info(f"Received Topic {msg.topic} : {msg.payload.decode()}")
    db = on_connect_database()
    on_save(db, msg)


def connect_mqtt():
    client = mqttc.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=120)
    client.on_disconnect = on_disconnect
    return client


def run():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    on_connect_database()
    client = connect_mqtt()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run()
