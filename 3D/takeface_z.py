# MediaPipeを使用して顔の向きを推定し、Yaw（回転）を検出するコード
# カメラで画像撮影


import cv2
import mediapipe as mp
import numpy as np

save_path = ""# 保存先のパスを指定

#("maskless_face.jpg")  # 基準（マスクなし）
#("masked_face.jpg")    # 対象（マスクあり）
#("hmd_face.jpg")    # 対象（HMDあり）



# 準備
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True) 
cap = cv2.VideoCapture(0)
print("📸 カメラを起動中。スペースキーで撮影、ESCで終了します。")

# カメラ内部パラメータ（仮設定）
w, h = 640, 480
focal_length = 700
camera_matrix = np.array([[focal_length, 0, w/2],
                          [0, focal_length, h/2],
                          [0, 0, 1]])
dist_coeffs = np.zeros((4, 1))  # 歪みなし

# 3Dモデルポイント（顔の基準点、Z=0前提）
model_points = np.array([
    [0.0, 0.0, 0.0],       # 鼻先
    [0.0, -63.6, -12.5],   # 顎
    [-43.3, 32.7, -26.0],  # 左目端
    [43.3, 32.7, -26.0],   # 右目端
    [-28.9, -28.9, -24.1], # 左口端
    [28.9, -28.9, -24.1]   # 右口端
], dtype=np.float32)

# 対応するランドマークインデックス（MediaPipe仕様）
indices = [1, 152, 263, 33, 287, 57]




while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    image_points = []

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        for idx in indices:
            lm = landmarks[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            image_points.append([x, y])
        image_points = np.array(image_points, dtype=np.float32)

        # 姿勢推定
        success, rotation_vec, _ = cv2.solvePnP(model_points, image_points,
                                                camera_matrix, dist_coeffs)
        if success:
            # 回転ベクトルをオイラー角に変換
            rot_mat, _ = cv2.Rodrigues(rotation_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rot_mat)
            yaw = angles[1]  # Y軸（回転＝顔の向き）
           #yaw_deg = yaw * 180 / np.pi
            rounded_yaw = round(yaw / 5) * 5  # 5度単位で丸める

            cv2.putText(frame, f"Angle of Rotation: {rounded_yaw} deg", (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Yaw Detection", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESCキーで終了
        break
    elif key == 32:  # スペースキーで撮影
        cv2.imwrite(save_path, frame)
        print(f"[✅] 撮影・保存しました: {save_path}")
        break

cap.release()
cv2.destroyAllWindows()
