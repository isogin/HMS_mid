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
expName = "MullerLyer"
expInfo = {"participant": "", "session": "001"}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
new_filename = "MullerLyer_{}_{}".format(expInfo["participant"],expInfo["session"])
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
	datafile = open(csvFile, mode = "x", encoding='utf-8') # mode = "a"だと追記可能，"x"だと新規作成のみ可能
	datafile.write("outward_length,inward_length,angle,response,reaction_time\n") # 列名をつけておく

# windowの準備
win = visual.Window(
	monitor="testMonitor", # 自分で設定したモニター設定名を読み込む
	units = "deg", # 表示する単位，ここでは視野角
	fullscr = True, # フルスクリーン表示
	color = [0, 0, 0] # 色強度は-1.0から1.0の実数で指定
)

# 線の準備
line = visual.Line(
	win = win,
	units = "deg", # 線の長さの単位
	lineColor = [-1, -1, -1] # 色強度は-1.0から1.0の実数で指定
)
line.lineWidth = 4 # 線の太さ, ここだけpixelサイズでの指定

# マウスカーソル設定
mouse = event.Mouse(
	win = win,
	visible = 0 # 1で表示，0で非表示
)

# 矢印の基準長さ
# 内向き矢印は常に基準長さにする
inward_length_L0 = 6 # degree

# 基準長さの矢印に対して，もう片方の矢印の長さをどれくらいの範囲で調節するか
# 値の指定は[最も短くする範囲 最も長くする範囲]．絶対値を揃えること
abs_delta = 2 # degree
delta_x_range = [-1*abs_delta, abs_delta]

# 上で指定したdelta_x_rangeの範囲を何分割して矢印の長さを変更するのかを指定する
# 上下の矢印の長さが全く同じになる状況を含めるために，指定する値は奇数にすること．
cond_num = 11
width_cond = np.linspace(delta_x_range[0], delta_x_range[1], cond_num)

# repeat_numで指定した回数だけ各条件での刺激が繰り返し提示される
# 例えば，5を指定すると，上が外向き，下が内向きの刺激が5回,上が内向き,下が外向きの刺激が5回提示される
repeat_num = 2

# 総試行回数. deltaXの条件数 * 各条件での繰り返し数
trial_num = cond_num * repeat_num
bar_distance = 2	# 上下の線の間の距離 # degree
arrow_length = 1	# 矢羽の長さ # degree
arrow_arg = 30		# 矢羽の角度 # degree

# 長さの条件をランダムに決定する
delta_x_cond_order = list(range(cond_num)) * repeat_num * 2
random.shuffle(delta_x_cond_order)

# 刺激提示順をランダムに決定する
# 1: 上が内向き,下が外向き 2: 上が外向き,下が内向き
arrow_cond_order = [1, 2] * trial_num
random.shuffle(arrow_cond_order)

# 矢印の描画に必要な値で，あらかじめ計算できるものを計算しておく
# centerの座標は(0,0)
# 棒のy座標
top_bar_y = bar_distance / 2
bot_bar_y = bar_distance / 2 * (-1)
# 矢羽
arrow_x = arrow_length * math.cos(arrow_arg * math.pi / 180)
arrow_y = arrow_length * math.sin(arrow_arg * math.pi / 180)

# このあたりで注視点表示の項目を用意
fixation = visual.ImageStim(win, "bulseye.png") # 1. 画像刺激の準備
fixation.size = 0.5

# 実験時に使う変数を用意
trial_ID = 0
stopwatch = core.Clock()

for arrow_cond in arrow_cond_order:
	# 内向きの長さを基準に，外向きの長さを変更する
	outward_bar_length = inward_length_L0 + width_cond[delta_x_cond_order[trial_ID]]
	print(trial_ID)
	print(outward_bar_length)

	# 矢羽の向きで区別する
	if arrow_cond == 1:
		# 内向きの設定
		inward_bar_left_x = inward_length_L0 / 2 * (-1)
		inward_bar_left_y = top_bar_y
		inward_bar_right_x = inward_length_L0 / 2
		inward_bar_right_y = top_bar_y
		# 外向きの設定
		outward_bar_left_x = outward_bar_length / 2 * (-1)
		outward_bar_left_y = bot_bar_y
		outward_bar_right_x = outward_bar_length / 2
		outward_bar_right_y = bot_bar_y
	else:
		# 外向きの設定
		outward_bar_left_x = outward_bar_length / 2 * (-1)
		outward_bar_left_y = top_bar_y
		outward_bar_right_x = outward_bar_length / 2
		outward_bar_right_y = top_bar_y
		# 内向きの設定
		inward_bar_left_x = inward_length_L0 / 2 * (-1)
		inward_bar_left_y = bot_bar_y
		inward_bar_right_x = inward_length_L0 / 2
		inward_bar_right_y = bot_bar_y

	# 実験内容の説明
	if trial_ID == 0:
		inst = visual.ImageStim(win, "inst.png") # 1. 画像刺激の準備
		inst.size = (21, 7)
		inst.draw()
		win.flip()
		event.waitKeys(keyList = ["space"])

	# 注視点の表示
	fixation.draw()

	# 矢印の描画
	# 外向き
	line.start = [outward_bar_left_x, outward_bar_left_y]
	line.end = [outward_bar_right_x, outward_bar_right_y]
	line.draw()
	# 左上
	line.start = [outward_bar_left_x, outward_bar_left_y]
	line.end = [outward_bar_left_x + arrow_x, outward_bar_left_y + arrow_y]
	line.draw()
	# 左下
	line.start = [outward_bar_left_x, outward_bar_left_y]
	line.end = [outward_bar_left_x + arrow_x, outward_bar_left_y - arrow_y]
	line.draw()
	# 右上
	line.start = [outward_bar_right_x, outward_bar_right_y]
	line.end = [outward_bar_right_x - arrow_x, outward_bar_right_y + arrow_y]
	line.draw()
	# 右下
	line.start = [outward_bar_right_x, outward_bar_right_y]
	line.end = [outward_bar_right_x - arrow_x, outward_bar_right_y - arrow_y]
	line.draw()
	# 内向き
	line.start = [inward_bar_left_x, inward_bar_left_y]
	line.end = [inward_bar_right_x, inward_bar_right_y]
	line.draw()
	# 左上
	line.start = [inward_bar_left_x, inward_bar_left_y]
	line.end = [inward_bar_left_x - arrow_x, inward_bar_left_y + arrow_y]
	line.draw()
	# 左下
	line.start = [inward_bar_left_x, inward_bar_left_y]
	line.end = [inward_bar_left_x - arrow_x, inward_bar_left_y - arrow_y]
	line.draw()
	# 右上
	line.start = [inward_bar_right_x, inward_bar_right_y]
	line.end = [inward_bar_right_x + arrow_x, inward_bar_right_y + arrow_y]
	line.draw()
	# 右下
	line.start = [inward_bar_right_x, inward_bar_right_y]
	line.end = [inward_bar_right_x + arrow_x, inward_bar_right_y - arrow_y]
	line.draw()

	# 画面に反映
	win.flip()

	# 反応時間記録のために時間を0にリセット
	stopwatch.reset()
	resp = event.waitKeys(keyList = ["up", "down", "escape"], timeStamped = stopwatch)

	# データの保存
	key = resp[0][0] # 反応キーの取得
	rt = resp[0][1] # 反応時間の取得
	print(key)
	print(rt)

	# check for quit (typically the Esc key)
	if key == "escape":
		break

	# 解答は外向きと内向きの矢印どっちが長いかで記録する
	if arrow_cond == 1:
		if key == "up":
			answer = "in"
		else:
			answer = "out"
	elif arrow_cond == 2:
		if key == "up":
			answer = "out"
		else:
			answer = "in"

	# 結果をファイルに書き込む
	# 内容: 内向きの長さ，外向きの長さ，矢羽角度，回答，反応時間
	data = "{},{},{},{},{}\n".format(outward_bar_right_x-outward_bar_left_x, inward_bar_right_x-inward_bar_left_x, arrow_arg, answer, rt) # カンマ区切りの文字列にする
	datafile.write(data) # ファイルに書き込む

	print(outward_bar_right_x-outward_bar_left_x)

	trial_ID = trial_ID + 1 # ループごとにtrial_IDを1増やす

	# 注視点の表示
	fixation.draw()
	# 画面に反映
	win.flip()
	# 250 ms待機
	core.wait(0.5)

# ループ外で終了処理
datafile.close() # ファイルを閉じる
win.close() # 画面を閉じる



