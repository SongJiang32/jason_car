# INTRODUCTION:The SLAM algorithm used is cartographer
# Oher SLAM algorithm:
  GMAPPING:先使用里程计推算机器人的位移，然后通过雷达点云贴合障碍物轮廓修正里程计误差
  HECTOR MAPPING:直接将雷达点云贴合障碍物轮廓所得出的位移作为最终的定位结果,即map→scanmatcher_frame，他会迁就scanmatcher_frame与odom重合
  两者的区别:
  1.在gmapping中机器人的位移主要由里程计推算,激光雷达点云配准算法只是在修正里程计出现的误差。
  2.hector mapping输出map→base_footprint_link or base_link(下面简称为base)的tf的目的，不是为了修正里成绩误差，而是为了让base的位置始终和scammer_frame保持一致。
  hector mapping在定位过程中，丝毫不考虑里程计的数据，只使用雷达点云和障碍物配准的方法来进行定位，只不过为了rviz里能够显示地图和机器人模型。而输出了一段map→odom的tf,去抵消不断增长的里程计tf。好让base和scanmatcher_frame的位置始终保持一致。


# For the topic which outputs matrix information when you view
# You can add parameter --noarr, for instance:
$ rostopic echo /scan --noarr
$ rostopic echo /map--noarr


# GMAPPING PARAMETERS
wiki.ros.org/gmapping
# HECTOR MAPPING PARAMETERS
wiki.ros.org/hector_mapping