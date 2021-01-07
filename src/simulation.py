#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np
from geometry_msgs.msg import Twist, TransformStamped
from tf2_ros import TransformBroadcaster

a = 2
b = 3
dt = 0.05

class Robot:
    def __init__(self, node, name):
        
        self.name = name
        self.tf = TransformStamped()
        
        self.tf.child_frame_id = name + '/base_link'
        self.tf.header.frame_id = 'map'
        
        if name == 'r2d2':
            self.x = 0.
            self.y = 0.
            self.theta = 0.
            self.t = 0.
        else:
            self.cmd = None
            if name == 'bb8':
                self.x = 2.
                self.y = 0.
                self.theta = 0.
            else:
                self.x = -2.
                self.y = 0.
                self.theta = 0.
            # also create subscriber
            self.cmd_sub = node.create_subscription(
            Twist,
            name + '/cmd_vel',
            self.cmd_callback,
            10)
            
    def cmd_callback(self, msg):
        self.cmd = msg
            
    def update_tf(self, node):
        
        # update position
        if self.name == 'r2d2':
            self.t += dt                
            c,s = np.cos(.5*self.t),np.sin(.5*self.t)
            self.x = (a + b*c)*c
            self.y = (a + b*c)*s
            vx = -a*s-2*b*c*s
            vy = a*c + b - 2*b*s*s
            self.theta = np.arctan2(vy, vx)
            
        elif self.cmd is not None:
            v,w = self.cmd.linear.x, self.cmd.angular.z
            self.x += v * np.cos(self.theta)*dt
            self.y += v * np.sin(self.theta)*dt
            self.theta += w*dt
        
        self.tf.header.stamp = node.get_clock().now().to_msg()
        self.tf.transform.translation.x = self.x
        self.tf.transform.translation.y = self.y
        self.tf.transform.rotation.z = np.sin(self.theta/2)
        self.tf.transform.rotation.w = np.cos(self.theta/2)
        
        node.br.sendTransform(self.tf)

class SimulationNode(Node):    

    def __init__(self):        
        super().__init__('simulation')
        
        self.robots = [Robot(self, name) for name in ('bb8','r2d2','d0')]
        self.br = TransformBroadcaster(self)
        self.create_timer(dt, self.publish)
        
    def publish(self):
        
        for robot in self.robots:
            robot.update_tf(self)
            
    
def main(args=None):
    
    rclpy.init(args=args)

    simulation = SimulationNode()

    rclpy.spin(simulation)
    simulation.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
