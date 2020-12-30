#!/usr/bin/env python
from __future__ import print_function   # just a fancy print, No big deal
import os                               # For cleaning the terminal


import rospy
import numpy as np

from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker

from tf.transformations import euler_from_quaternion, quaternion_from_euler


def loop(sub_data):

    os.system('clear')                                  #cleans the mess we made on last iteration



    #################------------Conversion Stuff-----------#######################
    
    #Position and yaw Data
    _postion_ = sub_data.pose.pose.position
    #_orientation_ = sub_data.pose.pose.orientation     #Not used as everything is in footprint frame


    #Covariance Matrix
    _covaraince_ = sub_data.pose.covariance             #Filled completely in row manner

    # 6-variable Covariance Matrix 
    #|  xx  |   xy  |   xz  |   xR  |   xP  |   xY  |   R--roll
    #|  yx  |   yy  |   yz  |   YR  |   yP  |   yY  |   P--pitch
    #|  zx  |   zy  |   zz  |   ZR  |   zP  |   zY  |   Y--yaw
    #|  Rx  |   Ry  |   Rz  |   RR  |   RP  |   RY  |
    #|  Px  |   Py  |   Pz  |   PR  |   PP  |   PY  |
    #|  Yx  |   Yy  |   Yz  |   YR  |   YP  |   YY  |

    xy_cov_matrix =[[_covaraince_[0],_covaraince_[1]],
                    [_covaraince_[6],_covaraince_[7]]]


    #Sometimes My Genius... It's Almost Frightening 
    # https://cookierobotics.com/007/
    # well i said somtimes.

    a = xy_cov_matrix[0][0]
    b = xy_cov_matrix[0][1]
    b_= xy_cov_matrix[1][0]
    c = xy_cov_matrix[1][1]
    print("#############")
    print('x v/s y Covariance Matrix\n')

    print("|%f|%f|" %(a,b))
    print("|%f|%f|" %(b_,a))

    print("-------------")

    lambda_1 = ( (a+c)/2 ) + ( ((a-c)/2)**2 + b**2 )**0.5   #Length of Major Axis
    lambda_2 = ( (a+c)/2 ) - ( ((a-c)/2)**2 + b**2 )**0.5   #Length of Minor Axis

    print('lambda_1 = ',lambda_1)
    print('lambda_2 = ',lambda_2)

    if (b==0 and a<=c):
        theta = 0.0
    elif (b==0 and a<c):
        theta = 3.14/2
    else:
        theta = np.arctan2(lambda_1-a,b)

    #################------------Rviz Stuff-----------#######################

    marker_pub = rospy.Publisher('visualization_marker', Marker, queue_size=1)
    
    marker_ = Marker()                                  # DS object 
    header = Header()

    #Marker Information
    marker_.header.stamp =rospy.get_rostime()
    marker_.header.frame_id = 'footprint'               # selecting bot frame for less complexity footprint == base frame

    marker_.ns = "ellipse_data_node"
    marker_.id = 777
    marker_.action = marker_.ADD
       
    #Features of the marker
    marker_.type = marker_.SPHERE                       #Sphere shaped
    marker_.color.r = 0.0                               #
    marker_.color.g = 1.0                               #Colour code
    marker_.color.b = 0.0                               #
    marker_.color.a = 0.5                               #Transparancy 

    # To Set the pose of the marker as same as bot
    marker_.pose.position.x = 0                         #Positions are in Footprint frame
    marker_.pose.position.y = 0                         #so the position will always same as of bot
    marker_.pose.position.z = 0.01

    # Making ellipsoid outof covariance matrix
    marker_.scale.x = abs(lambda_1)
    marker_.scale.y = abs(lambda_2)
    marker_.scale.z = 0.001                             # Its 2D Ellipsoid Bitch

    # Orientation of 2d Ellipsoid about all the 3 axis.

    q= quaternion_from_euler(0.0,0.0,theta)             #Everything is in Footprint frame

    marker_.pose.orientation.x = q[0]                   #Heading
    marker_.pose.orientation.y = q[1]                   #Side
    marker_.pose.orientation.z = q[2]                   #Vertical
    marker_.pose.orientation.w = q[3]                   #Bitch its a Quaternion !!!!
    
    #print("-------------")
    #print("Quaternion = ",q)                           #Marker Pose orientation

    marker_.lifetime = rospy.Duration()

    print("-------------")
    print("Number Of Connections = ",marker_pub.get_num_connections())
    if (marker_pub.get_num_connections()<1):
        print("Please create a subscriber to the marker")
    else:
        print("Publishing on /visualization_marker ")
    print("#############")

    marker_pub.publish(marker_)
    
    rate = rospy.Rate(10)
    rate.sleep()


def listener():
    # Inititate node named "ellipse_data_node"
    rospy.init_node('ellipse_data_node', anonymous=False)

    #set test_subscriber to subscribe from topic odometry/filtered the data of type Odometry
    rospy.Subscriber("odometry/filtered", Odometry, loop)
    
    # spin() : let it burn..., till the end of time.
    rospy.spin()

if __name__ == '__main__':
    listener()