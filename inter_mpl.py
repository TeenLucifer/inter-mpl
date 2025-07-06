import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
from typing import Sequence
from matplotlib.figure import Figure, SubFigure, FigureBase, figaspect

class InterMpl():
    """
    可交互的matplotlib绘图, 支持点击和拖动
    """
    def __init__(
        self,
        num = None,
        figsize = None,
        dpi = None,
        facecolor = None,
        edgecoloe = None,
        frameon = True, 
        FigureClass = Figure,
        clear = False,
        xticks_density = 30,
        **kwargs
    ) -> None:
        """
        初始化成员变量
        """
        self.fig = plt.figure(
            num=num,
            figsize=figsize,
            dpi=dpi,
            facecolor=facecolor,
            edgecolor=edgecoloe,
            frameon=frameon,
            FigureClass=FigureClass,
            clear=clear
        )
        self.plot_ax = plt.gca()
        self.xticks_density = xticks_density # 横轴刻度的密度
        self.cursor: mplcursors.Cursor = None

        ## 绑定鼠标事件响应函数
        if self.fig is not None:
            self.fig.canvas.mpl_connect('scroll_event',         self.mouse_toggle_event)
            self.fig.canvas.mpl_connect('button_press_event',   self.mouse_toggle_event)
            self.fig.canvas.mpl_connect('button_release_event', self.mouse_toggle_event)
            self.fig.canvas.mpl_connect('motion_notify_event',  self.mouse_toggle_event)

        # 本图鼠标点击事件参数
        self.mouse_press = False
        self.mouse_move_start_x = 0
        self.mouse_move_start_y = 0
        self.mouse_move_rx = 0.0   # 鼠标移动横向比例, 用于和其它子图同步
        self.mouse_move_ry = 0.0   # 鼠标移动纵向比例, 用于和其它子图同步
        self.mouse_scroll_rx = 1.0 # 鼠标滚轮横向缩放比例, 用于和其它子图同步
        self.mouse_scroll_ry = 1.0 # 鼠标滚轮纵向缩放比例, 用于和其它子图同步

    def plot(
            self,
            x_axis_data: np.ndarray,
            y_axis_data: np.ndarray,
            label: str | None = None,
            color: str | None = None,
            linewidth: float | None = None
        ) -> None:
            """
            画图和绘制曲线
            """
            plt.plot(x_axis_data, y_axis_data, label=label, color=color, linewidth=linewidth)

    def show(self):
        self.cursor = mplcursors.cursor(multiple=True)
        self.cursor.connect("add", self.update_cursor_annotation)
        x_min, x_max = self.plot_ax.get_xlim()
        y_min, y_max = self.plot_ax.get_ylim()
        plt.grid()
        plt.legend(fontsize=8)
        plt.tick_params(axis='x', rotation=20)
        plt.xticks(np.linspace(x_min, x_max, self.xticks_density))
        plt.show()

    def update_cursor_annotation(self, cursor: mplcursors._mplcursors.Cursor) -> None:
        """
        更新鼠标点击曲线显示的标签信息
        """
        cursor_text = f'{cursor.artist._label}\nx: {cursor.target[0]:.4f}\ny: {cursor.target[1]:.4f}'

        cursor.annotation.set_text(cursor_text)

    def mouse_toggle_event(self, event: matplotlib.backend_bases.MouseEvent) -> None:
        """
        鼠标事件回调函数, 实现右键按住空白处拖动, 滚轮缩放
        """
        if self.plot_ax == event.inaxes and \
           (event.name == 'button_press_event' or event.name == 'scroll_event' or\
            event.name == 'button_press_event' or event.name == 'button_release_event' or \
            (event.name == 'motion_notify_event' and event.button == 3 and self.mouse_press == True)):
            # 获取本图横纵轴范围
            x_min, x_max = self.plot_ax.get_xlim()
            y_min, y_max = self.plot_ax.get_ylim()
            subplot_width = x_max - x_min
            subplot_height = y_max - y_min
            updated_x_min = x_min
            updated_x_max = x_max
            updated_y_min = y_min
            updated_y_max = y_max

            # 滚轮缩放事件响应
            if event.name == 'scroll_event':
                scale_factor = 0.9 if event.button == 'up' else 1.1
                fig_width_px, fig_height_px = self.fig.canvas.get_width_height()

                if event.xdata > (x_min + subplot_width / 5.0):
                    self.mouse_scroll_rx = scale_factor # 横轴缩放系数
                    self.mouse_scroll_ry = 1.0          # 纵轴缩放系数

                    # 横轴缩放参数
                    x_mid = (x_max + x_min) / 2.0
                    updated_x_min = x_mid - (subplot_width / 2.0) * self.mouse_scroll_rx
                    updated_x_max = x_mid + (subplot_width / 2.0) * self.mouse_scroll_rx
                else:
                    self.mouse_scroll_rx = 1.0          # 横轴缩放系数
                    self.mouse_scroll_ry = scale_factor # 纵轴缩放系数

                    # 纵轴缩放参数
                    y_mid = (y_max + y_min) / 2.0
                    updated_y_min = y_mid - (subplot_height / 2.0) * self.mouse_scroll_ry
                    updated_y_max = y_mid + (subplot_height / 2.0) * self.mouse_scroll_ry

            # 鼠标拖动事件响应
            if event.name == 'button_press_event' and event.button == 3:
                self.mouse_press = True
                self.mouse_move_start_x = event.xdata
                self.mouse_move_start_y = event.ydata
            elif event.name == 'button_release_event' and event.button == 3:
                self.mouse_press = False
            elif event.name == 'motion_notify_event' and event.button == 3 and self.mouse_press:
                mx = event.xdata - self.mouse_move_start_x
                my = event.ydata - self.mouse_move_start_y
                self.mouse_move_rx = mx / subplot_width
                self.mouse_move_ry = my / subplot_height

                updated_x_min = x_min - mx
                updated_x_max = x_min - mx + subplot_width
                updated_y_min = y_min - my
                updated_y_max = y_min - my + subplot_height

            self.plot_ax.set_xlim(updated_x_min, updated_x_max)
            self.plot_ax.set_ylim(updated_y_min, updated_y_max)
            self.plot_ax.set_xticks(np.linspace(updated_x_min, updated_x_max, self.xticks_density))
            self.fig.canvas.draw_idle()