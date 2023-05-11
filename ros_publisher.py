#!/usr/bin/python
import sys
import socket
import rospy
import json
from open_manipulator_msgs.srv import SetKinematicsPoseRequest, SetKinematicsPose

def init_server():
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    port = 8888
    host = "127.0.0.1"
    serversocket.bind((host, port))
    serversocket.listen(5)
    print("[ROS PUB SERVER] Start")
    while True:
        clientsocket, addr = serversocket.accept()
        print("connect %s" % str(addr))
        msg = clientsocket.recv(1024)
        msg = msg.decode('utf-8')
        recv_msg = json.loads(msg)
        ros_pub(recv_msg)
        # print(recv_msg)
        clientsocket.close()

def ros_pub(pkg):
    set_position_client(pkg['px'],pkg['py'],pkg['pz'],pkg['ox'],pkg['oy'],pkg['oz'],pkg['ow'],pkg['time'])




def set_position_client(px,py, pz,ox,oy,oz,ow,time):
    service_name = '/goal_task_space_path'
    rospy.wait_for_service(service_name)
    try:
        set_position = rospy.ServiceProxy(service_name, SetKinematicsPose)

        arg = SetKinematicsPoseRequest()
        arg.end_effector_name = 'gripper'
        arg.kinematics_pose.pose.position.x = px
        arg.kinematics_pose.pose.position.y = py
        arg.kinematics_pose.pose.position.z = pz
        arg.kinematics_pose.pose.orientation.x = ox 
        arg.kinematics_pose.pose.orientation.y = oy
        arg.kinematics_pose.pose.orientation.z = oz
        arg.kinematics_pose.pose.orientation.w = ow
        arg.path_time = time
        resp1 = set_position(arg)
        print 'Service done!'
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        return False

if __name__ == '__main__':
    init_server()
