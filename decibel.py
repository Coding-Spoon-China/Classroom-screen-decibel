"""UTF-8"""
"""Python3.11.4"""
"""decibel_v0.3"""
"""前期导入"""
import keyboard
import datetime
import pyaudio
import time
import json
import numpy as np
# from tkinter import Tk, Label
import matplotlib.pyplot as plt

# 假设 `volume_list` 是一个包含连续分贝值的列表
# 定义EMA系数 alpha，值越接近1，EMA对新数据反应越灵敏
alpha = 0.1

# 初始化EMA值
ema_value = 0

# # 初始化 PyAudio
# 定义一些常量
CHUNK_SIZE = 1024  # 每次读取的数据量
FORMAT = pyaudio.paInt16  # 数据格式
CHANNELS = 1  # 假设单声道
RATE = 44100  # 采样率
SCALE_FACTOR = (2.0 ** 15) - 1  # 对于16位量化音频的scale因子
p = pyaudio.PyAudio()

# # 打开默认音频输入设备
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

f = 0

# # 创建Tkinter GUI
# root = Tk()
# root.title("Real-time Sound Level Meter")
# label = Label(root, font=("Helvetica", 36), bg="black", fg="white")
# label.pack(pady=20)


def smooth_volume(volume):
    global ema_value
    ema_value = alpha * volume + (1 - alpha) * ema_value
    return ema_value

# 对实时数据进行平滑处理
# smoothed_volumes = []
# for vol in volume_list:
#     smoothed_vol = smooth_volume(vol)
#     smoothed_volumes.append(smoothed_vol)

def get_average_volume(data,rms_Magnification):
    # abs_data = np.abs(data)
    # # print(data)
    # return np.sqrt(np.mean(abs_data ** 2))
    signal = np.frombuffer(data, dtype=np.int16) / scale_factor  # 转换为浮点数
    rms = np.sqrt(np.mean(signal ** 2))
    db = rms_Magnification * np.log10(rms)
    print(db)
    return db

# def get_average_volume(frame_data):
#     # #volume = np.abs(frame_data).mean()
#     # volume = int(np.abs(frame_data).mean()* 10 / (2.0 ** 15 ) * 60)  # 使用均方根作为近似强度
#     # #balance(volume)
#     # if (volume - f)**2 < 400:
#     #     f = volume
#     #     print(volume)
#     # else:
#     #     print(f+5)
#     # #return v
    
#     # print(v)
#     # return v   # Normalize to approximately dBFS scale
#     volume = np.abs(frame_data).mean()  # 使用均方根作为近似强度
#     print(volume)
#     return volume * 10 / (2.0 ** 15)  # Normalize to approximately dBFS scale
    

def update_meter(increase,step,start_time,color):
    data = stream.read(CHUNK_SIZE)
    # print(data)
    level = smooth_volume(get_average_volume(np.frombuffer(data, dtype=np.int16),rms_Magnification))
    if level <=0:
        level = 0
    # level = smooth_volume(get_average_volume(np.frombuffer(data, )))
    print(type(level))
    # label.config(text=f"{level:.2f}")  # 显示两位小数的分贝值
    # root.after(100, update_meter)  # 每隔1000毫秒更新一次
    # ytime = time.strftime('%H:%M:%S', time.localtime(time.time()))
    M = time.strftime('%M', time.localtime(time.time()))
    S = time.strftime('%S', time.localtime(time.time()))
    # ytime = time.strftime('%H:%M', time.localtime(time.time()))
    # ytime = int(time.strftime('%M%S', time.localtime(time.time())))
    ytime = int(M + S)
    print(ytime)

    # # 设置参考区域
    # plt.axhspan(ymin=y_min,ymax=y_max, facecolor='y')
    
    x.append(ytime)# 添加i到x轴的数据中
    y.append(level + increase)# 添加i的平方到y轴的数据中
    plt.clf()  # 清除之前画的图
    print(x,y)
    
    # 设置参考区域
    plt.axhspan(ymin=y_min,ymax=y_max, facecolor=color)
    # plt.axhline(y=y_min)

    plt.axhline(y=y_min,c = 'r')

    # plt.ylabel("当前分贝："+str(int(level+increase)),loc='top')
    plt.title("当前分贝："+str(int(level+increase)))
    plt.plot(x, y)  # 画出当前x列表和y列表中的值的图形
    
    # plt.figure()
    # current_figure = plt.gcf()  # gcf() 获取当前figure
    # current_figure.canvas.set_window_title('New Window Title')  # 设置窗口标题
    plt.pause(0.01)  # 暂停一段时间，不然画的太快会卡住显示不出来
    plt.ioff()  # 关闭画图窗口
    time.sleep(step)

# 使用中文
plt.rcParams['font.sans-serif']=['SimHei']

# 获取修改权限
if str(input("Enter the administrator password or press any key to continue:")) == "3231106963":
    # 获取重要参数设置
    rms_Magnification = int(input("rms_Magnification:"))
    increase = int(input("increase:"))
    stop_time_m = int(input("stop_time_m(M/S):"))
    stop_time_e = int(input("stop_time_e(M/S):"))
    step = float(input("Time step:"))
    y_min = int(input("Y_min:"))
    y_max = int(input("Y_max:"))
    color = str(input("color"))
    data_main = {
        'rms_Magnification':rms_Magnification,
        'increase':increase,
        'stop_time_m':stop_time_m,
        'stop_time_e':stop_time_e,
        'step':step,
        'y_min':y_min,
        'y_max':y_max,
        'color':color,
        }
    with open('data.json', 'w') as f:
        json.dump(data_main, f)

else:
    with open('data.json', 'r') as f:
        data = json.load(f)
    rms_Magnification = data['rms_Magnification']
    increase = data['increase']
    stop_time_m = int(data['stop_time_m'])
    stop_time_e = int(data['stop_time_e'])
    step = data['step']
    y_min  = data['y_min']
    y_max  = data['y_max']
    color = data['color']

start_time = int(time.strftime('%M%S', time.localtime(time.time())))
# now_time = 0

# 计算每个采样的浮点值
bytes_per_sample = FORMAT // 8
scale_factor = (2.0 ** (8 * bytes_per_sample - 1)) - 1  # 根据量化位数计算scale因子

# 创建实时绘制横纵轴变量
x = []
y = []
 
# 创建绘制实时损失的动态窗口
plt.figure('分贝仪')
plt.ion()


# # 更新图表视图
# plt.draw()

# # 在主程序开始时立即启动更新循环
# while keyboard.is_pressed("esc") != True:
#     update_meter(increase)
if int(time.strftime('%H', time.localtime(time.time()))) < 12:
    stop_time = stop_time_m
else:
    stop_time = stop_time_e
while stop_time != int(time.strftime('%M%S', time.localtime(time.time()))) :
    update_meter(increase,step,start_time,color)
    
now=datetime.datetime.now()
plt.savefig(now.strftime("%Y-%m-%d_%H-%M-%S") + '.png', dpi=300)  # 保存为PNG格式
plt.show()

#root.mainloop()

# 结束时关闭音频流
stream.stop_stream()
stream.close()
p.terminate()