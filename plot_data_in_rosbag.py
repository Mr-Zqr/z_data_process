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
bag_files.sort()
# Print out the list of files with numbers for selection
for i, f in enumerate(bag_files):
    print(f"\t{i+1}. {f}")
# Get user input for selection
selection = int(input("\n选择想要估计的rosbag文件: "))
# Assign the selected file path to bag_file
bag_file = os.path.join('/home/zqr/devel/dataset/evo_bag/', bag_files[selection-1])

b = bagreader(bag_file)

# 选择topic
print(b.topic_table)
# 设置topic
topics = ['/velocity_meas']

data = b.message_by_topic(topics[0])

data_csv = pd.read_csv(data)

import matplotlib.pyplot as plt
data_time = data_csv['twist.twist.linear.z'].to_numpy()

plt.figure(1)
plt.plot(data_time,label = 'time')
plt.show()