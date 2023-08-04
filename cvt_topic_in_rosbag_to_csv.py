import bagpy
from bagpy import bagreader
import os

file_path = '/home/zqr/devel/dataset/evo_bag/'
# Get a list of all .bag files in the directory
bag_files = [f for f in os.listdir(file_path) if f.endswith('.bag')]
print("找到以下rosbag文件：")
# Print out the list of files with numbers for selection, 按照文件名升序排列
bag_files.sort()
for i, f in enumerate(bag_files):
    print(f"\t{i+1}. {f}")

# Get user input for selection
selection = int(input("\n选择想要估计的rosbag文件: "))
# Assign the selected file path to bag_file
bag_file = os.path.join(file_path, bag_files[selection-1])

# 将bag文件转换为csv文件
b = bagreader(bag_file)
print(b.topic_table)

topics = b.topics

# Write each topic to a separate csv file
for topic in topics:
    df = b.message_by_topic(topic)

print("Down....")
