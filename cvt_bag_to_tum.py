import rosbag
import numpy as np

# 设置rosbag文件路径和输出文件路径
bag_path = "/path/to/bag/file.bag"
output_path = "/path/to/output/file.txt"

# 设置需要转换的topic名称
topic_name = "/odom"

# 读取rosbag文件
bag = rosbag.Bag(bag_path)

# 初始化变量
timestamps = []
positions = []
orientations = []

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
timestamps -= timestamps[0]

# 将位置和姿态信息保存到tum格式的txt文件中
with open(output_path, "w") as f:
    for i in range(len(timestamps)):
        f.write("{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(
            timestamps[i] / 1e9,
            positions[i, 0], positions[i, 1], positions[i, 2],
            orientations[i, 0], orientations[i, 1], orientations[i, 2], orientations[i, 3]))

# 关闭rosbag文件
bag.close()
