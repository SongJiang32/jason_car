cmake_minimum_required(VERSION 2.8.3)
project(jason2wd_description)

find_package(catkin REQUIRED COMPONENTS
  robot_state_publisher
  rviz
  joint_state_publisher
  gazebo_ros
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
