cmake_minimum_required(VERSION 3.5)
project(ros2_2020)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Debug)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(rclcpp_components REQUIRED)

# main source file
add_library(control_node SHARED control_node.cpp)
ament_target_dependencies(
   control_node rclcpp sensor_msgs tf2_ros rclcpp_components geometry_msgs)
  
# auto-executable from node
rclcpp_components_register_node(control_node
  PLUGIN "ros2_2020::ControlNode"
  EXECUTABLE control)

install(TARGETS control_node
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)
  
install(PROGRAMS src/simulation.py
  DESTINATION lib/${PROJECT_NAME})
  
install(DIRECTORY launch urdf DESTINATION share/${PROJECT_NAME})
  
ament_package()
