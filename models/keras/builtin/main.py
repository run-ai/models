import os
import sys
import time

import keras
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
import scipy # scipy.misc.imresize() is was removed in scipy-1.3.0

MODEL = 'vgg16'
BATCH_SIZE = 64
IMAGE_SIZE = 32
EPOCHS = 100

if len(sys.argv) > 1:
    MODEL = sys.argv[1]

if len(sys.argv) > 2:
    BATCH_SIZE = int(sys.argv[2])

if len(sys.argv) > 3:
    IMAGE_SIZE = int(sys.argv[3])

if len(sys.argv) > 4:
    EPOCHS = int(sys.argv[4])

print("MODEL=%s" % MODEL)
print("BATCH_SIZE=%d" % BATCH_SIZE)
print("IMAGE_SIZE=%d" % IMAGE_SIZE)
print("EPOCHS=%d" % EPOCHS)

def resize_images(src, shape):
    resized = [scipy.misc.imresize(img, shape, 'bilinear', 'RGB') for img in src]
    return np.stack(resized)

def load_cifar10_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cifar-10')

    num_train_samples = 50000

    x_train = np.empty((num_train_samples, 3, 32, 32), dtype='uint8')
    y_train = np.empty((num_train_samples,), dtype='uint8')

    for i in range(1, 6):
        fpath = os.path.join(path, 'data_batch_' + str(i))
        (x_train[(i - 1) * 10000: i * 10000, :, :, :],
         y_train[(i - 1) * 10000: i * 10000]) = keras.datasets.cifar.load_batch(fpath)

    fpath = os.path.join(path, 'test_batch')
    x_test, y_test = keras.datasets.cifar.load_batch(fpath)

    y_train = np.reshape(y_train, (len(y_train), 1))
    y_test = np.reshape(y_test, (len(y_test), 1))

    if keras.backend.image_data_format() == 'channels_last':
        x_train = x_train.transpose(0, 2, 3, 1)
        x_test = x_test.transpose(0, 2, 3, 1)

    return (x_train, y_train), (x_test, y_test)

def cifar10_data(train_samples, test_samples, num_classes, trg_image_dim_size):
    (x_train, y_train), (x_test, y_test) = load_cifar10_data()
    print('Loaded train samples')

    if os.getenv('RUNAI_USE_ENTIRE_DATASET', '0') == '0':
        x_train = x_train[:train_samples]
        y_train = y_train[:train_samples]

        x_test = x_test[:test_samples]
        y_test = y_test[:test_samples]

    x_train = resize_images(x_train, (trg_image_dim_size, trg_image_dim_size))
    x_test = resize_images(x_test, (trg_image_dim_size, trg_image_dim_size))

    y_train = np.clip(y_train, None, num_classes - 1)
    y_test = np.clip(y_test, None, num_classes - 1)
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    print('Preprocessed train samples')
    print('X train shape: %s' % str(x_train.shape))
    print('Y train shape: %s' % str(y_train.shape))
    print('X test shape: %s' % str(x_test.shape))
    print('Y test shape: %s' % str(y_test.shape))

    return (x_train, y_train), (x_test, y_test)

class StepTimeReporter(keras.callbacks.Callback):
    def on_batch_begin(self, batch, logs={}):
        self.batch_start = time.time()

    def on_batch_end(self, batch, logs={}):
        print(' >> Step %d took %g sec' % (batch, time.time() - self.batch_start))

    def on_epoch_begin(self, epoch, logs=None):
        self.epoch_start = time.time()

    def on_epoch_end(self, epoch, logs=None):
        print(' >> Epoch %d took %g sec' % (epoch, time.time() - self.epoch_start))

def main():
    if 'RUNAI_TF_ALLOW_GROWTH' in os.environ and int(os.environ['RUNAI_TF_ALLOW_GROWTH']) == 1:
        import tensorflow
        config = tensorflow.ConfigProto()
        config.gpu_options.allow_growth = True
        keras.backend.set_session(tensorflow.Session(config=config))
        print("Using TF allow growth")

    models = {
        'xception':             'Xception',
        'vgg16':                'VGG16',
        'vgg19':                'VGG19',
        'inception_v3':         'InceptionV3',
        'inception_resnet_v2':  'InceptionResNetV2',
        'mobilenet':            'MobileNet',
        'densenet':             'DenseNet169',
        'nasnet':               'NASNetLarge',
        'mobilenet_v2':         'MobileNetV2',
        'resnet50':             'ResNet50',
    }

    print("Loading data")
    (x_train, y_train), (x_test, y_test) = cifar10_data(
        train_samples=5000,
        test_samples=1000,
        num_classes=10,
        trg_image_dim_size=IMAGE_SIZE,
    )

    print("Creating model '%s'" % MODEL)
    module = getattr(keras.applications, MODEL)
    func = getattr(module, models[MODEL])
    model = func(
        input_shape=x_train[0].shape,
        include_top=True,
        weights=None,
        input_tensor=None,
        pooling=None,
        classes=10)

    model.compile(loss='categorical_crossentropy',
                    optimizer=keras.optimizers.SGD(lr=1e-3),
                    metrics=['accuracy'])

    print("Training model")
    model.fit(x_train, y_train,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              validation_data=(x_test, y_test),
              shuffle=False,
              verbose=True,
              callbacks=[StepTimeReporter()])

    print("Done")

if __name__ == "__main__":
    main()
