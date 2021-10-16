# tls.py Test of asynchronous mqtt client with SSL for Pyboard D. Tested OK.

# (C) Copyright Peter Hinch 2017-2019.
# Released under the MIT licence.

# This demonstrates bidirectional TLS communication.
# You can also run the following on a PC to verify:
# mosquitto_sub -h test.mosquitto.org -t yoloyolowoopwoop
# I haven't yet figured out how to get mosquitto_sub to use a secure connection.

# Public brokers https://github.com/mqtt/mqtt.github.io/wiki/public_brokers

from machine import Pin
from micropython_mqtt_as.mqtt_as import MQTTClient
from micropython_mqtt_as.config import config
#from mqtt_as import MQTTClient, config
import uasyncio as asyncio

# Define configuration
config['ssid'] = 'NSA@home'
config['wifi_pw'] = '23.stePARANOIA42'
config['server'] = 'test.mosquitto.org'
config['ssl'] = True

topic = 'yoloyolowoopwoop'

led = Pin(4, Pin.OUT)

loop = asyncio.get_event_loop()

# Subscription callback
async def flash(count, time):
    for x in range(0, count):
        led.value(1)
        await asyncio.sleep_ms(time)
        led.value(0)

def sub_cb(topic, msg, retained):
    c, r = [int(x) for x in msg.decode().split(' ')]
    print('Topic = {} Count = {} Retransmissions = {} Retained = {}'.format(topic.decode(), c, r, retained))
    loop.create_task(flash(2, 100))

# Demonstrate scheduler is operational and TLS is nonblocking.
async def heartbeat():
    while True:
        await flash(1, 500)

async def wifi_han(state):
    if state:
        await flash(1, 200)
    else:
        await flash(1, 50)
    print('Wifi is ', 'up' if state else 'down')
    await asyncio.sleep(1)

# If you connect with clean_session True, must re-subscribe (MQTT spec 3.1.2.4)
async def conn_han(client):
    await client.subscribe(topic, 1)

async def main(client):
    await client.connect()
    n = 0
    await asyncio.sleep(2)  # Give broker time
    while True:
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish(topic, '{} {}'.format(n, client.REPUB_COUNT), qos = 1)
        n += 1
        await asyncio.sleep(20)  # Broker is slow

# Set up client
config['subs_cb'] = sub_cb
config['connect_coro'] = conn_han
config['wifi_coro'] = wifi_han
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(**config)

loop.create_task(heartbeat())
try:
    loop.run_until_complete(main(client))
finally:
    client.close()
