# 使用evo求变换矩阵并读取结果

import subprocess
import numpy as np

bag_file = 'bagfile.bag'
topics = ['topic1', 'topic2']
cmd = f"evo_ape bag {bag_file} {' '.join(topics)} -va"
# print(cmd)
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
output = result.stdout
start = output.find('Translation of alignment:\n') + len('Translation of alignment:\n')
end = output.find('\n', start)
matrix_str = output[start:end]
# 去掉`matrix_str中的[],并转换为numpy数组`
matrix_str = matrix_str.replace('[', '').replace(']', '')
matrix = np.fromstring(matrix_str, sep=' ')
T_ex = np.eye(4)
T_ex[0:3, 3] = matrix[0:3]

