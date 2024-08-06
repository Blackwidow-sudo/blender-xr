import openvr
import time


def initialize_vr_system():
    # Initialize the VR system
    vr_system = openvr.init(openvr.VRApplication_Scene)
    return vr_system


def get_tracking_data(vr_system):
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
                matrix[0][0], matrix[0][1], matrix[0][2],
                matrix[1][0], matrix[1][1], matrix[1][2],
                matrix[2][0], matrix[2][1], matrix[2][2]
            )
            tracking_data[device_index] = {
                'position': position,
                'rotation': rotation
            }
    return tracking_data


def main():
    vr_system = initialize_vr_system()

    try:
        while True:
            tracking_data = get_tracking_data(vr_system)
            for device_index, data in tracking_data.items():
                print(f"Device {device_index}: Position: {
                      data['position']}, Rotation: {data['rotation']}")
            time.sleep(1)  # Adjust the sleep time as necessary
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        openvr.shutdown()


if __name__ == "__main__":
    main()
