import os.path

import tensorflow as tf
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def transform_to_tflite(path):
    converter = tf.lite.TFLiteConverter.from_saved_model(path)
    tflite_model = converter.convert()

    dir_name, file_name = os.path.split(path)
    output_file = os.path.join(dir_name, file_name + '.tflite')
    with open(output_file, 'wb') as f:
        f.write(tflite_model)
    print(f'output_file: {output_file}')


if __name__ == '__main__':
    transform_to_tflite(
        '/Users/zhouzhenliang/Desktop/tensorflowlite/model/mobilenet-v2-tensorflow2-100-224-feature-vector-v2')
