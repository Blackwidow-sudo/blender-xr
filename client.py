import socket
import json
import time


HOST, PORT = 'localhost', 12345

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the address and port
sock.bind((HOST, PORT))

try:
    print("Listening for motion data...")
    while True:
        # Receive motion data
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        motion_data = json.loads(data.decode())
        xyz, rot = [v for v in motion_data.values()]
        print(f"Received motion data from {addr}: {xyz}@{rot}")
finally:
    # Close the socket
    sock.close()
