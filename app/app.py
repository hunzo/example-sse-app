from flask import Flask, request
from flask.templating import render_template
from flask.wrappers import Response
import paho.mqtt.client as mqtt
import redis
import json
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_POST", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "thisispassword")
KEEP_ALIVE = 1

MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = os.environ.get("MQTT_POST", 1883)


app = Flask(__name__)

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=1,
    password=REDIS_PASSWORD
)

# MQTT


def init_redis():
    r.set("count", 0)
    r.set("control", "stop")
    print("initial redis...")


init_redis()


def on_connect(client, userdata, flags, rc):
    print(f"Connect with result {rc}")
    TOPIC = [("test/count", 0), ("status/control", 0)]
    # client.subscribe("test/count")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    if str(msg.payload.decode("utf-8")) == "inc":
        print("Redis: Count")
        r.decr("count")
        # r.incr("count")

    if str(msg.payload.decode("utf-8")) == "start":
        print("Redis Control: Start")
        r.set("control", "start")

    if str(msg.payload.decode("utf-8")) == "stop":
        print("Redis Control: Stop")
        r.set("control", "stop")


def on_subscribe(mosq, obj, mid, granted_qos):
    print(f"Start Subscribed with Qos: {granted_qos}")


def on_publish(client, userdata, mid):
    print(f"Publish message sequence ... {mid}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish
client.username_pw_set(username="mosquitto", password="mosquitto")
client.connect(
    host=MQTT_HOST,
    port=MQTT_PORT,
    keepalive=KEEP_ALIVE
)
client.loop_start()
# client.loop_forever()
# Flask


@app.get("/")
def index():
    key = request.args.get("key")
    if key != "test":
        return "invalid token"
    return render_template("index.html")


@app.get("/stream")
def stream():
    def get_data():
        while True:
            # time.sleep(0.5)
            count = r.get("count")
            control = r.get("control")
            ret = {
                "count": count.decode("utf-8"),
                "control": control.decode("utf-8")
            }

            yield f'data: {json.dumps(ret)}\n\n'

    return Response(get_data(), mimetype='text/event-stream')


# MQTT


@app.post("/start")
def start():
    client.publish("api/control", "start")
    ret = {
        "sever status": "Publish Messages start"
    }
    return ret


@app.post("/stop")
def stop():
    client.publish("api/control", "stop")
    ret = {
        "sever status": "Publish Messages stop"
    }
    return ret

# Redis


@app.post("/increase")
def increase():
    r.incr("count")
    return {
        "status": "increase"
    }


@app.post("/decrease")
def decrease():
    r.decr("count")
    return {
        "status": "decrease"
    }


@app.post("/reset")
def reset_counter():
    r.set("count", 0)
    return {
        "status": "reset"
    }


@app.post("/set/<num>")
def set_counter(num):
    r.set("count", num)
    return {
        "status": num,
    }


# client.loop_stop()
