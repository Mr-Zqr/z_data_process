# data_process_cmp_xyz.py

# This script is used to process rosbag files and estimate the Absolute Pose Error (APE) between two topics. 
# The script uses the `evo` library to estimate the APE and extract the transformation matrix between the two topics.

# Place your rosbag files in the directory `/home/zqr/devel/dataset/evo_bag/`.
# Run the script `data_process_cmp_xyz.py` in a Python environment with the required dependencies installed.
# The script will display a list of all .bag files in the directory `/home/zqr/devel/dataset/evo_bag/`.
# Select the rosbag file you want to estimate by entering the corresponding number.
# The script will estimate the APE between the two topics `/Odometry` and `/vicon/kuafu/kuafu` and extract the transformation matrix.
# Then use the t matrix to aline two trajectories in specified topics and plot x, y, and z coordinates of the two trajectories.

# Dependencies:
# - rosbag
# - rospy
# - bagpy
# - pandas
# - numpy
# - scipy
# - evo

# You can install the required dependencies using pip:
# pip install rosbag rospy bagpy pandas numpy scipy evo

# Author: Github Copilot, Zhao Qingrui

import rosbag
import rospy
import bagpy
import pandas as pd
from bagpy import bagreader
import numpy as np
from scipy.spatial.transform import Rotation as R
import subprocess

# 读取文件路径/home/zqr/devel/dataset/evo_bag/中的.bag文件，并在命令行中列出来，让我通过1 2 3... 进行选择，选择后，将选择的文件路径赋值给bag_file
import os
# Get a list of all .bag files in the directory
bag_files = [f for f in os.listdir('/home/zqr/devel/dataset/evo_bag/') if f.endswith('.bag')]
print("找到以下rosbag文件：")
# Print out the list of files with numbers for selection
for i, f in enumerate(bag_files):
    print(f"\t{i+1}. {f}")
# Get user input for selection
selection = int(input("\n选择想要估计的rosbag文件: "))
# Assign the selected file path to bag_file
bag_file = os.path.join('/home/zqr/devel/dataset/evo_bag/', bag_files[selection-1])

# 设置topic
topics = ['/Odometry', '/vicon/kuafu/kuafu']

cmd = f"evo_ape bag {bag_file} {' '.join(topics)} -va"
# print(cmd)
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# 提取变换矩阵
output = result.stdout
start = output.find('Translation of alignment:\n') + len('Translation of alignment:\n')
end = output.find('\n', start)
matrix_str = output[start:end]
# 去掉`matrix_str中的[],并转换为numpy数组`
matrix_str = matrix_str.replace('[', '').replace(']', '')
matrix = np.fromstring(matrix_str, sep=' ')
T_ex = np.eye(4)
T_ex[0:3, 3] = matrix[0:3]

b = bagreader(bag_file)

print(b.topic_table)
# message_by_topic 与topics联动
odom = b.message_by_topic(topics[0])
vicon = b.message_by_topic(topics[1])

odom_msg = pd.read_csv(odom)
vicon_msg = pd.read_csv(vicon)
import matplotlib.pyplot as plt
# 将上边两个pd数组的时间戳和xyz左边转为numpy格式，并分别存在新数组中
odom_time = odom_msg['Time'].to_numpy()
odom_x = odom_msg['pose.pose.position.x'].to_numpy()
odom_y = odom_msg['pose.pose.position.y'].to_numpy()
odom_z = odom_msg['pose.pose.position.z'].to_numpy()

vicon_time = vicon_msg['Time'].to_numpy()
vicon_x = vicon_msg['transform.translation.x'].to_numpy()
vicon_y = vicon_msg['transform.translation.y'].to_numpy()
vicon_z = vicon_msg['transform.translation.z'].to_numpy()
vicon_rx = vicon_msg['transform.rotation.x'].to_numpy()
vicon_ry = vicon_msg['transform.rotation.y'].to_numpy()
vicon_rz = vicon_msg['transform.rotation.z'].to_numpy()
vicon_rw = vicon_msg['transform.rotation.w'].to_numpy()

vicon_xyzxyzw = np.vstack((vicon_x, vicon_y, vicon_z, vicon_rx, vicon_ry, vicon_rz, vicon_rw))

# 将vicon的xyzw转换为旋转矩阵
vicon_r_0 = R.from_quat(vicon_xyzxyzw[3:7,0].T)
vicon_t_0 = vicon_xyzxyzw[0:3,0]
# 将vicon_r_0, vicon_t_0拼为其次变换矩阵
# 定义vicon_xyz
vicon_xyz = np.zeros((3, vicon_xyzxyzw.shape[1]))
vicon_T_0 = np.vstack((np.hstack((vicon_r_0.as_matrix(), vicon_t_0.reshape(3,1))), np.array([0,0,0,1])))
for i in range(vicon_xyzxyzw.shape[1]):
    vicon_r = R.from_quat(vicon_xyzxyzw[3:7,i].T)
    vicon_t = vicon_xyzxyzw[0:3,i]
    vicon_T = np.vstack((np.hstack((vicon_r.as_matrix(), vicon_t.reshape(3,1))), np.array([0,0,0,1])))
    temp1 = np.dot(np.linalg.inv(T_ex),np.linalg.inv(vicon_T_0))
    temp2 = np.dot(temp1, vicon_T)
    vicon_T_0_t = np.dot(temp2,T_ex)
    vicon_xyz[0:3,i] = vicon_T_0_t[0:3,3]

odom_txyz = np.vstack((odom_time,odom_x, odom_y, odom_z))
# vicon_xyz = np.vstack((vicon_x, vicon_y, vicon_z))
vicon_txyz = np.vstack((vicon_time,vicon_xyz[0,:], vicon_xyz[1,:], vicon_xyz[2,:]))

# 将vicon和odom的x y z结果分别绘制在三张图上，横坐标为时间戳
plt.figure()
plt.plot(odom_txyz[0,:], odom_txyz[1,:], label='odom_x')
plt.plot(vicon_txyz[0,:], vicon_txyz[1,:], label='vicon_x')
plt.legend()
plt.figure()
plt.plot(odom_txyz[0,:], odom_txyz[2,:], label='odom_y')
plt.plot(vicon_txyz[0,:], vicon_txyz[2,:], label='vicon_y')
plt.legend()
plt.figure()
plt.plot(odom_txyz[0,:], odom_txyz[3,:], label='odom_z')
plt.plot(vicon_txyz[0,:], vicon_txyz[3,:], label='vicon_z')
plt.legend()
plt.show()
