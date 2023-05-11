#!/usr/bin/python
from open_manipulator_msgs.msg import KinematicsPose
import rospy 
import socket
import json

def init_server():
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 9999
    serversocket.bind((host, port))
    serversocket.listen(5)
    print("[ROS TOPIC SERVER] Start")
    while True:
        clientsocket, addr = serversocket.accept()
        print("[ROS TOPIC SERVER] connect %s" % str(addr))
        msg = ros_listen()
        sendmsg = json.dumps(msg)
        clientsocket.sendall(sendmsg.encode('utf-8'))
        clientsocket.close()

def ros_listen():
    rospy.init_node("listener",anonymous=True)
    try:
        POSE_MSG = rospy.wait_for_message("/gripper/kinematics_pose", KinematicsPose, timeout=5)
    except:
        POSE_MSG = None

    if(POSE_MSG == None):
        return None 
    else:
        return {"pose":{"position":{"x":POSE_MSG.pose.position.x,"y":POSE_MSG.pose.position.y,"z":POSE_MSG.pose.position.z}, "orientation":{"x":POSE_MSG.pose.orientation.x,"y":POSE_MSG.pose.orientation.y,"z":POSE_MSG.pose.orientation.z,"w":POSE_MSG.pose.orientation.w} }}


if __name__ == "__main__":
    init_server()