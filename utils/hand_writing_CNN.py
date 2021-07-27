import tensorflow as tf
from tensorflow import keras
import os

# If the file of the model already exists, we loaded as model
if 'hand_writing_model_CNN.h5' in os.listdir():
    model = keras.models.load_model('hand_writing_model_CNN.h5')

# Otherwise, we create the model
else:
    import numpy as np
    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten


    # Images are 28 by 28 pixels
    img_rows = img_cols = 28
    num_classes = 10

    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    # We reshape the images and divided them by 255, in order to get a value from 0 to 1
    train_images = train_images.reshape(train_images.shape[0], img_rows, img_cols, 1)
    train_images = train_images.astype('float32')
    train_images /= 255

    test_images = test_images.reshape(test_images.shape[0], img_rows, img_cols, 1)
    test_images = test_images.astype('float32')
    test_images /= 255

    input_shape = (img_rows, img_cols, 1)

    # We use One-Hot encoding for the labels
    train_labels = keras.utils.to_categorical(train_labels, num_classes)
    test_labels = keras.utils.to_categorical(test_labels, num_classes)
    
    model = Sequential()
    model.add(Conv2D(filters = 64, kernel_size = (3, 3), activation = 'relu', input_shape = input_shape))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(rate = .4))
    model.add(Conv2D(filters = 32, kernel_size = (3, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(rate = .4))
    model.add(Flatten())
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(10, activation = 'softmax'))
    
    model.summary()
    
    model.compile(
        optimizer = 'adam',
        loss = 'categorical_crossentropy',
        metrics = ['accuracy']
    )
    
    model.fit(
        train_images,
        train_labels,
        epochs = 10,
        batch_size = 64,
        shuffle = True
    )
    
    test_loss, test_acc = model.evaluate(
        test_images,
        test_labels,
        verbose = 2
    )

    print('Total accuracy: ', test_acc)
    print('Total loss: ', test_loss)

    model.save('hand_writing_model_CNN.h5')