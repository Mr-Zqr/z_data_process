# matplotlib 图像绘制相关代码
a = []
b = []
# 导入 matplotlib
import matplotlib.pyplot as plt
import numpy as np
# 设置 matplotlib 图像绘制参数
plt.rc('font',family='Times New Roman')
plt.rcParams['figure.subplot.right'] = 0.990
plt.rcParams['figure.subplot.left'] = 0.140
plt.rcParams['figure.subplot.top'] = 0.95
plt.rcParams['figure.subplot.bottom'] = 0.185
plt.rcParams['font.size'] = 12 
plt.figure(figsize=(4,4))


# 单图绘制
plt.scatter(a, b, s=5, linewidths= 2,color='tab:gray', label='contact gt')
plt.plot(a, b, '--', label='position gt.', color='tab:gray', linewidth=2)
plt.ylim(0.2,0.8)
plt.xlim(-1.5, -0.1)
plt.xlabel('X Position (m)',fontsize=14)
plt.ylabel('Y Position (m)',fontsize=14)
plt.xticks(np.arange(0, 130, 20), size = 12)
plt.yticks(np.arange(-0.05, 0.15, 0.05), size = 12)


# 图例绘制
leg = plt.legend(ncol = 2, loc='upper center', fontsize = 14)
# 去除边框和底色
leg.get_frame().set_alpha(0)
leg.get_frame().set_edgecolor('none')
# 定位
leg.set_bbox_to_anchor([1.7, 1.55])
# 将图例的线宽设置为3
for line in leg.get_lines():
    line.set_linewidth(2)


# 子图绘制
import matplotlib.gridspec as gridspec
fig = plt.figure()
# 建立3×5的网格
grid = gridspec.GridSpec(3,5)
# 设置图片的wspace
grid.update(wspace=0.6, hspace=0.1)
fig.tight_layout()

ax1 = fig.add_subplot(grid[0,:])
ax1.set_title('***',fontsize=14)
ax1.plot(a, b, label='***',linewidth=1, color='tab:green')
ax1.set_xlim(0,140)
plt.xticks(np.arange(0, 160,20))
ax1.set_ylabel('***',fontsize=14)

ax2 = fig.add_subplot(grid[1,:])
ax2.plot(a, b, label='**',linewidth=1,color='tab:orange')
ax2.set_xlim(0,140)
plt.xticks(np.arange(0, 160,20))
ax2.set_ylabel('**',fontsize=14)

ax3 = fig.add_subplot(grid[2,:])
ax3.plot(a, b, label='**',linewidth=1,color='tab:orange')
ax3.set_ylabel('**',fontsize=14)
ax3.set_xlim(0,140)
plt.xticks(np.arange(0, 160,20))
ax3.set_xlabel('**',fontsize=14)
# 取消ax1, ax2,的横坐标数字，但是保留刻度
plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)


# helper func
# x轴某一范围填充颜色
ax1.axvspan(40, 45, facecolor='gray', alpha=0.5)