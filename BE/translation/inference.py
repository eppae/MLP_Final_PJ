"""Translate an image to another image
An example of command-line usage is:
python export_graph.py --model models/Hazy_to_Clear.pb \
                       --input_dir input \
                       --output_dir output \
                       --image_size 256
"""

import os
import tensorflow as tf
from absl import app, flags
import utils

FLAGS = flags.FLAGS

flags.DEFINE_string('model', 'models/Hazy_to_Clear.pb', 'model path (.pb)')
flags.DEFINE_string('input_dir', 'input', 'input directory path ')
flags.DEFINE_string('output_dir', 'output', 'output directory path ')
flags.DEFINE_integer('image_size', '256', 'image size, default: 256')


def img_reader(input_dir):
    file_paths = []

    for img_file in os.scandir(input_dir):
        if img_file.name.endswith('.jpg') and img_file.is_file():
            file_paths.append(img_file.path)

    return file_paths


def inference():
    for n, img_path in enumerate(img_reader(FLAGS.input_dir)):
        graph = tf.Graph()
        with graph.as_default():
            with tf.io.gfile.GFile(img_path, 'rb') as f:
                image_data = f.read()
                input_image = tf.image.decode_jpeg(image_data, channels=3)
                input_image = tf.image.resize(input_image, size=(FLAGS.image_size, FLAGS.image_size))
                input_image = utils.convert2float(input_image)
                input_image.set_shape([FLAGS.image_size, FLAGS.image_size, 3])
            with tf.io.gfile.GFile(FLAGS.model, 'rb') as model_file:
                graph_def = tf.compat.v1.GraphDef()
                graph_def.ParseFromString(model_file.read())
                [output_image] = tf.import_graph_def(graph_def,
                                                     input_map={'input_image': input_image},
                                                     return_elements=['output_image:0'],
                                                     name='output')
            with tf.compat.v1.Session(graph=graph):
                generated = output_image.eval()

        with open(FLAGS.output_dir + '/sample_' + img_path.split('\\')[-1], 'wb') as f:
            f.write(generated)


def main(unused_argv):
    inference()


if __name__ == '__main__':
    app.run(main)
