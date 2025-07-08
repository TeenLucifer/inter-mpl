import numpy as np
from inter_mpl import InterMpl

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)

inter_mpl = InterMpl(figsize=(8, 6))
inter_mpl.plot(x_axis_data=x, y_axis_data=y1, label="sin(x)", color="blue", linewidth=2)
inter_mpl.plot(x_axis_data=x, y_axis_data=y2, label="cos(x)", color="red", linewidth=2)
inter_mpl.show()