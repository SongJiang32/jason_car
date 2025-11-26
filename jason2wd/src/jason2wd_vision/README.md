在CMake中导入第三方函数库时,基本操作：
step1: find_package()
find_package(OpenCV REQUIRED)

step2: 添加节点编译规则，注意需要多加一条库文件列表
add_dependencies(cv_image_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
add_executable(cv_image_node src/cv_image_node.cpp)
target_link_libraries(cv_image_node
  ${catkin_LIBRARIES} ${OpenCV_LIBS}
)

step3: 添加include头文件路径
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)


