import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

vicon_marker_file = "/vicon_kuafu_kuafu.tum"
vicon_foot_file = "/vicon_kuafu_fot_kuafu_fot.tum"
pinocchio_imu_foot_file = "/bitbot_foot_position.tum"

vicon_marker_data = np.loadtxt(vicon_marker_file, delimiter=' ')
vicon_foot_data = np.loadtxt(vicon_foot_file, delimiter=' ')
pinocchio_imu_foot_data = np.loadtxt(pinocchio_imu_foot_file,delimiter=' ')


T_imu_marker = [[1,0,0,0.047],[0,1,0,0.01825],[0,0,1,0.48385],[0,0,0,1]]

vicon_imu_foot = np.zeros((3,vicon_marker_data.shape[0]-1))
vicon_imu_foot_time = []

for i in range(vicon_marker_data.shape[0]-1):
    vicon_marker_r = R.from_quat(vicon_marker_data[i, 4:8])
    vicon_marker_t = vicon_marker_data[i, 1:4]
    vicon_G_marker = np.vstack((np.hstack((vicon_marker_r.as_matrix(), vicon_marker_t.reshape(3,1))), np.array([0,0,0,1])))
    vicon_foot_r = R.from_quat(vicon_foot_data[i, 4:8])
    vicon_foot_t = vicon_foot_data[i, 1:4]
    vicon_G_foot = np.vstack((np.hstack((vicon_foot_r.as_matrix(), vicon_foot_t.reshape(3,1))), np.array([0,0,0,1])))

    temp1 = np.dot(T_imu_marker, np.linalg.inv(vicon_G_marker))
    temp2 = np.dot(temp1, vicon_G_foot)
    vicon_imu_foot[0:3,i] = temp2[0:3,3]
    vicon_imu_foot_time.append(vicon_marker_data[i,0] - vicon_marker_data[0,0])

vicon_imu_foot_txyz = np.vstack((vicon_imu_foot_time,vicon_imu_foot[0,:], vicon_imu_foot[1,:], vicon_imu_foot[2,:]))

pinocchio_imu_foot_time = []
for i in range(pinocchio_imu_foot_data.shape[0]):
    pinocchio_imu_foot_time.append(pinocchio_imu_foot_data[i,0] - pinocchio_imu_foot_data[0,0])

pinocchio_imu_foot_txyz = np.vstack((pinocchio_imu_foot_time,pinocchio_imu_foot_data[:,1], pinocchio_imu_foot_data[:,2], pinocchio_imu_foot_data[:,3]))

# 绘制vicon_imu_foot_txyz的三维图像
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot(vicon_imu_foot_txyz[1,:], vicon_imu_foot_txyz[2,:], vicon_imu_foot_txyz[3,:], label='vicon_imu_foot')
ax.plot(pinocchio_imu_foot_txyz[1,:], pinocchio_imu_foot_txyz[2,:], pinocchio_imu_foot_txyz[3,:], label='pinocchio_imu_foot')
#将xyz轴写上xyz
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()
plt.show()
