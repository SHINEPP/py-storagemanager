import tensorflow as tf

# 加载 MobileNetV2 预训练模型（不包括分类头）
model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False)

# 保存模型
model.save("mobilenet_v2")
