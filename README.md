# 模拟鼠标点击

## 版本信息

此版本为v3+

## 窗口创建
**tkinter模块**

```
import tkinter as tk
root = tk.Tk()
```

## 图片选择

1. 选中图片才可以进行模拟点击
2. 重新选择 需要重启进程
3. 选择图片后，点击按钮，进行模拟点击
4. 进程效果可能会受计算机缩放比影响
5. 图片大小截图页面原始大小

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

## 依赖安装

**推荐python 3.10 +**

~~requirements.txt 暂时有问题，自己根据情况安装吧~~
```bash
pip install -r requirements.txt
```

## 打包

**pyinstaller会根据不同系统打不同的包，当前并未适配window以外的系统**

```bash
pyinstaller --onefile index.py
```

### icon的生成
1. 编辑 .spec 文件： 
```spec
exe = EXE(
    # 其他参数...
    icon='myicon.ico',
    # 其他参数...
)
```
2. 打包：
```bash
pyinstaller --onefile --icon=myicon.ico index.py
```


## 异常

1. mac定位有异常，正常/2可以，没有找到具体原因，目前暂未真正解决
2. 图片查找时匹配度0.85，可能会出现多个同位置的匹配异常，可以尝试调整匹配度，未添加解决