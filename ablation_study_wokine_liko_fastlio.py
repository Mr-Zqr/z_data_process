# 读取指定文的tum文件，并保存到numpy数组中
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

vicon_file = "/home/zqr/devel/dataset/cmp_liko_likowokin_likowolidar/vicon_kuafu_kuafu.tum"
liko_file = "/home/zqr/devel/dataset/cmp_liko_likowokin_likowolidar/bitbot_liko.tum"
fast_lio_file = "/home/zqr/devel/dataset/cmp_liko_likowokin_likowolidar/Odometry.tum"
imu_kin_file = "/home/zqr/devel/dataset/cmp_liko_likowokin_likowolidar/bitbot_liko_wolidar.tum"

vicon_data = np.loadtxt(vicon_file, delimiter=' ')
liko_data = np.loadtxt(liko_file, delimiter=' ')
fast_lio_data = np.loadtxt(fast_lio_file, delimiter=' ')
imu_kin_data = np.loadtxt(imu_kin_file, delimiter=' ')

vicon_r_0 = R.from_quat(vicon_data[0, 4:8])
vicon_t_0 = vicon_data[0, 1:4]

T_ex = [[1,0,0,0.047],[0,1,0,0.01825],[0,0,1,0.48385],[0,0,0,1]]
vicon_xyz = np.zeros((3,vicon_data.shape[0]))
vicon_time_0 = []

vicon_T_0 = np.vstack((np.hstack((vicon_r_0.as_matrix(), vicon_t_0.reshape(3,1))), np.array([0,0,0,1])))

for i in range(vicon_data.shape[0]):
    vicon_r = R.from_quat(vicon_data[i, 4:8])
    vicon_t = vicon_data[i, 1:4]
    vicon_T = np.vstack((np.hstack((vicon_r.as_matrix(), vicon_t.reshape(3,1))), np.array([0,0,0,1])))
    temp1 = np.dot(np.linalg.inv(T_ex),np.linalg.inv(vicon_T_0))
    temp2 = np.dot(temp1, vicon_T)
    vicon_T_0_t = np.dot(temp2,T_ex)
    vicon_xyz[0:3,i] = vicon_T_0_t[0:3,3]
    vicon_time_0.append(vicon_data[i,0] - vicon_data[0,0])

vicon_txyz = np.vstack((vicon_time_0,vicon_xyz[0,:], vicon_xyz[1,:], vicon_xyz[2,:]))
# 将liko_file和imu_kin_file的时间也改成从零开始的
liko_time_0 = []
imu_kin_time_0 = []
fastlio_time_0=[]
for i in range(liko_data.shape[0]):
    liko_time_0.append(liko_data[i,0] - liko_data[0,0])

delta_time_temp = 0
for i in range(imu_kin_data.shape[0]):
    delta_time = imu_kin_data[i,0] - imu_kin_data[0,0]
    if delta_time < -10:
        delta_time = delta_time_temp
    delta_time_temp = delta_time
    imu_kin_time_0.append(delta_time)

for i in range(fast_lio_data.shape[0]):
    fastlio_time_0.append(fast_lio_data[i,0] - fast_lio_data[0,0])

fastlio_txyz = np.vstack((fastlio_time_0,fast_lio_data[:,1], fast_lio_data[:,2], fast_lio_data[:,3]))
liko_txyz = np.vstack((liko_time_0,liko_data[:,1], liko_data[:,2], liko_data[:,3]))
imu_kin_txyz = np.vstack((imu_kin_time_0,imu_kin_data[:,1], imu_kin_data[:,2], imu_kin_data[:,3]))

# plt.figure()
# plt.plot(vicon_txyz[0,:], vicon_txyz[1,:], label='vicon_x')
# plt.plot(liko_txyz[0,:], liko_txyz[1,:], label='liko_x')
# plt.plot(imu_kin_txyz[0,:], imu_kin_txyz[1,:], label='imu_kin_x')
# plt.plot(fastlio_txyz[0,:], fastlio_txyz[1,:], label='fastlio_x')
# #限制x轴范围
# plt.ylim(-2, 2)
# plt.legend()

# plt.figure()
# plt.plot(vicon_txyz[0,:], vicon_txyz[2,:], label='vicon_y')
# plt.plot(liko_txyz[0,:], liko_txyz[2,:], label='liko_y')
# plt.plot(imu_kin_txyz[0,:], imu_kin_txyz[2,:], label='imu_kin_y')
# plt.plot(fastlio_txyz[0,:], fastlio_txyz[2,:], label='fastlio_y')
# plt.ylim(-2, 2)
# plt.legend()
plt.rc('font',family='Times New Roman') 
grid=plt.GridSpec(3,1,wspace=0.5, hspace=0.5)

plt.subplot(grid[0:2,:])
plt.plot(imu_kin_txyz[2,:], imu_kin_txyz[1,:], label='imu_kin_xy',linewidth=3,color='tab:purple')
plt.plot(vicon_txyz[2,:], vicon_txyz[1,:],     label='vicon_xy',linewidth=3, color='tab:orange')
plt.plot(fastlio_txyz[2,:], fastlio_txyz[1,:], label='fastlio_xy',linewidth=3, color='tab:blue')
plt.plot(liko_txyz[2,:], liko_txyz[1,:]+0.05, label='liko_xy',linewidth=3, color='tab:green')
plt.ylim(-2, 2)
plt.xlim(-2,2)
# ax = plt.gca()
# ax.set_aspect(1)
# x轴标签
plt.xlabel('(a) Y-Axis (m)', fontsize=14)
# y轴标签
plt.ylabel('X-Axis (m)', fontsize=14)
plt.xticks(np.arange(-2, 3, 1), size = 14)
plt.yticks(np.arange(-2, 3, 1), size = 14)
plt.tight_layout()
# plt.show()
# plt.savefig('/home/zqr/devel/dataset/cmp_liko_likowokin_likowolidar/z.svg', dpi=600, format='svg')

plt.subplot(grid[2,:])
plt.plot(imu_kin_txyz[0,:], imu_kin_txyz[3,:], label='LIKO (I & K)',linewidth=3, color='tab:purple')
plt.plot(vicon_txyz[0,:], vicon_txyz[3,:],label='Ground Truth',linewidth=3,color='tab:orange')
plt.plot(fastlio_txyz[0,:], fastlio_txyz[3,:], label='LIKO (L & I)',linewidth=3, color='tab:blue')
plt.plot(liko_txyz[0,:], liko_txyz[3,:],label='LIKO (L & I & K)',linewidth=3, color='tab:green')
plt.ylim(-0.1, 0.6)
plt.xlim(0, 140)
# x轴标签
plt.xlabel('(b) Time (s)', fontsize=14)
# y轴标签
plt.ylabel('Z-Axis (m)', fontsize=14)
# ax = plt.gca()
# ax.set_aspect(1)
plt.xticks(np.arange(0, 150, 20), size = 14)
plt.yticks(np.arange(-0.1, 0.6, 0.2), size = 14)
plt.legend(loc='upper right', prop = {'size':10})
# plt.legend()
plt.tight_layout()
plt.show()
# plt.savefig('/home/zqr/devel/dataset/cmp_liko_likowokin_likowolidar/xy3_4.svg', dpi=600, format='svg')