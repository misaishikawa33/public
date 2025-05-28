# 全方位画像から透視投影画像を生成
# 1. カメラ座標系の各軸周りの回転角度を与えて, 透視投影画像を生成する

import numpy as np
import cv2
import sys


##
# 透視投影画像を生成する関数
def perspective_projection(Ie, Theta, Phi, Wp, Hp, theta_eye, phi_eye, psi_eye):
    # 正距円筒画像のサイズ
    He, We, _ = Ie.shape


    # 画角をラジアンに変換(π表記)
    theta = np.radians(Theta)
    phi = np.radians(Phi)
    theta_eye = np.radians(theta_eye)
    phi_eye = np.radians(phi_eye)
    psi_eye = np.radians(psi_eye)


    # 正距円筒画像Ie上の対応する画素(ue, ve)の計算
    ue = int((theta_eye + np.pi)*(We/(2*np.pi)))
    ve = int((np.pi/2 - phi_eye)*(He/np.pi))


    # 画素間の長さΔx, Δy
    # 水平方向の画素間の長さΔx
    delta_x = 2*np.tan(theta/2) / Wp
    # 垂直方向の画素間の長さΔy
    delta_y = 2*np.tan(phi/2) / Hp


    # 回転行列R(θeye, φeye)の計算
    R_theta = np.array([[ np.cos(theta_eye), 0, np.sin(theta_eye) ],
                            [ 0, 1, 0 ],
                            [ -np.sin(theta_eye), 0, np.cos(theta_eye) ]])
    
    R_phi = np.array([[ 1, 0, 0 ],
                      [ 0, np.cos(phi_eye), -np.sin(phi_eye) ],
                      [ 0, np.sin(phi_eye), np.cos(phi_eye) ]])
    
    R_theta_phi = np.dot(R_theta, R_phi)
    

    # ベクトルvを回転行列R(θeye, φeye)によって回転
    # ベクトル v = (0, 0, 1)^Tにより正規化され，単位ベクトルを得る
    v = np.array([[0], [0], [1]])
    Rv = np.dot(R_theta_phi, v)


    # R(ψeye)を求める
    R_psi = np.array([[ Rv[0,0]**2 * (1-np.cos(psi_eye)) + np.cos(psi_eye),  Rv[0,0]*Rv[1,0] * (1-np.cos(psi_eye)) - Rv[2,0]*np.sin(psi_eye),  Rv[2,0]*Rv[0,0] * (1-np.cos(psi_eye)) + Rv[1,0]*np.sin(psi_eye) ],
                      [ Rv[0,0]*Rv[1,0] * (1-np.cos(psi_eye)) + Rv[2,0]*np.sin(psi_eye),  Rv[1,0]**2 * (1-np.cos(psi_eye)) + np.cos(psi_eye),  Rv[1,0]*Rv[2,0] * (1-np.cos(psi_eye)) - Rv[0,0]*np.sin(psi_eye) ],
                      [ Rv[2,0]*Rv[0,0] * (1-np.cos(psi_eye)) - Rv[1,0]*np.sin(psi_eye),  Rv[1,0]*Rv[2,0] * (1-np.cos(psi_eye)) + Rv[0,0]*np.sin(psi_eye),  Rv[2,0]**2 * (1-np.cos(psi_eye)) + np.cos(psi_eye) ]
                      ])
    
    

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

            # 視点ベクトルxを回転する
            xd = np.dot(R_psi, np.dot(R_theta_phi, x))

            # (θ, φ)の計算（ラジアンから度に変換）
            theta_xd = np.arctan2(xd[0,0], xd[2,0])
            phi_xd = - np.arctan2(xd[1,0], np.sqrt(xd[0,0]**2 + xd[2,0]**2))


            # 正距円筒画像Ie上の対応する画素(ue, ve)の計算
            ue = int((theta_xd + np.pi)*(We/(2*np.pi)))
            ve = int((np.pi/2 - phi_xd)*(He/np.pi))


            # 画素値を透視投影画像Ipの画素(up, vp)に割り当てる
            Ip[vp, up] = Ie[ve-1, ue-1]

    return Ip
##



## 画角から出力画像サイズを求める関数
def size(Ie, Theta, Phi):
    He, We, _ = Ie.shape

    phi = np.radians(Phi)
    theta = np.radians(Theta)

    Hp = int(2 * np.tan(phi / 2) * (He / np.pi))
    Wp = int(2 * np.tan(theta / 2) * (We / (2*np.pi)))

    print("入力した画角θ, φ =", Theta, Phi, "より")
    print("計算された出力画像サイズ")
    print("W, H =", Wp, Hp)

    return Hp, Wp
##



##
# 出力画像サイズから画角を求める関数
def angle(Ie, Hp, Wp):
    He, We, _ = Ie.shape

    Theta = 2 * np.arctan2(Wp * np.pi, We)
    Phi = 2 * np.arctan2(Hp * np.pi, (2 * He))

    theta = np.degrees(Theta)
    phi = np.degrees(Phi)

    print("入力した画像サイズW, H =", Wp, Hp, "より，")
    print("計算された画角")
    print("θ, φ", theta, phi)

    return theta, phi
##




def main():
    # パラメータの設定
    Ie = cv2.imread(sys.argv[1])  # 入力画像の読み込み
    
    # 入力の指定
    if "angle" == sys.argv[9]:
        Theta = float(sys.argv[2])    # 水平方向の画角θ
        Phi = float(sys.argv[3])      # 垂直方向の画角φ
        # 出力サイズを求める
        Hp, Wp = size(Ie, Theta, Phi)

    elif "size" == sys.argv[9]:
        Hp = int(sys.argv[4])  # 出力画像Ipの画像サイズ（高さ)
        Wp = int(sys.argv[5])  # 出力画像Ipの画像サイズ（幅)
        # 画角を求める
        Theta, Phi = angle(Ie, Hp, Wp)

    else :
        Theta = float(sys.argv[2])    # 水平方向の画角θ
        Phi = float(sys.argv[3])      # 垂直方向の画角φ
        Hp = int(sys.argv[4])  # 出力画像Ipの画像サイズ（高さ)
        Wp = int(sys.argv[5])  # 出力画像Ipの画像サイズ（幅)


    theta_eye = float(sys.argv[6])  # 水平方向の視線角度
    phi_eye = float(sys.argv[7])    # 垂直方向の視線角度
    psi_eye = float(sys.argv[8])    #光軸回りの回転角度


    # 透視投影画像の生成
    print("全方位画像から透視投影画像を生成しています")
    Ip = perspective_projection(Ie, Theta, Phi, Wp, Hp, theta_eye, phi_eye, psi_eye)

    # 画像の保存，出力
    cv2.imwrite("Viewpoint Perspective Image.jpg", Ip)
    print("透視投影画像が保存されました")


if __name__ == "__main__":
    main()