# Lint as: python2, python3
# Copyright 2018 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Converts chopped glom data to TFRecord file format"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import os
import sys
import build_data
from six.moves import range
import tensorflow as tf




FLAGS = tf.app.flags.FLAGS

_NUM_SHARDS = 4


def _convert_dataset(dataset_split, image_data_filename,output_dir):
    """Converts the dataset into tfrecord format.

    Args:
      dataset_split: Dataset split (e.g., train, val).
      image_data_filename: List of tuples, each containing the filename, image, and label as BytesIO objects.
    """

    num_images = len(image_data_filename)
    num_per_shard = int(math.ceil(num_images / _NUM_SHARDS))

    image_reader = build_data.ImageReader('jpeg', channels=3)
    label_reader = build_data.ImageReader('png', channels=1)
    for shard_id in range(_NUM_SHARDS):
        output_filename = os.path.join(
            output_dir,
            '%s-%05d-of-%05d.tfrecord' % (dataset_split, shard_id, _NUM_SHARDS))
        with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
            start_idx = shard_id * num_per_shard
            end_idx = min((shard_id + 1) * num_per_shard, num_images)
            for i in range(start_idx, end_idx):
                sys.stdout.write('\r>> Converting image %d/%d shard %d' % (
                    i + 1, num_images, shard_id))
                sys.stdout.flush()
                # Get image and label data from image_data_filename
                filename, buffer_crop_imgPAS, buffer_Glommask2 = image_data_filename[i]

                # Read the image data from the BytesIO object
                buffer_crop_imgPAS.seek(0)  # Reset buffer position
                image_data = buffer_crop_imgPAS.read()
                height, width = image_reader.read_image_dims(image_data)

                # Read the label data from the BytesIO object
                buffer_Glommask2.seek(0)  # Reset buffer position
                seg_data = buffer_Glommask2.read()
                seg_height, seg_width = label_reader.read_image_dims(seg_data)

                if height != seg_height or width != seg_width:
                    raise RuntimeError('Shape mismatched between image and label.')

                # Convert to tf example
                example = build_data.image_seg_to_tfexample(
                    image_data, filename, height, width, seg_data)
                tfrecord_writer.write(example.SerializeToString())
    sys.stdout.write('\n')
    sys.stdout.flush()
