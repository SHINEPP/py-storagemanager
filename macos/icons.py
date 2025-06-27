import os.path

from PIL import Image


def scale_and_pad_image(input_path, output_path, scale_factor=0.8):
    # 打开原始图片（保持透明通道）
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size

    # 缩放尺寸
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # 缩小图片
    img_scaled = img.resize((new_width, new_height), resample=Image.LANCZOS)

    # 创建新的透明画布（原尺寸）
    new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # 计算把缩小图居中
    x = (width - new_width) // 2
    y = (height - new_height) // 2

    # 粘贴缩小后的图
    new_img.paste(img_scaled, (x, y))

    # 保存
    new_img.save(output_path)
    print(f"保存成功: {output_path}")


# 使用方法
dir_root = '/Users/zhouzhenliang/Desktop/oss_app/macos-py'
dir_root_out = '/Users/zhouzhenliang/source/shine/flutter-oss-browser/macos/Runner/Assets.xcassets/AppIcon.appiconset'
icons = ['1024x1024.png', '512x512 1.png', '512x512.png', '256x256 1.png', '256x256.png', '128x128.png', '32x32.png', '64x64.png', '32x32 1.png', '16x16.png']
for icon in icons:
    scale_and_pad_image(os.path.join(dir_root, icon), os.path.join(dir_root_out, icon))
