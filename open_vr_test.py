import openvr
import time
import matplotlib.pyplot as plt
import json
from scipy.spatial.transform import Rotation as R
import numpy as np


FPS = 30


def initialize_vr_system():
    # Initialize the VR system
    vr_system = openvr.init(openvr.VRApplication_Background)
    return vr_system


def get_tracking_data(vr_system: openvr.IVRSystem):
    # Get the poses of all tracked devices
    poses = vr_system.getDeviceToAbsoluteTrackingPose(
        openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount)

    tracking_data = {}
    for device_index, pose in enumerate(poses):
        if pose.bDeviceIsConnected and pose.bPoseIsValid:
            matrix = pose.mDeviceToAbsoluteTracking
            position = (
                matrix[0][3],  # x
                matrix[1][3],  # y
                matrix[2][3]   # z
            )
            rotation = (
                [matrix[0][0], matrix[0][1], matrix[0][2]],
                [matrix[1][0], matrix[1][1], matrix[1][2]],
                [matrix[2][0], matrix[2][1], matrix[2][2]]
            )
            tracking_data[device_index] = {
                'position': position,
                'rotation': rotation
            }
    return tracking_data


def main():
    vr_system = initialize_vr_system()
    data_record = []
    poses = []

    try:
        while True:
            tracking_data = get_tracking_data(vr_system)
            data_record.append(tracking_data)
            for device_index, data in tracking_data.items():
                xyz = data['position']
                rot = R.from_matrix(data['rotation']).as_quat()
                if device_index == 3:
                    poses.append((xyz, rot))
                print(
                    f"Device {device_index}: Position: {xyz}, Rotation: {rot}"
                )
            time.sleep(1 / FPS)  # Adjust the sleep time as necessary
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        openvr.shutdown()

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        positions = [x[0] for x in poses]
        rotations = [x[1] for x in poses]

        # y and z are swapped and x is mirrored
        x_vals = [x[0] * -1 for x in positions]
        y_vals = [x[2] for x in positions]
        z_vals = [x[1] for x in positions]
        ax.scatter(x_vals, y_vals, z_vals, marker='o')
        ax.plot(x_vals, y_vals, z_vals, color="g")

        for pos, quat in zip(positions, rotations):
            x, y, z = pos[0] * -1, pos[2], pos[1]
            u, v, w = R.from_quat(quat).apply([1, 0, 0])
            ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True, color='r')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)

        with open('data_record.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data_record, indent=4))

        plt.show()


if __name__ == "__main__":
    main()
