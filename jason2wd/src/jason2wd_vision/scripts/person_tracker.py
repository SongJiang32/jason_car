# !/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
import os

class PersonFollower:
    def __init__(self):
        rospy.init_node('person_follower', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.image_callback)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        # 加载 YOLO 模型
        weights_path = os.path.expanduser("~/yan23_ws/src/yan23_vision/dl/yolov3/yolov3.weights")
        config_path = os.path.expanduser("~/yan23_ws/src/yan23_vision/dl/yolov3/yolov3.cfg")
        names_path = os.path.expanduser("~/yan23_ws/src/yan23_vision/dl/yolov3/coco.names")

        print(f"Loading YOLO model from: {weights_path} and {config_path}")
        try:
            self.net = cv2.dnn.readNet(weights_path, config_path)
            self.layer_names = self.net.getLayerNames()
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            with open(names_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
            print("YOLO model loaded successfully")
        except Exception as e:
            rospy.logerr(f"Failed to load YOLO model: {e}")
            self.net = None

        print("PersonTracker initialized.")

    def image_callback(self, msg):
        if not hasattr(self, 'net') or self.net is None:
            rospy.logwarn("YOLO model is not loaded")
            return

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        height, width, channels = cv_image.shape

        # YOLO 模型预测
        blob = cv2.dnn.blobFromImage(cv_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                if len(detection) > 0 and detection.ndim == 2:
                    for obj in detection:
                        if len(obj) >= 7:
                            center_x = int(obj[0] * width)
                            center_y = int(obj[1] * height)
                            w = int(obj[2] * width)
                            h = int(obj[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)

                            confidence = obj[4]
                            class_scores = obj[5:]
                            class_id = np.argmax(class_scores)
                            if confidence > 0.5 and self.classes[class_id] == "person":
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        cmd = Twist()
        detected_person = False

        if len(indexes) > 0:
            i = indexes.flatten()[0]
            x, y, w, h = boxes[i]
            center_x = x + w // 2
            center_y = y + h // 2

            # 绘制检测框和标签
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            label = f"{self.classes[class_ids[i]]}: {confidences[i]:.2f}"
            cv2.putText(cv_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            detected_person = True
            frame_center_x = width // 2
            frame_center_y = height // 2
            
            error_x = center_x - frame_center_x
            error_y = center_y - frame_center_y

            cmd.linear.x = 0.5
            cmd.angular.z = -error_x * 0.001

        if not detected_person:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5

        self.cmd_pub.publish(cmd)

        # 显示图像
        cv2.imshow("Person Tracker", cv_image)
        cv2.waitKey(1)

    def shutdown(self):
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        person_follower = PersonFollower()
        rospy.spin()
    except rospy.ROSInterruptException:
        person_follower.shutdown()