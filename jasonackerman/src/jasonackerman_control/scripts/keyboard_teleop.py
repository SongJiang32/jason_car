#!/usr/bin/env python3

# Copyright (c) 2019, The Personal Robotics Lab, The MuSHR Team, The Contributors
# License: BSD 3-Clause. See LICENSE.md file in root directory.

import atexit
import os
import signal
from threading import Lock
from tkinter import Frame, Label, Tk

import rospy
from ackermann_msgs.msg import AckermannDriveStamped

# Key mappings
UP = "w"
LEFT = "a"
DOWN = "s"
RIGHT = "d"
QUIT = "q"

# Global state variables
state = [False, False, False, False]
state_lock = Lock()
state_pub = None
root = None
control = False


def keyeq(e, c):
    """Check if the key event matches the given key."""
    return e.char == c or e.keysym == c


def keyup(e):
    """Handle key release events."""
    global state, control

    with state_lock:
        if keyeq(e, UP):
            state[0] = False
        elif keyeq(e, LEFT):
            state[1] = False
        elif keyeq(e, DOWN):
            state[2] = False
        elif keyeq(e, RIGHT):
            state[3] = False
        control = sum(state) > 0


def keydown(e):
    """Handle key press events."""
    global state, control

    with state_lock:
        if keyeq(e, QUIT):
            shutdown()
        elif keyeq(e, UP):
            state[0] = True
            state[2] = False
        elif keyeq(e, LEFT):
            state[1] = False
            state[3] = True
        elif keyeq(e, DOWN):
            state[0] = False
            state[2] = True
        elif keyeq(e, RIGHT):
            state[1] = True
            state[3] = False
        control = sum(state) > 0


def publish_cb(_):
    """Publish the Ackermann command based on the current state."""
    with state_lock:
        if not control:
            return
        ack = AckermannDriveStamped()
        ack.drive.speed = 0.0
        ack.drive.steering_angle = 0.0

        if state[0]:
            ack.drive.speed = max_velocity
        elif state[2]:
            ack.drive.speed = -max_velocity

        if state[1]:
            ack.drive.steering_angle = max_steering_angle
        elif state[3]:
            ack.drive.steering_angle = -max_steering_angle

        if state_pub is not None:
            state_pub.publish(ack)


def shutdown():
    """Handle shutdown events."""
    if root:
        root.destroy()
    rospy.signal_shutdown("shutdown")


def main():
    """Main function to initialize ROS and Tkinter."""
    global state_pub, root, max_velocity, max_steering_angle

    rospy.init_node("keyboard_teleop", disable_signals=True)

    # Read parameters
    max_velocity = rospy.get_param("~speed", 2.0)
    max_steering_angle = rospy.get_param("~max_steering_angle", 0.6)

    # ROS publisher
    state_pub = rospy.Publisher("/ackermann_cmd_mux/output", AckermannDriveStamped, queue_size=1)
    rospy.Timer(rospy.Duration(0.1), publish_cb)

    # Tkinter setup
    root = Tk()
    frame = Frame(root, width=100, height=100)
    frame.bind("<KeyPress>", keydown)
    frame.bind("<KeyRelease>", keyup)
    frame.pack()
    frame.focus_set()

    lab = Label(
        frame,
        height=10,
        width=30,
        text="""Focus on this window
and use the WASD keys
to drive the car.""",
    )
    lab.pack()

    print(f"Press '{QUIT}' to quit")
    root.mainloop()


if __name__ == "__main__":
    # Set up signal handler
    signal.signal(signal.SIGINT, lambda s, f: shutdown())
    main()