# ランドマーク検出
## 顔画像を読み込み、MediaPipeを使用して顔のランドマークを検出(json形式で保存)し、描画するスクリプト 


import cv2
import mediapipe as mp
import json
import os

# MediaPipeの初期化
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

# 入力画像のパス（マスクなし画像）
image_path = "" # 画像のパスを指定
image_id = os.path.splitext(os.path.basename(image_path))[0]  # ファイル名からID生成

#("maskless_face.jpg")  # 基準（マスクなし）
#("masked_face.jpg")    # 対象（マスクあり）




# 画像読み込み
image = cv2.imread(image_path)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 顔ランドマーク検出
results = face_mesh.process(rgb_image)

# ランドマーク保存用構造
landmark_data = {}                                                                                                                           

if results.multi_face_landmarks:
    landmarks = results.multi_face_landmarks[0]
    landmark_list = []

    h, w, _ = image.shape  # 画像サイズ取得

    # 描写用の画像をコピー
    image_with_landmarks = image.copy()

    for idx, lm in enumerate(landmarks.landmark):
        cx, cy = int(lm.x * w), int(lm.y * h)
        landmark_list.append({
            "x": lm.x,
            "y": lm.y,
            "z": lm.z
        })
        # ランドマーク点を描画
        cv2.circle(image_with_landmarks, (cx, cy), 1, (0, 255, 0), -1)

    # JSON保存
    landmark_data[image_id] = landmark_list
    with open(f"{image_id}_landmarks.json", "w") as f:# "出力パス" +{image_id}_landmarks.json
        json.dump(landmark_data, f, indent=2)

    # 描写画像の保存
    output_image_path = f"{image_id}_with_landmarks.jpg"# "出力パス" +{image_id}_with_landmarks.jpg
    cv2.imwrite(output_image_path, image_with_landmarks)

    print(f"[✅] ランドマーク保存完了: {image_id}_landmarks.json")# "出力パス" +{image_id}_landmarks.json
    print(f"[🖼️] ランドマーク描写画像: {output_image_path}")# "出力パス" +{image_id}_with_landmarks.jpg

    # 画像表示（任意）
    cv2.imshow("Landmarks", image_with_landmarks)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("[⚠️] 顔が検出されませんでした。")
