# import
import math
import random
import pathlib
import numpy as np  # whole numpy lib is available, prepend "np."
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
import os  # handy system and path functions
import sys  # to get file system encoding
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard

# ファイル準備
# Ensure that relative paths start from the same directory as this script
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
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
csvFile = new_filepath + ".csv"

# ファイルが存在する場合はキャンセル
if os.path.isfile(csvFile):
    print(csvFile + " exists!")
    core.quit()
else:
    datafile = open(csvFile, mode="x", encoding='utf-8')  # mode = "a"だと追記可能，"x"だと新規作成のみ可能
    datafile.write("central_size,flanker_size,response,reaction_time\n")  # 列名をつけておく

# windowの準備
win = visual.Window(
    monitor="testMonitor",  # 自分で設定したモニター設定名を読み込む
    units="deg",  # 表示する単位，ここでは視野角
    fullscr=True,  # フルスクリーン表示
    color=[0, 0, 0]  # 色強度は-1.0から1.0の実数で指定
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
    visible=0  # 1で表示，0で非表示
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
    flanker_size = size_cond[delta_size_cond]
    print(trial_ID)
    print(flanker_size)

    # 実験内容の説明
    if trial_ID == 0:
        inst = visual.ImageStim(win, "inst.png")  # 1. 画像刺激の準備
        inst.size = (21, 7)
        inst.draw()
        win.flip()
        event.waitKeys(keyList=["space"])

    # 中央円の描画
    central_circle.radius = central_size_L0
    central_circle.pos = (0, 0)
    central_circle.draw()

    # フランカー円の描画
    for pos in flanker_positions:
        flanker_circle.radius = flanker_size
        flanker_circle.pos = pos
        flanker_circle.draw()

    # 画面に反映
    win.flip()

    # 反応時間記録のために時間を0にリセット
    stopwatch.reset()
    resp = event.waitKeys(keyList=["up", "down", "escape"], timeStamped=stopwatch)

    # データの保存
    key = resp[0][0]  # 反応キーの取得
    rt = resp[0][1]  # 反応時間の取得
    print(key)
    print(rt)

    # check for quit (typically the Esc key)
    if key == "escape":
        break

    # 解答はフランカー円が大きいか小さいかで記録する
    if key == "up":
        answer = "larger"
    else:
        answer = "smaller"

    # 結果をファイルに書き込む
    data = "{},{},{},{}\n".format(central_size_L0, flanker_size, answer, rt)  # カンマ区切りの文字列にする
    datafile.write(data)  # ファイルに書き込む

    trial_ID = trial_ID + 1  # ループごとにtrial_IDを1増やす

    # 注視点の表示
    win.flip()
    # 250 ms待機
    core.wait(0.5)

# ループ外で終了処理
datafile.close()  # ファイルを閉じる
win.close()  # 画面を閉じる
core.quit()
