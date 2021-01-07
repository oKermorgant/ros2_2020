// this node has its class fully defined in the cpp file
// for larger nodes, the class can be classically split in header / source


// include any thing required - do not forget to use the .hpp extension for ROS 2 files
#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/static_transform_broadcaster.h>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer_client.h>

using namespace std::chrono_literals;

namespace ros2_2020
{

class ControlNode : public rclcpp::Node
{
public:
  ControlNode(rclcpp::NodeOptions options)
    : Node("control", options), tf_buffer(get_clock()), tf_listener(tf_buffer)
  {
    // init parameters: name of this robot + name of the target
      
    // init whatever is needed for your node: publisher / timer / etc

  }
  
private:

  // declare member variables for publisher and timer


  // TF 2 stuff
  tf2_ros::Buffer tf_buffer;
  tf2_ros::TransformListener tf_listener;

  
};
}

#include "rclcpp_components/register_node_macro.hpp"
RCLCPP_COMPONENTS_REGISTER_NODE(ros2_2020::ControlNode)
