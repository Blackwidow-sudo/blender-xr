# Blender XR

This is a collection of helpful python scripts to experiment with XR (Extended Reality) in Blender.

## server.py

This file contains a simple UDP server that emulates motion data around an object in the center of the scene.

## motion_track.blend

This file is a file for blender which contains a script that listens to the server that was mentioned above.
According to the broadcasted motion data from the server, the camera will be updated on the XYZ axis.
Additionally the server will send random rotation data.

### Debugging in Blender

Debugging python scripts and outputting print statements in blender is only possible if you start the project from the terminal.

For example with (on a Arm Mac):

```
/Applications/Blender.app/Contents/MacOS/Blender ai/blender-xr/motion_track.blend 
```