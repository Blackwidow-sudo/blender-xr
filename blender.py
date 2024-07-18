import threading
import socket
import json
import functools

import bpy

scene = bpy.context.scene
cam = scene.camera


def update_cam(data):
    vec = [v for v in data.values()]
    cam.location = vec


def listen_udp(ip, port, event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    try:
        while not event.is_set():
            data, addr = sock.recvfrom(1024)
            motion_data = json.loads(data.decode())
            print(data)
    finally:
        print("Closing connection")
        sock.close()


def stop_listen(event):
    event.set()


HOST, PORT = 'localhost', 12345

stop_event = threading.Event()
thread = threading.Thread(target=listen_udp, args=(
    HOST, PORT, stop_event), daemon=True)
thread.start()

bpy.app.timers.register(functools.partial(
    stop_listen, stop_event), first_interval=10.0)
