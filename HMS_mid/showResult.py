# import
import numpy as np
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os  # handy system and path functions
import sys  # to get file system encoding

#
# 設定する必要のあるパラメータ
#
# シグモイド関数 y = 1/(1 + exp(-(x - x0)/a)) へのカーブフィッティングの初期値
a_init = 0.4
x0_init = -0.5
# フィッティング許容誤差
fTolVal = 1e-8
xTolVal = 1e-8
# 読み込むデータの設定
participant_name = "YM"
session_num = "001"


# ファイル準備
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = "showResult"
expInfo = {"participant": participant_name, "session": session_num}
new_filename = "MullerLyer_{}_{}".format(expInfo["participant"],expInfo["session"])
new_filepath = os.path.join(".", "data", new_filename)
csvFileIn = new_filepath + ".csv"
csvFileOut = new_filepath + "_pf.csv"

# csvファイルの読み込み
df = pd.read_csv(csvFileIn, encoding="utf-8")

# シグモイド関数定義
def sigmoid(x, x0, a):
	y = 1 / (1 + np.exp(-(x-x0)/a))
	return y

# データを項目ごとに抽出
inward_length = df["inward_length"] # 矢羽内向きの線分長さ
outward_length = df["outward_length"] # 矢羽外向きの線分長さ
arrow_angle = df["angle"] # 矢羽の角度
response = df["response"] # 被験者の回答（1 = 内向きが長い, 2 = 外向きが長い）
rt = df["reaction_time"] # 反応時間（回答までの時間, ms）

# 矢羽内向きの線分長さと矢羽外向きの線分長さの差の計算
delta = inward_length - outward_length
print(delta)

# 差の条件が何種類あるかを算出
u_delta = delta.unique()
u_delta = np.sort(u_delta) # uniqueの結果を小さい順にソート
print(u_delta)

# 差の条件ごとに被験者が矢羽内向きの方が長いと答えた確率を計算
# 一致するindexを取得し，その条件下での内向きという回答の割合を計算する
cnt = 0
prob_inward = pd.Series([])
for cond_delta in u_delta:
	cond_data = delta[delta == cond_delta] # 条件下での結果を抽出
	prob_inward[cnt] = np.count_nonzero(response[cond_data.index]=='in') / len(cond_data.index) # inと回答した割合を記録
	cnt = cnt + 1

print(prob_inward)

# 結果の図を作成
plt.plot(u_delta, prob_inward, color='red', marker='o', linestyle='-')
# 体裁を整える
plt.xlabel("Inward - Outward length (Deg.)")
plt.ylabel("Prob. (inward is longer)")
plt.ylim(0,1)
plt.xlim(min(u_delta), max(u_delta))
plt.yticks([0, 0.25, 0.5, 0.75, 1])
plt.tight_layout()
plt.grid()

# シグモイド関数 y = 1/(1 + exp(-(x - x0)/a)) へのカーブフィッティング
xs_fit = np.linspace(min(u_delta), max(u_delta), 100)
try:
    popt, pcov = curve_fit(sigmoid, u_delta, prob_inward, [x0_init, a_init], ftol=fTolVal, xtol=xTolVal, maxfev=10000)    
    ys_fit = sigmoid(xs_fit, *popt)
    print(popt)
    print("x0 = " + str(popt[0]))
    print("a = " + str(popt[1]))
    
    # 被験者の回答確率にフィッティングの結果を重ねる
    plt.plot(xs_fit, ys_fit, color='black', linestyle='-')
    
    # psychometric function (フィッティング前)の値のファイル出力
    data = pd.DataFrame({'delta_in_out': u_delta, 'prob_inward': prob_inward})
    data.to_csv(csvFileOut, mode="w", index=False) # mode = "w"により上書きされるので注意

except RuntimeError as e:
    print(e)
    print('=== Bad fitting: try another initial parameters, increase tolerance, or decrease x range tested in experients ===')
    ys_fit = sigmoid(xs_fit, x0_init, a_init)

    # 被験者の回答確率に初期値で設定したsigmoid関数を重ねる
    plt.plot(xs_fit, ys_fit, color='black', linestyle='--')

# figureの保存
fig_name = new_filepath + ".png"
plt.savefig(fig_name)

# figureの表示
plt.show()

# end
