# wonfes-image-crop

`input/` に置いた画像を中央基準で切り抜き、`output/` に 800x600 の JPEG 画像として保存します。

## 使い方

```bash
uv run main.py
```

対応形式: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif`, `.tiff`

処理内容:

1. 画像の EXIF 回転情報を反映
2. 中央を基準に 4:3 でクロップ
3. 800x600 にリサイズ
4. 拡張子を `.jpeg` にして、品質 100 で `output/` に保存
