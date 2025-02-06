import tensorflow as tf
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# 加载 MobileNetV2 预训练模型（不包括分类头）
# model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False)

# 保存模型
# model.export("mobilenet_v2_001")

converter = tf.lite.TFLiteConverter.from_saved_model("/Users/zhouzhenliang/Desktop/tensorflowlite/model/mobilenet-v1-tensorflow2-025-128-classification-v2")
tflite_model = converter.convert()

# 保存 TFLite 模型
with open("mobilenet-v1-tensorflow2-025-128-classification-v2.tflite", "wb") as f:
    f.write(tflite_model)
print("转换完成！")
