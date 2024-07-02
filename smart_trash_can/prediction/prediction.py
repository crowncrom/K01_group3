# import libraries
import numpy as np
import time
import os
import PIL
import PIL.Image
import tensorflow as tf

batch_size = 2
img_height = 120
img_width = 120

# load dataset
# (x_train, y_train), (x_test, y_test) = cifar10.load_data()
train_ds = tf.keras.utils.image_dataset_from_directory(
  "train",
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
  "test",
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break

normalization_layer = tf.keras.layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
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

model_name="k01_group03_smart-trash-can_"+str(time.time())+".keras"
model.save(model_name)

# load model
from tensorflow.keras.models import load_model
stc_model = load_model(model_name)

img = PIL.Image.open("./gomi2/IMG_4295.jpg")
img = img.resize((120, 120))

# prediction
vec = np.array(img)
vec = vec.astype('float32') /255
vec = vec.reshape(1, 120, 120, 3)
result = stc_model.predict(vec)
print("Prediction result = ", result)
print("Prediction Lavel = ", class_names[np.argmax(result[0])])
