import socket
import json
import time 
from time import sleep
from time import time
import numpy as np
import os
import random
from scipy.spatial.transform import Rotation as R 
import sys 
from threading import Thread
sys.path.append("./cv")
sys.path.append("./nlp")
from detection import human_detection
from test_nlp import nlp_main

out_dict = None
cur_dict = None
motor_speed = 4


class motion_pkg:
    def __init__(self,x,y,z,ox,oy,oz,ow) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.ox = ox
        self.oy = oy 
        self.oz = oz

def euler2quat(x,y,z):
    euler = [x,y,z]
    r = R.from_euler('xyz',euler,degrees=True)
    qual = r.as_quat()
    return qual

def nlp_thread():
    global out_dict
    while(1):
        out_dict = nlp_main() 

def nlp_handler(out_dict):
    global motor_speed
    if(out_dict['force'] == 1):
        if(motor_speed<6):
            print("increase force")
            motor_speed+=1
        else:
            return
    elif(out_dict['force'] == -1):
        if(motor_speed>1):
            print("decrease force")
            motor_speed-=1
        else:
            return

def img2task(img_x,img_y):
    input_xy = np.array([img_x,img_y])
    A = np.array([[-2.08859508,  0.25894776],
       [ 0.51384374,  1.75344038]])
    B = np.array([ 1.35273004, -1.00227283])
    # A = np.array([[-2.10805,-0.026388],
    #               [0.06995109,1.73509612]])
    # B = np.array([1.45397184,-0.81637098])
    output_xy = np.dot(A,input_xy) + B
    print("Output xy",output_xy)
    return output_xy

def set_motor_speed(value = '1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 6666
    s.connect((host, port))
    s.sendall(value.encode())
    s.close()

def get_heartbeat():
    heart_array = []
    for i in range(1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 7777
        s.connect((host, port))
        msg = s.recv(1024)
        msg = msg.decode('utf-8')
        s.close()
        heart_array.append(int(msg.split(":")[2]))
        sleep(0.02)
    return np.mean(heart_array)

def get_force():
    force_array = []
    for i in range(5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 7777
        s.connect((host, port))
        msg = s.recv(1024)
        msg = msg.decode('utf-8')
        # print(msg.split(":")[0])
        s.close()
        force_array.append(int(msg.split(":")[0]))
        sleep(0.02)
    return np.mean(force_array)

def get_distance():
    dis_array = []
    for i in range(10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port = 7777
        s.connect((host, port))
        msg = s.recv(1024)
        msg = msg.decode('utf-8')
        s.close()
        # print(msg)
        dis_array.append(int(msg.split(":")[1])*17/1000)
        sleep(0.05)
    distance = np.mean(dis_array)
    return distance

def get_pose():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 9999
    s.connect((host, port))
    msg = s.recv(1024)
    msg = msg.decode('utf-8')
    recv_msg = json.loads(msg)
    return recv_msg

def pub_pose(px = -1,py = -1,pz = -1 ,ox = -1,oy = -1,oz = -1,ow = -1,time0 = 4):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888
    s.connect((host, port))
    cur_pose = get_pose()
    cur_position = cur_pose['pose']['position']
    cur_orientation = cur_pose['pose']['orientation']

    target_px = cur_position['x'] if px == -1 else px
    target_py = cur_position['y'] if py == -1 else py
    target_pz = cur_position['z'] if pz == -1 else pz
    target_ox = cur_orientation['x'] if ox == -1 else ox
    target_oy = cur_orientation['y'] if oy == -1 else oy
    target_oz = cur_orientation['z'] if oz == -1 else oz
    target_ow = cur_orientation['w'] if ow == -1 else ow

    msg = {"px": target_px, "py": target_py, "pz":target_pz, "ox": target_ox, "oy": target_oy, "oz": target_oz, "ow":target_ow, "time":time0}
    msg = json.dumps(msg)
    s.sendall(msg.encode('utf-8'))
    s.close()
    thred = 0.0005
    o_thred = 0.012

    start_t = time()
    while(1):
        cur_pose = get_pose()
        cur_pose_x = cur_pose['pose']['position']['x']
        cur_pose_z = cur_pose['pose']['position']['z']
        cur_pose_y = cur_pose['pose']['position']['y']
        cur_ori_x = cur_pose['pose']['orientation']['x']
        cur_ori_y = cur_pose['pose']['orientation']['y']
        cur_ori_z = cur_pose['pose']['orientation']['z']
        cur_ori_w = cur_pose['pose']['orientation']['w']

        if(np.abs(cur_pose_x-target_px)>thred or 
           np.abs(cur_pose_z-target_pz)>thred or 
           np.abs(cur_pose_y-target_py)>thred):
            if(time() - start_t >= time0 + 3):
                print("[WARNING] cannot reach")
                break
            else:
        #    np.abs(cur_ori_x-target_ox)>o_thred or
        #     np.abs(cur_ori_y-target_oy)>o_thred or
        #     np.abs(cur_ori_z-target_oz)>o_thred or
        #     np.abs(cur_ori_w-target_ow)>o_thred ):
                continue
        else:
            break
    return

def pub_dpose(dpx = 0,dpy = 0,dpz = 0,dox = 0,doy=0,doz=0,dow=0,time=3):
    cur_pose = get_pose()
    cur_position = cur_pose['pose']['position']
    cur_orientation = cur_pose['pose']['orientation']
    pub_pose(cur_position['x']+dpx,cur_position['y']+dpy,cur_position['z']+dpz,cur_orientation['x']+dox,cur_orientation['y']+doy,cur_orientation['z']+doz,cur_orientation['w']+dow,time)

def nlp_move_xy(nlp_result):
    global motor_speed
    head_offset_y = 5.5
    if(nlp_result == None):
        return
    d_p_x = 0
    d_p_y = 0
    if(nlp_result['position_x'] == '-1'):
        d_p_x = -0.06
    if(nlp_result['position_x'] == '1'):
        d_p_x = 0.06
    if(nlp_result['position_y'] == '1'):
        d_p_y = 0.06
    if(nlp_result['position_y'] == '-1'):
        d_p_y = -0.06
    if(nlp_result['force'] == '-1' or nlp_result['velocity_z'] == '-1'):
        if (motor_speed >1):
            motor_speed -=1
    if(nlp_result['force'] == '1' or nlp_result['velocity_z'] == '1'):
        if (motor_speed <=5):
            motor_speed +=1
    
    cur_pose = get_pose()

    mas_loc(d_p_x + cur_pose['pose']['position']['x'], d_p_y + cur_pose['pose']['position']['y'] + head_offset_y*0.01)

    # pub_dpose(dpx= d_p_x, dpy= d_p_y)



# def test_move_around_x():
#     state = True
#     while(1):
#         cur_pose = get_pose()
#         if(cur_pose['pose']['position']['x']<0.25 or cur_pose['pose']['position']['x']>0.44):
#             state = not state
#         if(state == True):
#             pub_dpose(dpx = -0.05,time = 1)
#         else:
#             pub_dpose(dpx = 0.05,time = 1)

# def test_move_around_z():
#     state = True
#     while(1):
#         cur_pose = get_pose()
#         if(cur_pose['pose']['position']['z']<0.11 or cur_pose['pose']['position']['z']>0.32):
#             state = not state
#         if(state == True):
#             pub_dpose(dpz = -0.05,time = 1)
#         else:
#             pub_dpose(dpz = 0.05,time = 1)

def init_pose():
    quat = euler2quat(0,45,0)
    pub_pose(px = 0.3,py= 0, pz = 0.35, ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0 = 6)
    return 

def detect_pose():
    quat = euler2quat(0,0,0)
    pub_pose(px = 0.4,py= 0, pz = 0.45, ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0 = 5)
    return 

def mas_loc(x,y,time0=4, is_same = False):
    set_motor_speed('0')
    global motor_speed
    global cur_dict
    global out_dict
    # in cm
    sensor_offset_x = -5
    sensor_offset_y = 6
    sensor_offset_z = 11.48
    head_offset_z = 26.2
    head_offset_y = -5.5
    head_offset_x = 0

    safety_thred = -0.15
    quat = euler2quat(0,90,90)
    ## Go to xy 
    pub_pose(pz = 0,ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0 = time0)
    pub_pose(px = x + sensor_offset_x*0.01,py=y+sensor_offset_y*0.01,pz = 0,ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0 = time0)
    sleep(0.2)
    ## process z 
    dis = get_distance()
    print("Up: sensor to obj",dis)
    print("Up: task space to obj",dis + sensor_offset_z)
    up_head_to_obj_cm = dis+ sensor_offset_z - head_offset_z
    print("Up: head to obj", up_head_to_obj_cm)
    go_down_pos_z = -(up_head_to_obj_cm*0.01 -0.001)
    print("Go down Pos Z",go_down_pos_z)
    ## judge the safety threshold in axis-z
    if(go_down_pos_z < safety_thred or go_down_pos_z >=0):
        print("target position out of safety range")
        down_pos_z = safety_thred
    else:
        down_pos_z = go_down_pos_z
    sleep(0.2)
    ## go to z 
    # pub_pose(px = x + head_offset_x * 0.01, py=y + head_offset_y*0.01, pz = down_pos_z, ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0=time0)
    pub_pose(px = x + head_offset_x * 0.01, py=y + head_offset_y*0.01, ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0=time0)
    sleep(0.1)
    pub_pose(pz=down_pos_z, ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0=time0)
    # sleep(0.2)

    already_get_up = 0
    while(get_force() >= 400):
        already_get_up += 3
        pub_dpose(dpz=0.03,time=0.6)
        sleep(0.2)
    print("motor_speed",motor_speed)
    set_motor_speed(str(motor_speed))



    start_t = time()
    while(time()-start_t<15):
        hb = get_heartbeat()
        f = get_force()
        if(hb >= 90):
            print("STOP!! ",hb)
            set_motor_speed('0')
            pub_pose(pz = 0,ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0 = time0)
            return 
        if(f>=400):
            already_get_up += 3
            pub_dpose(dpz=0.03,time=0.6)
            sleep(0.15)
        elif(f<25):
            if(already_get_up>0):
                already_get_up-=1
                pub_dpose(dpz=-0.01,time=0.8)
                sleep(0.15)

    set_motor_speed('0')
    pub_pose(pz = 0,ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3],time0 = time0)

    # sleep(0.1)
    # dis = get_distance()
    # print("Down: sensor to obj ",dis)
    # print("Down: task space to obj",dis+ sensor_offset_z)
    # print("Down: head to obj", dis + sensor_offset_z-head_offset_z)
    # sleep(0.2)
    return

def process_z():
    sleep(1)
    return 

def main_square_mas(time = 5):
    init_pose()
    while(True):
        mas_loc(0.3,0.15,time0=time)
        process_z()
        mas_loc(0.45,0.15,time0=time)
        process_z()
        mas_loc(0.45,-0.15,time0=time)
        process_z()
        mas_loc(0.3,-0.15,time0=time)
        process_z()

def main():
    init_pose()
    quat = euler2quat(0,45,0)
    pub_pose(ox=quat[0],oy=quat[1],oz=quat[2],ow=quat[3])
    # main_square_mas(time = 3)
    return 

def nlp_massage_main():
    mas_loc(0.35,0)
    while(1):
        nlp_result = nlp_main()
        print(nlp_result)
        nlp_move_xy(nlp_result)
    return

def cv_massage_main():
    init_pose()
    img_xy = human_detection()
    locs = [# img2task(img_xy[6][0],img_xy[6][1]),
            img2task((img_xy[5][0] + img_xy[0][0])/2,(img_xy[5][1]-0.05 + img_xy[0][1])/2),
            img2task((img_xy[5][0] + img_xy[1][0])/2,(img_xy[5][1]-0.05 + img_xy[1][1])/2),

            # img2task((img_xy[0][0] + img_xy[2][0])/2,(img_xy[0][1] + img_xy[2][1])/2),
            # img2task((img_xy[1][0] + img_xy[3][0])/2,(img_xy[1][1] + img_xy[3][1])/2),

            # img2task(0.666 * img_xy[0][0] + 0.333* img_xy[2][0],0.666* img_xy[0][1] + 0.333* img_xy[2][1]),
            # img2task(0.666 * img_xy[1][0] + 0.333* img_xy[3][0],0.666* img_xy[1][1] + 0.333* img_xy[3][1]),

            img2task(0.333 * img_xy[0][0] + 0.666* img_xy[2][0],0.333* img_xy[0][1] + 0.666* img_xy[2][1]),
            img2task(0.333 * img_xy[1][0] + 0.666* img_xy[3][0],0.333* img_xy[1][1] + 0.666* img_xy[3][1]),

            ]# img2task((img_xy[6][0] + 0.05 + img_xy[2][0])/2,(img_xy[6][1] + img_xy[2][1])/2),
            # img2task((img_xy[6][0] + img_xy[3][0])/2,(img_xy[6][1] + img_xy[3][1])/2)]

    # locs = [img2task((img_xy[0][0] + img_xy[2][0])/2,(img_xy[0][1] + img_xy[2][1])/2),
    #         img2task((img_xy[1][0] + img_xy[3][0])/2,(img_xy[1][1] + img_xy[3][1])/2)]

    for loc in locs:
        mas_loc(loc[0]+0.01,loc[1],time0=5)


if __name__ == "__main__":
    set_motor_speed('0')
    # mas_loc(0.4,0,time0=4)
    # while(1):
    #     print(get_heartbeat())
    # print(get_distance())
    # print(get_force())



    # head_offset_y = 5.5
    # cur_pose = get_pose()
    # mas_loc(0 + cur_pose['pose']['position']['x'], 0 + cur_pose['pose']['position']['y'] + head_offset_y*0.01)

    cv_massage_main()
    # init_pose()
    # nlp_massage_main()

    # nlp_result = {'position_x': '0', 'position_y': '0', 'force': '0', 'velocity_xy': '0', 'velocity_z': '0'}
    # nlp_move_xy(nlp_result)


    # img_xy = human_detection()
    # task_xy = img2task(img_xy[0][0],img_xy[0][1])
    # init_pose()
    # mas_loc(task_xy[0],task_xy[1],time0=4)

    # while(1):
    #     for i in range(7):
    #         init_pose()
    #         img_xy = human_detection()
    #         task_xy = img2task(img_xy[i][0],img_xy[i][1])
    #         mas_loc(task_xy[0],task_xy[1],time0=4)


    # print(get_distance())

    # init_pose()
    # set_motor_speed('3')
    # Thread(target=nlp_thread).start()
    # while(1):
    #     if(cur_dict == out_dict):
    #         continue
    #     else:
    #         print("Change")
    #         cur_dict=out_dict
    #         nlp_handler(cur_dict)
    #         init_pose()
    #         img_xy = human_detection()
    #         task_xy = img2task(img_xy[i][0],img_xy[i][1])
    #         mas_loc(task_xy[0],task_xy[1],time0=4)


    # print(get_distance())

    # init_pose()
    # set_motor_speed('3')
    # Thread(target=nlp_thread).start()
    # while(1):
    #     if(cur_dict == out_dict):
    #         continue
    #     else:
    #         print("Change")
    #         cur_dict=out_dict
    #         nlp_handler(cur_dict)


    # main_square_mas()
    # init_pose()
    # mas_loc(0.38,-0.09,time0=4)
    # mas_loc(0.45,0.1,time=4)
    # mas_loc(0.38,-0.13,time=4)
    # main_square_mas(4)

    # init_pose()
    # while(True):
    #     pub_dpose(dpz=0.01,time = 0.2)
    #     pub_dpose(dpz=-0.01,time=0.2)

    # while(True):
    #     mas_loc(0.2,0.15,time=5)
    #     mas_loc(0.4,0.15,time=5)
    #     mas_loc(0.4,-0.15,time=5)
    #     mas_loc(0.2,-0.15,time=5)



    # main_square_mas()
    # init_pose()
    # mas_loc(0.38,-0.09,time0=4)
    # mas_loc(0.45,0.1,time=4)
    # mas_loc(0.38,-0.13,time=4)
    # main_square_mas(4)

    # init_pose()
    # while(True):
    #     pub_dpose(dpz=0.01,time = 0.2)
    #     pub_dpose(dpz=-0.01,time=0.2)

    # while(True):
    #     mas_loc(0.2,0.15,time=5)
    #     mas_loc(0.4,0.15,time=5)
    #     mas_loc(0.4,-0.15,time=5)
    #     mas_loc(0.2,-0.15,time=5)
