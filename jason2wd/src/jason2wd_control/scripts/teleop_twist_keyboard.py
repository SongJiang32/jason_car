#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# 速度参数
linear_vel = 0.1    # 线速度（m/s）
angular_vel = 0.2   # 角速度（rad/s）

def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    global settings
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('keyboard_control_node')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    twist_msg = Twist()
    twist_msg.linear.x = 0.0
    twist_msg.angular.z = 0.0

    print("键盘控制两轮差速小车：")
    print("w - 前进")
    print("s - 后退")
    print("a - 左转")
    print("d - 右转")
    print("x - 刹车")
    print("q - 退出")
    print("-------------")

    try:
        while not rospy.is_shutdown():
            key = get_key()

            if key == 'w':
                twist_msg.linear.x += linear_vel
                twist_msg.angular.z = 0.0
            elif key == 's':
                twist_msg.linear.x += -linear_vel
                twist_msg.angular.z = 0.0
            elif key == 'a':
                twist_msg.angular.z += angular_vel
                twist_msg.linear.x = 0.0
            elif key == 'd':
                twist_msg.angular.z += -angular_vel
                twist_msg.linear.x = 0.0
            elif key == 'x':
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
            elif key == 'q':
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                break

            pub.publish(twist_msg)

        twist_msg.linear.x = 0.0
        twist_msg.angular.z = 0.0
        pub.publish(twist_msg)

    except Exception as e:
        print(e)

    finally:
        twist_msg.linear.x = 0.0
        twist_msg.angular.z = 0.0
        pub.publish(twist_msg)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
