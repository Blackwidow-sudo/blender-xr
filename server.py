"""Simple UDP server that broadcasts motion data to all clients on the network."""
import socket
import time
import json
import math
from random import uniform

DEBUG = False

HOST, PORT = 'localhost', 12345

SPEED = 0.5
RADIUS = 10.0


def calc_cam_position(speed, radius, elapsed_time):
    """Calculate the motion of the object."""
    angle = speed * elapsed_time
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = 2.5 * math.sin(speed * elapsed_time) + 7.5

    return (x, y, z)


def run_server(ip, port):
    """Run the server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time

            xyz = calc_cam_position(SPEED, RADIUS, elapsed_time)

            rot = (uniform(-180, 180), uniform(-180, 180), uniform(-180, 180))

            motion_data = json.dumps({"xyz": xyz, "rot": rot})
            sock.sendto(motion_data.encode(), (ip, port))
            if DEBUG:
                print(f"Broadcasted motion data: {motion_data}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Closing connection")
    finally:
        # Close the socket
        sock.close()


if __name__ == "__main__":
    run_server(HOST, PORT)
