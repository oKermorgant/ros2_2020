from simple_launch import SimpleLauncher

def generate_launch_description():
    sl = SimpleLauncher()
    
    # load descriptions
    for robot in ('r2d2', 'bb8','d0'):
        with sl.group(ns = robot):
            sl.robot_state_publisher('ros2_2020', robot + '.xacro')
    
    # run Python simulation
    sl.node('ros2_2020','simulation.py', output='screen')
    
    # run RViz2
    rviz_config_file = sl.find('ros2_2020', 'config.rviz')
    sl.node('rviz2','rviz2', output='log', arguments=['-d', rviz_config_file])
    
    return sl.launch_description()
