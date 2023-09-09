# 读取某个目录下的所有.bag 文件，另存为csv文件
import bagpy
from bagpy import bagreader
import os
file_path = '******'
# Get a list of all .bag files in the directory
bag_files = [f for f in os.listdir(file_path) if f.endswith('.bag')]
print("找到以下rosbag文件: ")
# Print out the list of files with numbers for selection, 按照文件名升序排列
bag_files.sort()
for i, f in enumerate(bag_files):
    print(f"\t{i+1}. {f}")
# Get user input for selection
selection = int(input("\n选择想要估计的rosbag文件: "))
# Assign the selected file path to bag_file
bag_file = os.path.join(file_path, bag_files[selection-1])
b = bagreader(bag_file)
print(b.topic_table)
topics = b.topics
for topic in topics:
    df = b.message_by_topic(topic)

print("Down....")

# 读取.csv文件
import pandas as pd
file_data = pd.read_csv('file.csv')
file_x = file_data['transform.translation.x'].to_numpy()
