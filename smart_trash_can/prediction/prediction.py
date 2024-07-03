# import libraries
import numpy as np
import time
import os
import PIL
import PIL.Image
import tensorflow as tf
from tensorflow.keras.models import load_model

class Prediction:
    def __init__(self, config):
        self.model_name = config["modelName"]
        self.batch_size = config["batchSize"]
        self.img_height = config["imageHeight"]
        self.img_width = config["imageWidth"]
        self.class_names = ["burnable", "plastic"]
        print("Prediction initialized")

    def learning(self):
        train_ds = tf.keras.utils.image_dataset_from_directory(
          "train",
          validation_split=0.2,
          subset="training",
          seed=123,
          image_size=(self.img_height, self.img_width),
          batch_size=self.batch_size)

        val_ds = tf.keras.utils.image_dataset_from_directory(
          "test",
          validation_split=0.2,
          subset="validation",
          seed=123,
          image_size=(self.img_height, self.img_width),
          batch_size=self.batch_size)

        self.class_names = train_ds.class_names
        print(self.class_names)

        for image_batch, labels_batch in train_ds:
          print(image_batch.shape)
          print(labels_batch.shape)
          break

        normalization_layer = tf.keras.layers.Rescaling(1./255)

        normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        image_batch, labels_batch = next(iter(normalized_ds))
        first_image = image_batch[0]
        print(np.min(first_image), np.max(first_image))
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        num_classes = 2
        model = tf.keras.Sequential([
          tf.keras.layers.Rescaling(1./255),
          tf.keras.layers.Conv2D(32, 3, activation='relu'),
          tf.keras.layers.MaxPooling2D(),
          tf.keras.layers.Conv2D(32, 3, activation='relu'),
          tf.keras.layers.MaxPooling2D(),
          tf.keras.layers.Conv2D(32, 3, activation='relu'),
          tf.keras.layers.MaxPooling2D(),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(128, activation='relu'),
          tf.keras.layers.Dense(num_classes)
        ])

        model.compile(
          optimizer='adam',
          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
          metrics=['accuracy'])

        history = model.fit(
          train_ds,
          validation_data=val_ds,
          epochs=5
        )

        model.summary()

        self.model_name = "k01_group03_smart-trash-can_"+str(time.time())+".keras"
        model.save(self.model_name)

    def load(self):
        self.stc_model = load_model(self.model_name)

    def prediction(self, img_path):
        img = PIL.Image.open(img_path)
        img = img.resize((120, 120))
        vec = np.array(img)
        vec = vec.astype('float32') /255
        vec = vec.reshape(1, 120, 120, 3)
        result = self.stc_model.predict(vec)
        print("Prediction result = ", result)
        print("Prediction Label = ", self.class_names[np.argmax(result)])
        return np.argmax(result)
