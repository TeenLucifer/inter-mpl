import matplotlib.pyplot as plt
import numpy as np
from inter_mpl import InterMpl

# 设置中文字体显示（如果需要在图中显示中文）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成数据
x = np.linspace(0, 10, 100)  # 从0到10生成100个等间距的点
y1 = np.sin(x)  # 计算每个x点的正弦值
y2 = np.cos(x)
y3 = np.tan(x)

inter_mpl = InterMpl(figsize=(8, 6))
inter_mpl.plot(x_axis_data=x, y_axis_data=y1, label="sin(x)", color="blue", linewidth=2)
inter_mpl.plot(x_axis_data=x, y_axis_data=y2, label="cos(x)", color="red", linewidth=2)
inter_mpl.show()