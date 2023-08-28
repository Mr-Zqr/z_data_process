import rosbag
import numpy as np
import os

# 设置rosbag文件路径和输出文件路径
bag_path = "/home/zqr/devel/dataset/evo_bag/"

bag_files = [f for f in os.listdir(bag_path) if f.endswith('.bag')]
print("找到以下rosbag文件：")
bag_files.sort()
# Print out the list of files with numbers for selection
for i, f in enumerate(bag_files):
    print(f"\t{i+1}. {f}")
# Get user input for selection
selection = int(input("\n选择想要估计的rosbag文件: "))
# Assign the selected file path to bag_file
bag_file = os.path.join('/home/zqr/devel/dataset/evo_bag/', bag_files[selection-1])

# 设置需要转换的topic名称
topic_name = "/Odometry"
output_path = bag_file[:-4] + ".txt"

print(output_path)
# 读取rosbag文件
bag = rosbag.Bag(bag_file)

# 初始化变量
timestamps = []
positions = []
orientations = []

# 如果没有topic_name报错
if topic_name not in bag.get_type_and_topic_info()[1].keys():
    raise ValueError("Topic {} not found in bag file {}".format(topic_name, bag_file))

# 遍历rosbag文件中的消息
for topic, msg, t in bag.read_messages(topics=[topic_name]):
    # 提取odometry消息中的位置和姿态信息
    position = msg.pose.pose.position
    orientation = msg.pose.pose.orientation

    # 将时间戳和位置、姿态信息添加到对应的列表中
    timestamps.append(t.to_nsec())
    positions.append([position.x, position.y, position.z])
    orientations.append([orientation.x, orientation.y, orientation.z, orientation.w])

# 将位置和姿态信息转换为numpy数组
positions = np.array(positions)
orientations = np.array(orientations)

# 将时间戳转换为相对时间
timestamps = np.array(timestamps)
# timestamps -= timestamps[0]

# 将位置和姿态信息保存到tum格式的txt文件中
with open(output_path, "w") as f:
    for i in range(len(timestamps)):
        f.write("{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(
            timestamps[i] / 1e9,
            positions[i, 0], positions[i, 1], positions[i, 2],
            orientations[i, 0], orientations[i, 1], orientations[i, 2], orientations[i, 3]))

# 关闭rosbag文件
bag.close()
