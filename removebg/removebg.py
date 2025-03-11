import rembg
from PIL import Image

# 
# u2net: 通用预训练模型
# u2netp: u2net的轻量版
# u2net_human_seg: 预训练的人物分割模型
# u2net_cloth_seg: 预训练的衣服的分割模型，会分割 上半身，下半身和全身
# silueta: 和 u2net 模型一样只不过大小只有 43MB
# isnet-general-use: 预训练的通用模型
# isnet-anime: 动漫角色的高精度分割模型
# sam: 预训练的通用模型
# 

if __name__ == '__main__':
    # 加载图片
    image = Image.open('data/1141720496954.jpg')
    # 创建一个Rembg对象
    rembg_obj = rembg.remove(image)
    # 显示去除背景后的图片
    # rembg_obj.show()
    rembg_obj.save('data/1141720496954_out.png')
