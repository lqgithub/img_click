import os
import time
import cv2
import numpy as np
import pyautogui
import threading
import keyboard
import sys
import tkinter as tk
from tkinter import filedialog,messagebox
from PIL import Image,ImageTk,ImageGrab
class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.title(".0_0.")
        self.root.geometry("300x200")
        self.label = tk.Label(root, text="未选择图片")
        self.label.pack(pady=20)

        self.button1 = tk.Button(root, text="选择图片", command=self.select_image)
        self.button1.pack(pady=10)  # 设置水平和垂直间距
        self.button2 = tk.Button(root, text="开始 or 重启", command=self.start)
        self.button2.pack(side=tk.LEFT,padx=40) 
        self.button3 = tk.Button(root, text="终止进程", command=self.quit)
        self.button3.pack(side=tk.RIGHT,padx=(0,40)) 

        self.runnum = 0
        self.image_path = None
        self.running = False  # 循环控制器
        self.lock = threading.Lock()
        self.escape_thread = None # 存储ESC键监听线程
    

    # 监听ESC键的线程函数
    def listen_for_escape(self):
        keyboard.wait('esc')  # 等待ESC键被按下
        with self.lock:  # 使用锁来确保修改running变量的线程安全
            self.running = False  # 设置标志变量为False，以中断主循环
            messagebox.showinfo("提示", "已关闭进程")
    def select_image(self):
        if self.image_path:
            self.running = False
            messagebox.showwarning("注意", "重新选择图片需要重启进程")
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.label.config(text="已选择图片:" + self.image_path)
        else:
            self.label.config(text="未选择图片")
    
    def loop_default(self):
        while self.running and self.image_path:
            # 加载模板图像（你要匹配的小图）
            template_image_path = self.image_path
            template = cv2.imread(template_image_path, 0)  # 以灰度模式读取
            w, h = template.shape[::-1]  # 获取模板图像的宽度和高度
            
            # 截取当前屏幕图像
            screen = np.array(ImageGrab.grab())
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
            
            # 使用模板匹配算法
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # 设置匹配阈值，根据实际情况调整
            loc = np.where(res >= threshold)
                
            # 获取匹配区域的中心点坐标（注意：如果有多个匹配区域，这里只取第一个）
            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):
                    center_x = pt[0] + w // 2
                    center_y = pt[1] + h // 2
                    # 打印中心点坐标（用于调试）
                    print(f'Matched center: ({center_x}, {center_y})')
                    
                    # 模拟鼠标点击
                    pyautogui.click(center_x, center_y)
                    # 可选：点击后等待一段时间，以便观察效果
                    break  # 找到第一个匹配后就退出循环
            else:
                print('No match found')
                self.runnum += 1
                if self.runnum > 240:
                    self.running = False
                    messagebox.showinfo("提示", "未找到符合图片")
            time.sleep(0.5) # 休眠0.5秒

    def start(self):
        self.runnum = 0
        if not self.image_path:
            return messagebox.showinfo("提示", "未选择图片无法开始")
        self.escape_thread = threading.Thread(target=self.listen_for_escape)
        self.escape_thread.start()
        print('start')
        if not self.running:
            self.running = True
            loop_thread = threading.Thread(target=self.loop_default)
            loop_thread.start()
            print("循环已启动")

    def quit(self):
        if self.running:
            self.running = False
            messagebox.showinfo("提示", "已关闭进程")
        else:
            messagebox.showinfo("提示", "进程未运行")

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)  # 窗口置顶
    app = MainWindow(root)
    root.mainloop()