#!/bin/bash

# 入力画像のパス
INPUT_IMAGE=""

# 垂直方向の画角 (Phi)
PHI=90

# 水平方向の画角 (Theta)
THETA=90

# 出力画像の高さと幅
HP=600
WP=800

# 垂直方向の視線角度
PHI_EYE=0

# 光軸回りの回転角度
PSI_EYE=0

# 出力ディレクトリ
OUTPUT_DIR="" # 出力ディレクトリのパスを指定
mkdir -p "$OUTPUT_DIR"

# 水平方向の視線角度 (theta_eye) を -π から π まで 10度刻みで変化させる
for THETA_EYE in $(seq -180 10 180); do
    echo "生成中: 水平方向の視線角度 θ_eye = $THETA_EYE 度"

    # 実行コマンド
    python3 XXXX "$INPUT_IMAGE" "$THETA" "$PHI" "$HP" "$WP" "$THETA_EYE" "$PHI_EYE" "$PSI_EYE" "size" #XXXにパスを指定

    # 出力画像をリネームして保存 (角度のみのファイル名)
    mv "Viewpoint Perspective Image.jpg" "$OUTPUT_DIR/${THETA_EYE}.jpg"
done

echo "すべての透視投影画像が生成されました。出力ディレクトリ: $OUTPUT_DIR"