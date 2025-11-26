#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class CmdVelSubscriber:
    def __init__(self):
        # 初始化 ROS 节点
        rospy.init_node('cmd_vel_subscriber', anonymous=True)
        
        # 创建订阅者
        self.cmd_vel_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        
        # 设置节点运行的频率
        self.rate = rospy.Rate(10)  # 10 Hz

    def cmd_vel_callback(self, msg):
        # 处理接收到的 Twist 消息
        rospy.loginfo("Received cmd_vel message:")
        rospy.loginfo(f"Linear x: {msg.linear.x}")
        rospy.loginfo(f"Linear y: {msg.linear.y}")
        rospy.loginfo(f"Linear z: {msg.linear.z}")
        rospy.loginfo(f"Angular x: {msg.angular.x}")
        rospy.loginfo(f"Angular y: {msg.angular.y}")
        rospy.loginfo(f"Angular z: {msg.angular.z}")

    def spin(self):
        # 使节点保持活动状态
        rospy.spin()

if __name__ == '__main__':
    try:
        # 创建 CmdVelSubscriber 实例并运行
        cmd_vel_subscriber = CmdVelSubscriber()
        cmd_vel_subscriber.spin()
    except rospy.ROSInterruptException:
        pass
