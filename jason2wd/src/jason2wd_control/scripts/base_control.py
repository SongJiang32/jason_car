#!/usr/bin/python3
# coding=utf-8

import rospy
import tf
import time
import sys
import math
import serial
import string
import ctypes
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from tf.transformations import euler_from_quaternion


class BaseControl:
    def __init__(self):
        self.device_port = rospy.get_param('~port','/dev/base')
        self.baudrate = int(rospy.get_param('~baudrate','115200'))
        self.cmd_vel_topic= rospy.get_param('~cmd_vel_topic','/cmd_vel')
        self.baseId = rospy.get_param('~base_id','base_footprint') 
        self.odomId = rospy.get_param('~odom_id','odom') 
        self.odom_freq = int(rospy.get_param('~odom_freq','50'))
        self.previous_time = None
        self.previous_linear_acceleration_x = None
        self.threshold = 0.1  # 设置阈值为 0.1 米/秒^2
        #data to calculate
        self.trans_x = 0.0
        self.trans_y = 0.0
        self.rotat_z = 0.0
        self.outData = bytearray([0x5A,0x0C,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])  # 将outputdata定义为类属性
        self.Vx = 0.0
        self.Vy = 0.0
        self.Vz = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0      #航向角
        self.pose_x = 0.0
        self.pose_y = 0.0 
        self.yaw_next = 0.0     #θ_{k+1}
        self.pose_x_next = 0.0      #x_{k+1}
        self.pose_y_next = 0.0      #y_{k+1}
        self.s = 0.0
        #data from imu
        self.angular_velocity_x = 0     
        self.angular_velocity_y = 0
        self.angular_velocity_z = 0
        self.linear_acceleration_x = 0
        self.linear_acceleration_y = 0
        self.linear_acceleration_z = 0
        self.orientation_x = 0             
        self.orientation_y = 0
        self.orientation_z = 0
        self.orientation_w = 1
        self.sub_imu = rospy.Subscriber('/IMU_data', Imu, self.imu_callback, queue_size=20)
        self.pub_odom = rospy.Publisher('/odom', Odometry, queue_size = 20)
        self.tf_broadcaster = tf.TransformBroadcaster()
        self.timer_odom = rospy.Timer(rospy.Duration(1.0/self.odom_freq),self.timerOdomCB)
        #this case is differential mode
        self.sub_cmd_vel = rospy.Subscriber(self.cmd_vel_topic,Twist,self.cmdCB,queue_size=20)
        # Serial Communication:串口通信部分：这部分的作用是打开机器人串口并连接到底盘上
        try:
            self.serial = serial.Serial(self.device_port,self.baudrate,timeout=10)
            rospy.loginfo("Opening Serial")
            try:
                if self.serial.in_waiting:
                    self.serial.readall()
            except:
                rospy.loginfo("Opening Serial Try Faild")
                pass
        except:
            rospy.logerr("Can not open Serial"+self.device_port)        #log error
            self.serial.close
            sys.exit(0)
        rospy.loginfo("Serial Open Succeed!")        #log information

    def cmdCB(self,msg):
        self.trans_x = msg.linear.x
        self.trans_y = msg.linear.y
        self.rotat_z = msg.angular.z
        # 判断self.trans_x的正负号，设置outputdata[3]的值
        if self.trans_x >= 0:
            self.outData[3] = 0x2B  # 如果是正数，设置为0x2B
        else:
            self.outData[3] = 0x2D  # 如果是负数，设置为0x2D
        if self.trans_y >= 0:
            self.outData[6] = 0x2B  
        else:
            self.outData[6] = 0x2D  
        if self.rotat_z >= 0:
            self.outData[9] = 0x2B  
        else:
            self.outData[9] = 0x2D 
        self.outData[4] = abs(int((self.trans_x*1000)/100))
        self.outData[5] = abs(int((self.trans_x*1000)%100))
        self.outData[7] = abs(int((self.trans_y*1000)/100))
        self.outData[8] = abs(int((self.trans_y*1000)%100))
        self.outData[10] = abs(int((self.rotat_z*1000)/100))
        self.outData[11] = abs(int((self.rotat_z*1000)%100))
        self.output = bytearray([0x5A,0x0C,0x01,self.outData[3],self.outData[4],self.outData[5],self.outData[6],self.outData[7],self.outData[8],self.outData[9],self.outData[10],self.outData[11]])
        # print(self.output)
        try:
            while self.serial.out_waiting:
                pass
            self.serial.write(self.output)
        except:
            rospy.logerr("Vel Command Send Faild")

    def imu_callback(self, data):        
        # analysis the header information
        header = data.header
        self.seq = header.seq
        self.timestamp = header.stamp
        self.frame_id = header.frame_id
        # 解析姿态、角速度和线性加速度信息
        self.orientation_x = data.orientation.x
        self.orientation_y = data.orientation.y
        self.orientation_z = data.orientation.z
        self.orientation_w = data.orientation.w
        self.angular_velocity_x = data.angular_velocity.x * 0.1 * math.pi / 180        # 原始数据单位0.1°/s
        self.angular_velocity_y = data.angular_velocity.y * 0.1 * math.pi / 180
        self.angular_velocity_z = data.angular_velocity.z * 0.1 * math.pi / 180
        self.linear_acceleration_x = data.linear_acceleration.x         # 单位0.001g
        self.linear_acceleration_y = data.linear_acceleration.y 
        self.linear_acceleration_z = data.linear_acceleration.z 
        # transform quaternion to euler angle
        quaternion = (self.orientation_x, self.orientation_y, self.orientation_z, self.orientation_w)
        euler_angles = euler_from_quaternion(quaternion)
        self.yaw = euler_angles[2]      # 从欧拉角中提取航向角（yaw），在ROS中，通常航向角对应欧拉角的第三个元素
        # calculate self for odom
        self.current_time = rospy.Time.now()        # self.current_time = timestamp.secs + timestamp.nsecs * 1e-9
        if self.previous_time is not None:
            dt = (self.current_time - self.previous_time).to_sec()
        if self.previous_linear_acceleration_x is not None:       
            if abs(self.linear_acceleration_x) < self.threshold:  
                self.Vx = 0.0  
            else:
                self.Vx += ((self.linear_acceleration_x + self.previous_linear_acceleration_x) / 2) * dt
        self.previous_linear_acceleration_x = self.linear_acceleration_x
        self.previous_time = self.current_time
        # print("yaw:", self.yaw)
        # print("angular_velocity_z:", self.angular_velocity_z)
        # print("Vx:", self.Vx)

    def timerOdomCB(self,event):
        self.current_time = rospy.Time.now()
        if self.previous_time is not None:
            Ts = (self.current_time - self.previous_time).to_sec()     #Sampling interval time
            self.yaw_next = self.yaw + self.angular_velocity_z * Ts  
            if self.angular_velocity_z != 0:
                self.pose_x_next = self.pose_x + self.Vx * (math.sin(self.yaw_next) - math.sin(self.yaw)) / self.angular_velocity_z
                self.pose_y_next = self.pose_y - self.Vx * (math.cos(self.yaw_next) - math.cos(self.yaw)) / self.angular_velocity_z
            else:
                self.pose_x_next = self.pose_x + self.Vx * math.cos(self.yaw)
                self.pose_y_next = self.pose_y + self.Vx * math.sin(self.yaw)
        self.s += math.sqrt((self.pose_x_next - self.pose_x)**2 + (self.pose_y_next - self.pose_y)**2)  # total distance
        # update for next calculate 
        self.yaw = self.yaw_next
        self.pose_x = self.pose_x_next
        self.pose_y = self.pose_y_next
        self.previous_time = self.current_time
        # the information under the command "rostopic echo odom"
        msg = Odometry()
        msg.header.stamp = self.current_time
        msg.header.frame_id = self.odomId
        # msg.child_frame_id = self.baseId
        msg.pose.pose.position.x = self.pose_x      # pose字段本身是一个geometry_msgs/PoseWithCovariance类型的消息，包含了机器人的位姿信息，.pose表示访问Odometry消息中的pose字段，.pose之后的.position表示访问geometry_msgs/PoseWithCovariance消息中的position字段，最后.x表示你在访问该position字段中的x坐标值
        msg.pose.pose.position.y = self.pose_y
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.x = self.orientation_x
        msg.pose.pose.orientation.y = self.orientation_y
        msg.pose.pose.orientation.z = self.orientation_z
        msg.pose.pose.orientation.w = self.orientation_w
        # msg.twist.twist.linear.x = 
        # msg.twist.twist.linear.y = 
        # msg.twist.twist.angular.x = 
        self.pub_odom.publish(msg)
        self.tf_broadcaster.sendTransform((self.pose_x_next, self.pose_y_next, 0.0), 
                                          (self.orientation_x, self.orientation_y, self.orientation_z, self.orientation_w), 
                                           self.current_time, self.baseId, self.odomId)
        # print("yaw:",self.yaw)
        # print("pose_x:",self.pose_x)
        # print("pose_y:",self.pose_y)
        # print("s:",self.s)
        

        



if __name__=="__main__":
    try:
        rospy.init_node('base_control',anonymous=True)
        bc = BaseControl()
        bc.sub_cmd_vel
        bc.sub_imu
        bc.timer_odom
        bc.pub_odom
        rospy.spin()
    except KeyboardInterrupt:
        bc.serial.close
        print("Shutting down")



