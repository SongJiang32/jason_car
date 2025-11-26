#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

void Cam_RGB_Callback(const sensor_msgs::ImageConstPtr& msg)
{
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
        cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return;
    }
    
    Mat imgOriginal = cv_ptr->image;
    imshow("RGB", imgOriginal);
    waitKey(1); // Wait for 1 ms to process events and display the image
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "cv_image");

    ros::NodeHandle nh;
    ros::Subscriber rgb_sub = nh.subscribe("/camera/color/image_raw", 1, Cam_RGB_Callback);

    namedWindow("RGB", WINDOW_AUTOSIZE); // Create window with autosize property
    ros::spin(); // Enter the ROS event loop

    destroyWindow("RGB"); // Clean up the window after exiting ROS spin
    return 0;
}



