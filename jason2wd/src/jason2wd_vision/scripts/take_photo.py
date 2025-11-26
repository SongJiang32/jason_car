#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class CameraPublisher:
    def __init__(self):
        # 初始化 ROS 节点
        rospy.init_node('camera_publisher', anonymous=True)

        # 初始化 CV Bridge
        self.bridge = CvBridge()

        # 创建一个 Publisher，用于发布图像消息
        self.image_pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

        # 打开相机，0 表示默认摄像头
        self.cap = cv2.VideoCapture(0)

        # 设置摄像头分辨率为 1920x1080
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
        # 设置帧率为 30
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        if not self.cap.isOpened():
            rospy.logerr("Unable to open camera")
            rospy.signal_shutdown("Unable to open camera")

    def publish_images(self):
        rate = rospy.Rate(30)  # 设置发布频率为 30 Hz
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if not ret:
                rospy.logwarn("Failed to grab frame")
                continue

            try:
                # 将 OpenCV 图像转换为 ROS 图像消息
                ros_image = self.bridge.cv2_to_imgmsg(frame, "bgr8")
                # 发布图像消息
                self.image_pub.publish(ros_image)

                # 实时显示图像
                cv2.imshow("Camera Feed", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except CvBridgeError as e:
                rospy.logerr(f"CvBridge Error: {e}")

            rate.sleep()

    def shutdown(self):
        # 释放摄像头资源
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        camera_publisher = CameraPublisher()
        camera_publisher.publish_images()
    except rospy.ROSInterruptException:
        camera_publisher.shutdown()