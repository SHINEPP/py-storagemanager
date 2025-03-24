import os

import rembg
from PIL import Image, ImageFilter


def process_photo(in_path, out_path, size=(358, 441), min_kb=10, max_kb=80):
    input_img = Image.open(in_path)
    rembg_img = rembg.remove(input_img)

    resize_img = rembg_img.resize(size)
    if resize_img.mode == 'RGBA':
        result_img = Image.new("RGB", size, (255, 255, 255))  # 纯白背景
        result_img.paste(resize_img, (0, 0), resize_img)
    else:
        result_img = resize_img.convert("RGB")

    result_img = result_img.filter(ImageFilter.GaussianBlur(0.1))

    # 调整质量以满足 10 KB ~ 80 KB
    quality = 95
    while True:
        result_img.save(out_path, "JPEG", quality=quality)
        file_size = os.path.getsize(out_path) / 1024

        if min_kb <= file_size <= max_kb:
            print(f"✅处理成功！最终文件大小: {file_size:.2f} KB")
            break
        elif file_size > max_kb:
            quality -= 5  # 过大，降低质量
        elif file_size < min_kb:
            quality += 5  # 过小，提高质量
        if quality < 10:  # 避免质量过低
            print("⚠️无法满足大小要求，请尝试其他图片")
            break


if __name__ == '__main__':
    process_photo('data/xlb.jpg', 'data/xlb_out.jpg', size=(358, 441), min_kb=10, max_kb=80)
