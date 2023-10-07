from bagpy import bagreader
import os

def get_user_selection():
  selection = input("请输入您的选择：")
  selection = selection.replace(" ", "")  # 去除空格
  selected_items = []
  if "," in selection:
    item_parts = selection.split(",")
    for part in item_parts:
      if "-" in part:
        range_parts = part.split("-")
        start = int(range_parts[0])
        end = int(range_parts[1])
        selected_items.extend(range(start, end + 1))
      else:
        selected_items.append(int(part))
  elif "-" in selection:
    range_parts = selection.split("-")
    start = int(range_parts[0])
    end = int(range_parts[1])
    selected_items.extend(range(start, end + 1))
  else:
    selected_items.append(int(selection))
  return selected_items

file_path = './'
# Get a list of all .bag files in the directory
bag_files = [f for f in os.listdir(file_path) if f.endswith('.bag')]
print("找到以下rosbag文件: ")
# Print out the list of files with numbers for selection, 按照文件名升序排列
bag_files.sort()
for i, f in enumerate(bag_files):
    print(f"\t{i+1}. {f}")
# Get user input for selection
selection = int(input("\n选择想要转换的rosbag文件: "))
# Assign the selected file path to bag_file
bag_file = os.path.join(file_path, bag_files[selection-1])
b = bagreader(bag_file)
print(b.topic_table)
print("请选择需要转换的topic(例:1-4,6,7):")
for i, f in enumerate(b.topic_table.Topics):
    print(f"\t{i+1}. {f}")

user_selection = get_user_selection()
topics = []
for i in user_selection:
    topics.append(b.topic_table.Topics[i-1])

for topic in topics:
    print(f"正在转换: {topic}")
    df = b.message_by_topic(topic)
    print(f"转换完成")

print("Done....")
