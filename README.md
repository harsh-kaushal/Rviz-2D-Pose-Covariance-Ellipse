# Rviz-2D-Pose-Covariance-Ellipse

This script creates a node which subscribes from the Odometry data (in script from EKF_filtered/Odometry) 
and calculates the length of major and minor axis of 2D pose Covariance.
![](Images/radius.png)

Then for RVIZ, a ellipse shaped marker is created with frame of footprint( bot base) therefore the pose is (0, 0, 0) wrt to robot.

This marker can can be visualized in the Rviz Add by topic section under Visualization_msg/Marker.
![](Images/Marker_Add.png)

Once added the Covariance will appere below the robot
![](Images/rviz_marker.png)

The Rqt_graph will not show any connection from visualization_msg to Rviz untill yoyu unhide Debug
![](Images/marker_rqt_graph.png)


Further, Script is full of comments DO check it out 
