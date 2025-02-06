import os
import shutil

import numpy as np
import tensorflow as tf
from numpy.linalg import norm


class ImageFeatures:

    def __init__(self):
        # 加载 TFLite 模型
        self.interpreter = tf.lite.Interpreter(model_path="mobilenet-v3-tensorflow2-large-075-224-classification-v1.tflite")
        self.interpreter.allocate_tensors()

        # 获取输入/输出张量信息
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        print("输入张量:", self.input_details)
        print("输出张量:", self.output_details)

    def extract_features(self, image_path):
        """ 计算图片的特征向量 """
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)

        img = tf.image.resize(img, (224, 224))  # 调整输入尺寸
        img = tf.expand_dims(img, axis=0) / 255.0  # 归一化

        self.interpreter.set_tensor(self.input_details[0]['index'], img.numpy().astype(np.float32))
        self.interpreter.invoke()  # 运行推理
        feature_vector = self.interpreter.get_tensor(self.output_details[0]['index'])

        return feature_vector.flatten()


def cosine_similarity(vec1, vec2):
    """ 计算余弦相似度 """
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def main_test():
    features = ImageFeatures()
    results = []

    img_dir = '/Users/zhouzhenliang/Desktop/tensorflowlite/Image'
    img_out_dir = '/Users/zhouzhenliang/Desktop/tensorflowlite/Image_out'
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            path = os.path.join(root, file)
            values = features.extract_features(path)
            results.append({'path': path, 'features': values})

    if os.path.exists(img_out_dir):
        shutil.rmtree(img_out_dir)

    count = len(results)
    for i in range(count):
        for j in range(i + 1, count):
            path1 = results[i]['path']
            path2 = results[j]['path']
            name1 = os.path.split(path1)[-1]
            name2 = os.path.split(path2)[-1]
            features1 = results[i]['features']
            features2 = results[j]['features']
            similarity = cosine_similarity(features1, features2)
            print(f'{i} - {j}, 相似度: {similarity}, {name1} - {name2}')
            if similarity > 0.7:
                out_dir = os.path.join(img_out_dir, f'V{similarity}')
                os.makedirs(out_dir, exist_ok=True)
                shutil.copyfile(path1, os.path.join(out_dir, name1))
                shutil.copyfile(path2, os.path.join(out_dir, name2))


if __name__ == '__main__':
    main_test()
