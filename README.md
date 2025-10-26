# 两轮差速 & 阿克曼

## Compile after Preparation

```
cd jason_ws && catkin build
```

## Preparation

```
wget http://fishros.com/install -O fishros && . fishros
sudo rosdepc init
rosdepc update
rosdepc install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} -y
```

> IF SHOW "cartographer: [libabsl-dev] defined as "not available" for OS version [focal]"
> 
> THEN 在文件 cartographer_ws/src/cartographer/package.xmL 注释掉 <depend>libabsl-dev</depend> 并重新执行指令

```
rosdepc install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} -y
src/cartographer/scripts/install_abseil.sh
sudo apt-get install libgmock-dev
catkin_make_isolated --install --use-ninja
```

> [!NOTE]
> Before each use

```
cd cartographer_ws
source install_isolated/setup.bash
```

> ONCE YOU CHANGING THE PARAMETERS OF <name>.lua
> Once you change the parameters of <name>.lua
```
cd cartographer_ws
catkin_make_isolated --install --use-ninja
source install_isolated/setup.bash
```

## About Cartographer

0 provide_odom_frame

0.1 carto建图时一定会有的map_frame也就是map的tf，建图时carto本质上能得到的一般是map与base_link之间的位置关系,因为激光雷达和imu的tf与base_link一般是固定的，map即它建得的地图固定坐标系，而描述位置关系在ROS中一般就直接是两个坐标系的tf

0.2 但是tf树是不能多个导向同一个的，会冲突，所以如果本身有坐标系指向base_link（比如odom、base_footprint_link这些），那么map要描述与base_link的位置关系就只能连到再上一层了（比如map→odom→base_link）

0.3 了解了这个基本机制之后，另外的两个配置参数只与这个开关参数有关，前面说了carto建图知道的是map与base_link之间的关系，但是由于tf树的机制并不是任意情况都能够直接用tf连接base_link与map的，而carto内部不知道你外部tf树的复杂情况，因此提供了这两个参数要求你手动定义

0.4 首先说明published_frame参数，这个参数理解为指定你要把map连接到哪个坐标系（因为不一定能够直接连base_link），假如base_link上面本身你已经有odom的tf连接着，那么这个published_frame就可以指定为odom，如果只是这样普通的情况，直接就这样设置，然后设置provide_odom_frame为false即可，即不需要carto提供odom的tf，因为我们本身有了，这种情况下
map就会直接连接published_frame

0.5 而假如我们没有odom的tf，而且我们希望carto能够给我们提供一个odom的tf（因为其实carto得到了这个信息），那么就将provide_odom_frame设置为true，同时odom_frame设置为你想要carto提供的odom的tf名字，这时，carto就会帮你生成map→odom_frame→publisher_frame这样的tf，对于这种我们没有odom的情况，一般published_frame也就指定为base_link或者base_footprint。

1 use_odometry

这个直接决定是否使用里程计信息（一般也就是我们是否有提供里程计信息），还是需要先理解一个前置知识，就是odom的tf与odom话题之间的关系，两者有关系，但并不等同，odom的tf一般也就是指odom与base_link的坐标系关系，它本身只有坐标系关系，即两个坐标系之间的平移矩阵、旋转矩阵；而odom话题就需要了解它的话题类型了，odom即里程计话题一般有专门的类型nav_msgs/Odometry，它内部不仅仅有tf包括的信息（它会指定child_frame的名字然后包括了旋转、平移的关系，具体去搜这个话题的定义），还会有速度信息、协方差矩阵也就是不确定性关系这些，因此如果odom的tf需要转换成odom的话题，需要手动定义协方差以及速度。了解了这些后，回到use_odometry的意义，它本身是决定是否使用里程计的信息，现在可以进一步说明是决定是否使用odom的话题，它一定是使用odom的话题，因此launch文件那个odom的remap就是和这个一起联动使用的。odom_frame和published_frame参数与use_odometry无关

2 tracking_frame

​tracking_frame一般设置为发布频率最高的传感器的frame_id，cartographer将会把其他数据都转移到该坐标系下进行计算。如果只使用雷达数据进行2D建图，那就只需要将其设置为雷达数据话题的frame_id。如果使用雷达数据+IMU进行2D或者3D建图，因为IMU的发布频率明显高于雷达，所以需要设置为imu数据话题的frame_id可以用rostopic echo <topicname> | grep frame_id查看frame_id

3 published_frame

​cartographer发布的tf树最后将指向published_frame，即published_frame不是cartographer提供的，这里如果没设置正确，tf树就不能连接成功，建图也就不能正常进行。这个一般设置为底盘的frame_id，也就是URDF文件中的底盘的link name，一般为base_link、base_footprint之类的名字

4 odom_frame

odom_frame与实际的里程计话题及消息没有什么关系，他只是cartographer提供的一个中间话题。将provide_odom_frame设置为false，cartographer将会提供tf树map指向published_frame；如果设置为true，cartographer将会提供tf树map->odom_frame指向published_frame。也就是是否需要
