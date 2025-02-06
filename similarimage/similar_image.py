import tensorflow as tf
import numpy as np
from numpy.linalg import norm

# 加载 TFLite 模型
interpreter = tf.lite.Interpreter(model_path="mobilenet_v2.tflite")
interpreter.allocate_tensors()

# 获取输入/输出张量信息
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("输入张量:", input_details)
print("输出张量:", output_details)


def extract_features(image):
    """ 计算图片的特征向量 """
    img = tf.image.resize(image, (224, 224))  # 调整输入尺寸
    img = tf.expand_dims(img, axis=0) / 255.0  # 归一化

    interpreter.set_tensor(input_details[0]['index'], img.numpy().astype(np.float32))
    interpreter.invoke()  # 运行推理
    feature_vector = interpreter.get_tensor(output_details[0]['index'])

    return feature_vector.flatten()


def cosine_similarity(vec1, vec2):
    """ 计算余弦相似度 """
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))


# 加载两张图片
img1 = tf.io.read_file("/Users/zhouzhenliang/Desktop/tensorflowlite/data/image_01.jpg")
img1 = tf.image.decode_jpeg(img1, channels=3)

img2 = tf.io.read_file("/Users/zhouzhenliang/Desktop/tensorflowlite/data/image_02.jpg")
img2 = tf.image.decode_jpeg(img2, channels=3)

# 提取特征向量
feature1 = extract_features(img1)
feature2 = extract_features(img2)

# 计算相似度
# 相似度值接近 1 代表两张图片相似，接近 0 代表不相似。
similarity = cosine_similarity(feature1, feature2)
print("相似度:", similarity)
