# 模拟鼠标点击

## 窗口创建
1. tkinter模块
    ```
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
    ```

## 图片选择
1. 选中图片才可以进行模拟点击
2. 重新选择 需要重启进程

## 模拟点击
python opencv联动pyautogui

    ```
    screen = np.array(ImageGrab.grab())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    # 使用模板匹配算法
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 设置匹配阈值，根据实际情况调整
    loc = np.where(res >= threshold) # 匹配数组
    pyautogui.click(center_x, center_y) # 模拟鼠标点击
    ```

## 终止进程
1. 按钮终止
2. 按ESC键终止
    添加esc监听，esc可以退出
