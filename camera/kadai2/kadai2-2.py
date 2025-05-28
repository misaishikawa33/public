# 全方位画像から透視投影画像を生成
# 正面画像の生成
# 入力の画角は視野角を表す

import numpy as np
import cv2
import sys


##
# 透視投影画像を生成する関数
def perspective_projection(Ie, Theta, Phi, Wp, Hp):
    # 正距円筒画像のサイズ
    He, We, _ = Ie.shape


    # 画角をラジアンに変換(π表記)
    theta = np.radians(Theta)
    phi = np.radians(Phi)


    # 画素間の長さΔx, Δy
    # 水平方向の画素間の長さΔx
    delta_x = 2*np.tan(theta/2) / Wp
    # 垂直方向の画素間の長さΔy
    delta_y = 2*np.tan(phi/2) / Hp


    # 透視投影画像Ipの初期化
    Ip = np.zeros((Hp, Wp, 3), dtype=np.uint8)


    # 透視投影画像Ipの画素(up, vp)から，3次元の視線ベクトルxを計算
    for vp in range(Hp):
        for up in range(Wp):
            x = np.array([
                [(up - Wp/2)*delta_x],
                [(vp - Hp/2)*delta_y],
                [1]
            ])

            # (θ, φ)の計算
            theta_x = np.arctan2(x[0,0], x[2,0])
            phi_x = - np.arctan2(x[1,0], np.sqrt(x[0,0]**2 + x[2,0]**2))


            # 正距円筒画像Ie上の対応する画素(ue, ve)の計算
            ue = int((theta_x + np.pi)*(We/(2*np.pi)))
            ve = int((np.pi/2 - phi_x)*(He/np.pi))


            # 画素値を透視投影画像Ipの画素(up, vp)に割り当てる
            Ip[vp, up] = Ie[ve, ue]

    return Ip
##


def main():
    # パラメータの設定
    Ie = cv2.imread(sys.argv[1])  # 入力画像の読み込み
    Theta = float(sys.argv[2])    # 水平方向の画角θ
    Phi = float(sys.argv[3])      # 垂直方向の画角φ
    Hp = int(sys.argv[4])         # 出力画像Ipの画像サイズ（高さ)
    Wp = int(sys.argv[5])         # 出力画像Ipの画像サイズ（幅)


    # 透視投影画像の生成
    print("全方位画像から透視投影画像を生成しています")
    Ip = perspective_projection(Ie, Theta, Phi, Wp, Hp)

    # 画像の保存，出力
    cv2.imwrite("Perspective Image.jpg", Ip)
    print("透視投影画像が保存されました")


if __name__ == "__main__":
    main()