# import
import math
import random
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
				   sqrt, std, deg2rad, rad2deg, linspace, asarray)
import os
from psychopy import gui, visual, core, data, event, logging

# ファイル準備
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = "Ebbinghaus"
expInfo = {"participant": "", "session": "001"}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
new_filename = "Ebbinghaus_{}_{}".format(expInfo["participant"], expInfo["session"])
new_filepath = os.path.join(".", "data", new_filename)

# save a log file for detail verbose info
logFile = logging.LogFile(new_filepath + ".log", level=logging.EXP)
logging.console.setLevel(logging.WARNING)
csvFile = new_filepath + ".csv"

# ファイルが存在する場合はキャンセル
if os.path.isfile(csvFile):
    print(csvFile + " exists!")
    core.quit()
else:
    datafile = open(csvFile, mode="x", encoding='utf-8')
    datafile.write("left_flanker_size,right_flanker_size,response,reaction_time\n")

# windowの準備
win = visual.Window(
    monitor="testMonitor",
    units="deg",
    fullscr=True,
    color=[0, 0, 0]
)

# 円の準備
central_circle = visual.Circle(
    win=win,
    units="deg",
    lineColor=[-1, -1, -1],
    fillColor=[-1, -1, -1]
)

flanker_circle = visual.Circle(
    win=win,
    units="deg",
    lineColor=[-1, -1, -1],
    fillColor=[-1, -1, -1]
)

# マウスカーソル設定
mouse = event.Mouse(
    win=win,
    visible=0
)

# 中央の円の基準サイズ
central_size_L0 = 1  # degree

# フランカー円のサイズの範囲を指定
abs_delta = 2  # degree
delta_size_range = [central_size_L0 - abs_delta, central_size_L0 + abs_delta]

# フランカー円のサイズの条件数
cond_num = 11
size_cond = np.linspace(delta_size_range[0], delta_size_range[1], cond_num)

# repeat_numで指定した回数だけ各条件での刺激が繰り返し提示される
repeat_num = 2

# 総試行回数. delta_sizeの条件数 * 各条件での繰り返し数
trial_num = cond_num * repeat_num

# フランカー円の配置
flanker_distance = 3  # フランカー円と中央円の距離 # degree
flanker_positions = [(cos(i * pi / 3) * flanker_distance, sin(i * pi / 3) * flanker_distance) for i in range(6)]

# 長さの条件をランダムに決定する
delta_size_cond_order = list(range(cond_num)) * repeat_num
random.shuffle(delta_size_cond_order)

# 実験時に使う変数を用意
trial_ID = 0
stopwatch = core.Clock()

for delta_size_cond in delta_size_cond_order:
    left_flanker_size = size_cond[delta_size_cond]
    right_flanker_size = size_cond[delta_size_cond_order[(trial_ID + cond_num // 2) % cond_num]]
    print(trial_ID)
    print(left_flanker_size, right_flanker_size)

    # 実験内容の説明
    if trial_ID == 0:
        inst = visual.ImageStim(win, "inst.png")
        inst.size = (21, 7)
        inst.draw()
        win.flip()
        event.waitKeys(keyList=["space"])

    # 左側のエビングハウス錯視の描画
    for pos in flanker_positions:
        flanker_circle.radius = left_flanker_size
        flanker_circle.pos = (-8 + pos[0], pos[1])
        flanker_circle.draw()

    central_circle.radius = central_size_L0
    central_circle.pos = (-8, 0)
    central_circle.draw()

    # 右側のエビングハウス錯視の描画
    for pos in flanker_positions:
        flanker_circle.radius = right_flanker_size
        flanker_circle.pos = (8 + pos[0], pos[1])
        flanker_circle.draw()

    central_circle.radius = central_size_L0
    central_circle.pos = (8, 0)
    central_circle.draw()

    # 画面に反映
    win.flip()

    # 反応時間記録のために時間を0にリセット
    stopwatch.reset()
    resp = event.waitKeys(keyList=["left", "right", "escape"], timeStamped=stopwatch)

    # データの保存
    key = resp[0][0]
    rt = resp[0][1]
    print(key)
    print(rt)

    if key == "escape":
        break

    # 解答は左の錯視か右の錯視のどちらが中央円が大きいかで記録する
    if key == "left":
        answer = "left"
    else:
        answer = "right"

    data = "{},{},{},{}\n".format(left_flanker_size, right_flanker_size, answer, rt)
    datafile.write(data)

    trial_ID += 1

    # 注視点の表示
    win.flip()
    core.wait(0.5)

# ループ外で終了処理
datafile.close()
win.close()
core.quit()
