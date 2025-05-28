# ツールタイトル
全方位画像から透視投影画像の生成
## 環境
- Ubuntu 22.04.5 LTS
- Python 3.10.12
## 概要
## 使用方法

### オプション一覧
- kadai2
```bash
<入力画像パス>: 入力画像ファイルのパス（例: /home/misa/public/camera/kadai2/input.jpg）。
<Theta>: 水平方向の画角（度単位）。
<Phi>: 垂直方向の画角（度単位）。
<Hp>: 出力画像の高さ（ピクセル単位）。
<Wp>: 出力画像の幅（ピクセル単位）。
<theta_eye>: 水平方向の視線角度（度単位）。
<phi_eye>: 垂直方向の視線角度（度単位）。
<psi_eye>: 光軸回りの回転角度（度単位）。
<mode>: モード指定（angle または size またはその他）。
```

- kadai2-2
```bash
<入力画像パス>: 入力画像ファイルのパス（例: /home/misa/public/camera/kadai2/input.jpg）。
<Theta>: 水平方向の画角（度単位）。
<Phi>: 垂直方向の画角（度単位）。
<Hp>: 出力画像の高さ（ピクセル単位）。
<Wp>: 出力画像の幅（ピクセル単位）。

```

### 実行例
- kadai2
```bash
python3 kadai2.py <入力画像パス> <Theta> <Phi> <Hp> <Wp> <theta_eye> <phi_eye> <psi_eye> <mode>
```
- kadai2-2
```bash
python3 /home/misa/public/camera/kadai2/kadai2-2.py <入力画像パス> <Theta> <Phi> <Hp> <Wp>
```

