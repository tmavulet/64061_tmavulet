# -*- coding: utf-8 -*-
"""Assignment 2 - Convolution - Tejasvini Mavuleti.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cpkku4qn-9XkTNvf5XcX6MObrImPp_D7

**MIS 64061 - Assignment 02 - Convolution** Tejasvini Mavuleti 11/06/2022

In this assignment we apply convolution networks also known as convents to image data to identify the difference between cats and dogs. 

**Summary**

For this assignment we assign weights and baises to algorithms and apply labels to clearly classsify the images as distinct and accurate as possible. We need to test the model on the unseen test data to check the accurarcy of the model classification. We compare the network predicition for every image out of the 1000 samples in batches and test the prediction capabilities of the network if it increases and the distance must be minimized.
"""

#Install kaggle
!pip install -q kaggle

from google.colab import files
files.upload()

from tensorflow import keras
from tensorflow.keras import layers
inputs = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(inputs)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(10, activation="softmax")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.summary()

from tensorflow.keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype("float32") / 255
test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype("float32") / 255
model.compile(optimizer="rmsprop",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"])
model.fit(train_images, train_labels, epochs=5, batch_size=64)

"""Model Building"""

test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Test accuracy: {test_acc:.3f}")

"""We now train the convnet on the dataset to test the accuracy of the model and if it is classfying the images efficiently.

**Using the maxpooling technique**

Note - we can identify the incorrectly structed convnet in this technique
"""

inputs = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(inputs)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(10, activation="softmax")(x)
model_no_max_pool = keras.Model(inputs=inputs, outputs=outputs)

model_no_max_pool.summary()

# Training the convnet from scratch

!kaggle competitions download -c dogs-vs-cats

!unzip -qq train.zip
!unzip -qq test1.zip

"""Now we are done with the downloading our data.

**Q1**.  Use any technique to reduce 
overfitting and improve performance in developing a network that you train from scratch. What 
performance did you achieve?**

Using the images of dogs and cats for making training, validation, and test directories
"""

import os, shutil, pathlib

original_dir = pathlib.Path("train")
new_base_dir = pathlib.Path("cats_vs_dogs_small")

def make_subset(subset_name, start_index, end_index):
    for category in ("cat", "dog"):
        dir = new_base_dir / subset_name / category
        os.makedirs(dir)
        fnames = [f"{category}.{i}.jpg" for i in range(start_index, end_index)]
        for fname in fnames:
            shutil.copyfile(src=original_dir / fname,
                            dst=dir / fname)

make_subset("train", start_index=0, end_index=1000)
make_subset("validation", start_index=1000, end_index=1500)
make_subset("test", start_index=1500, end_index=2000)

"""Using a small convnet for the dogs vs cats classification"""

from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(180, 180, 3))
x = layers.Rescaling(1./255)(inputs)
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.summary()

"""In this step, we have a model with just 4 conv2D layers and 4 maxpooling layers. Even though it is not a big model, we have 991,041 parameters to work with.
We go on to calculate overfitting and use some of the techniques to properly classify these images into their categories.

**Training the model**
"""

model.compile(loss="binary_crossentropy",
              optimizer="rmsprop",
              metrics=["accuracy"])

"""**Preprocessing the data**

Creating an image dataset from the image directory to read the images
"""

from tensorflow.keras.utils import image_dataset_from_directory

train_dataset = image_dataset_from_directory(
    new_base_dir / "train",
    image_size=(180, 180),
    batch_size=32)
validation_dataset = image_dataset_from_directory(
    new_base_dir / "validation",
    image_size=(180, 180),
    batch_size=32)
test_dataset = image_dataset_from_directory(
    new_base_dir / "test",
    image_size=(180, 180),
    batch_size=32)

import numpy as np
import tensorflow as tf
random_numbers = np.random.normal(size=(1000, 16))
dataset = tf.data.Dataset.from_tensor_slices(random_numbers)

for i, element in enumerate(dataset):
    print(element.shape)
    if i >= 2:
        break

batched_dataset = dataset.batch(32)
for i, element in enumerate(batched_dataset):
    print(element.shape)
    if i >= 2:
        break

reshaped_dataset = dataset.map(lambda x: tf.reshape(x, (4, 4)))
for i, element in enumerate(reshaped_dataset):
    print(element.shape)
    if i >= 2:
        break

"""
**Identifying the shapes and labels of the dataset**"""

for data_batch, labels_batch in train_dataset:
    print("data batch shape:", data_batch.shape)
    print("labels batch shape:", labels_batch.shape)
    break

"""
**Model fitting**
"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="convnet_from_scratch.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=30,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""
**Plotting the loss and accuracy of the classification while training**"""

import matplotlib.pyplot as plt
accuracy = history.history["accuracy"]
val_accuracy = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(1, len(accuracy) + 1)
plt.plot(epochs, accuracy, "bo", label="Training accuracy")
plt.plot(epochs, val_accuracy, "b", label="Validation accuracy")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs, loss, "bo", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""**Evaluating the model on the test set**"""

test_model = keras.models.load_model("convnet_from_scratch.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""**Answer 1)**

In this model, the model performed well on the training set until it started to overfit. We can also see that the validation accuracy ans test accuracy did not improve. We can try to imporve our model and reduce overfitting using data augmentation and regularization.

**STEP 1 - DATA AUGMNENTATION**

With the technique of data augmentation, we can work on a condition know as spatial invariance. This means that the object of either the cat or a dog will be same irrespective of it's spatial location. For instance the dog number 1 will be the same whether that number appears in the top left corner, center or bottom right corner. We could do it in multiple ways, like to flip, rotate, scale, crop, translate and moving image along x and y axis and also distorting high-frequesncy by adding some noise to them. Here, I am only using flipping, rotation and zooming.
"""

from google.colab import drive
drive.mount('/content/drive')

"""
**Adding an image model**"""

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.2),
    ]
)

"""**Displaying some randomly augmented training images**"""

plt.figure(figsize=(10, 10))
for images, _ in train_dataset.take(1):
    for i in range(9):
        augmented_images = data_augmentation(images)
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(augmented_images[0].numpy().astype("uint8"))
        plt.axis("off")

"""This is how we can change the orientation and display of one particular image.

**Defining a new convnet that includes image augmentation and dropout**
"""

inputs = keras.Input(shape=(180, 180, 3))
x = data_augmentation(inputs)
x = layers.Rescaling(1./255)(x)
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(loss="binary_crossentropy",
              optimizer="rmsprop",
              metrics=["accuracy"])

"""**Training the regularized convnet**"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="convnet_from_scratch_with_augmentation.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=50,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""Now we use the droupout function and the data augmentation together to use
2 out of 3 techniques for reducing over fitting. Dropout is nothing but ignoring or dropping out some of the layers from the model. We basicaly turn off some of the layers during our training. 

**Note**: We are only using dropout for training set, not for the validation and test set. This gives the effect of making a layer look-like and be treated-like a layer with different number of nodes and connectivity to the layers before in the model.

**STEP 2 - DROP OUT**

**Evaluating the model on the test set**
"""

test_model = keras.models.load_model(
    "convnet_from_scratch_with_augmentation.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""In this case, the test accuracy has increased by using dropout and data augmentation.

**Q2**. Increase your training sample size. Keep the validation and test 
samples the same as above. Optimize your network (again training from scratch). What performance did you achieve?**

Using the images of dogs and cats for making training, validation, and test directories
"""

import os, shutil, pathlib

original_dir_2 = pathlib.Path("train")
new_base_dir_2 = pathlib.Path("cats_vs_dogs_small")

def make_subset(subset_name, start_index, end_index):
    for category in ("cat", "dog"):
        dir = new_base_dir / subset_name / category
        os.makedirs(dir)
        fnames = [f"{category}.{i}.jpg" for i in range(start_index, end_index)]
        for fname in fnames:
            shutil.copyfile(src=original_dir / fname,
                            dst=dir / fname)

make_subset("train_2", start_index=0, end_index=2000)
make_subset("validation_2", start_index=2000, end_index=2500)
make_subset("test_2", start_index=2500, end_index=3000)

"""Let's increase our training sampe size to 2000, keeping validation and test same as before.

Model Building

Using a small convnet for the dogs vs cats classification
"""

from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(180, 180, 3))
x = layers.Rescaling(1./255)(inputs)
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.summary()

"""**Training the model**"""

model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

"""**Preprocessing the data**

Creating an image dataset from the image directory to read the images
"""

from tensorflow.keras.utils import image_dataset_from_directory

train_dataset = image_dataset_from_directory(
    new_base_dir / "train_2",
    image_size=(180, 180),
    batch_size=32)
validation_dataset = image_dataset_from_directory(
    new_base_dir / "validation_2",
    image_size=(180, 180),
    batch_size=32)
test_dataset = image_dataset_from_directory(
    new_base_dir / "test_2",
    image_size=(180, 180),
    batch_size=32)

import numpy as np
import tensorflow as tf
random_numbers = np.random.normal(size=(1000, 16))
dataset = tf.data.Dataset.from_tensor_slices(random_numbers)

for i, element in enumerate(dataset):
    print(element.shape)
    if i >= 2:
        break

batched_dataset = dataset.batch(32)
for i, element in enumerate(batched_dataset):
    print(element.shape)
    if i >= 2:
        break

reshaped_dataset = dataset.map(lambda x: tf.reshape(x, (4, 4)))
for i, element in enumerate(reshaped_dataset):
    print(element.shape)
    if i >= 2:
        break

"""
**Identifying the shapes and labels of the dataset**"""

for data_batch, labels_batch in train_dataset:
    print("data batch shape:", data_batch.shape)
    print("labels batch shape:", labels_batch.shape)
    break

"""
**Model fitting**
"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="convnet_from_scratch_updated_train_size.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=30,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""
**Plotting the loss and accuracy of the classification while training**"""

import matplotlib.pyplot as plt
accuracy = history.history["accuracy"]
val_accuracy = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(1, len(accuracy) + 1)
plt.plot(epochs, accuracy, "bo", label="Training accuracy")
plt.plot(epochs, val_accuracy, "b", label="Validation accuracy")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs, loss, "bo", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""**Evaluating the model on the test set**"""

test_model = keras.models.load_model("convnet_from_scratch_updated_train_size.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""We were able to achieve the accuracy of 100% for the training set.But the model didn't perfromed that well for validation and test set, so we will use data augmentation and dropout to optimize this network and then look at the acuracies again to see their performance.

**STEP 3 - Using data augmentation and drop out AGAIN**

**Adding an image model**
"""

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.2),
    ]
)

"""**Displaying some randomly augmented training images**"""

plt.figure(figsize=(10, 10))
for images, _ in train_dataset.take(1):
    for i in range(9):
        augmented_images = data_augmentation(images)
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(augmented_images[0].numpy().astype("uint8"))
        plt.axis("off")

"""Here we are showing a sample of 9 images that have been flipped, zoomed and rotated.

**Defining a new convnet that includes image augmentation and dropout**
"""

inputs = keras.Input(shape=(180, 180, 3))
x = data_augmentation(inputs)
x = layers.Rescaling(1./255)(x)
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

"""**Training the regularized convnet**"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="convnet_from_scratch_updated_train_size_with_augmentation.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=25,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""**ANSWER 2)** The is a significant growth in the accuracy. Also, the model is converging at a realy good rate not to fast or slow and the ame is with the rates of train and validation.

**Evaluating the model on the test set**
"""

test_model = keras.models.load_model(
    "convnet_from_scratch_updated_train_size_with_augmentation.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""Another big improvement that we can see is in the testing accuracy.

**Q3.** Now change your training sample so that you achieve better performance than those from Steps 
1 and 2.  The 
objective is to find the ideal training sample size to get best prediction results.

Using the images of dogs and cats for making training, validation, and test directories
"""

import os, shutil, pathlib

original_dir_3 = pathlib.Path("train")
new_base_dir_3 = pathlib.Path("cats_vs_dogs_small")

def make_subset(subset_name, start_index, end_index):
    for category in ("cat", "dog"):
        dir = new_base_dir / subset_name / category
        os.makedirs(dir)
        fnames = [f"{category}.{i}.jpg" for i in range(start_index, end_index)]
        for fname in fnames:
            shutil.copyfile(src=original_dir / fname,
                            dst=dir / fname)

make_subset("train_3", start_index=0, end_index=2500)
make_subset("validation_3", start_index=2500, end_index=3000)
make_subset("test_3", start_index=3000, end_index=3500)

"""Model Building

Using a small convnet for the dogs vs cats classification
"""

from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(180, 180, 3))
x = layers.Rescaling(1./255)(inputs)
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.summary()

"""
**Training the model **"""

model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

"""**Preprocessing the data**

Creating an image dataset from the image directory to read the images
"""

from tensorflow.keras.utils import image_dataset_from_directory

train_dataset = image_dataset_from_directory(
    new_base_dir / "train_3",
    image_size=(180, 180),
    batch_size=32)
validation_dataset = image_dataset_from_directory(
    new_base_dir / "validation_3",
    image_size=(180, 180),
    batch_size=32)
test_dataset = image_dataset_from_directory(
    new_base_dir / "test_3",
    image_size=(180, 180),
    batch_size=32)

import numpy as np
import tensorflow as tf
random_numbers = np.random.normal(size=(1000, 16))
dataset = tf.data.Dataset.from_tensor_slices(random_numbers)

for i, element in enumerate(dataset):
    print(element.shape)
    if i >= 2:
        break

batched_dataset = dataset.batch(32)
for i, element in enumerate(batched_dataset):
    print(element.shape)
    if i >= 2:
        break

reshaped_dataset = dataset.map(lambda x: tf.reshape(x, (4, 4)))
for i, element in enumerate(reshaped_dataset):
    print(element.shape)
    if i >= 2:
        break

"""
**Identifying the shapes and labels of the dataset**"""

for data_batch, labels_batch in train_dataset:
    print("data batch shape:", data_batch.shape)
    print("labels batch shape:", labels_batch.shape)
    break

"""
**Model fitting**
"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="convnet_from_scratch_final.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=30,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""
**Plotting the loss and accuracy of the classification while training**"""

import matplotlib.pyplot as plt
accuracy = history.history["accuracy"]
val_accuracy = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(1, len(accuracy) + 1)
plt.plot(epochs, accuracy, "bo", label="Training accuracy")
plt.plot(epochs, val_accuracy, "b", label="Validation accuracy")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs, loss, "bo", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""**Evaluating the model on the test set**"""

test_model = keras.models.load_model("convnet_from_scratch_final.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""**STEP 4 - Using data augmentation and drop out AGAIN**

**Adding an image model**
"""

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.2),
    ]
)

"""**Displaying some randomly augmented training images**"""

plt.figure(figsize=(10, 10))
for images, _ in train_dataset.take(1):
    for i in range(9):
        augmented_images = data_augmentation(images)
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(augmented_images[0].numpy().astype("uint8"))
        plt.axis("off")

"""Again we see how we can change the orientation and display of one particular image.

**Defining a new convnet that includes image augmentation and dropout**
"""

inputs = keras.Input(shape=(180, 180, 3))
x = data_augmentation(inputs)
x = layers.Rescaling(1./255)(x)
x = layers.Conv2D(filters=32, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=64, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=128, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.MaxPooling2D(pool_size=2)(x)
x = layers.Conv2D(filters=256, kernel_size=3, activation="relu")(x)
x = layers.Flatten()(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

"""**Training the regularized convnet**"""

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="convnet_from_scratch_final_with_augmentation.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=35,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""**ANSWER 3)** We have a well trained optimized model at this point. This is because that the training and validation accuracy is moving at similar pace and by increasing the number of epochs we can converge the model.

**Evaluating the model on the test set**
"""

test_model = keras.models.load_model(
    "convnet_from_scratch_final_with_augmentation.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""**Q4**. Repeat Steps 1-3, but now using a pretrained network. The sample sizes you use in Steps 2 and 3 
for the pretrained network may be the same or different from those using the network where 
you trained from scratch. Again, use any and all optimization techniques to get best 
performance.**

**STEP 5 - Pretrained network model**

**Using the VGG16 convolutional base**
"""

conv_base = keras.applications.vgg16.VGG16(
    weights="imagenet",
    include_top=False,
    input_shape=(180, 180, 3))

conv_base.summary()

"""This is an extremely big model because it has around 14 million parameters in it.

**Using feature extraction without data augmentation**
"""

import numpy as np

def get_features_and_labels(dataset):
    all_features = []
    all_labels = []
    for images, labels in dataset:
        preprocessed_images = keras.applications.vgg16.preprocess_input(images)
        features = conv_base.predict(preprocessed_images)
        all_features.append(features)
        all_labels.append(labels)
    return np.concatenate(all_features), np.concatenate(all_labels)

train_features, train_labels =  get_features_and_labels(train_dataset)
val_features, val_labels =  get_features_and_labels(validation_dataset)
test_features, test_labels =  get_features_and_labels(test_dataset)

train_features.shape

"""**Defining and training the densely connected classifiers**"""

inputs = keras.Input(shape=(5, 5, 512))
x = layers.Flatten()(inputs)
x = layers.Dense(256)(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs, outputs)
model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

callbacks = [
    keras.callbacks.ModelCheckpoint(
      filepath="feature_extraction.keras",
      save_best_only=True,
      monitor="val_loss")
]
history = model.fit(
    train_features, train_labels,
    epochs=20,
    validation_data=(val_features, val_labels),
    callbacks=callbacks)

"""
**Plotting the loss and accuracy of the classification**"""

import matplotlib.pyplot as plt
acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, "bo", label="Training accuracy")
plt.plot(epochs, val_acc, "b", label="Validation accuracy")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs, loss, "bo", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()

"""Now, the training and validation accuracy is moving at a similar pace and just by running for 20 epochs, we were able to get the accuracy of 98% which is much better than before.

**Using feature extraction with data augmentation**
"""

conv_base  = keras.applications.vgg16.VGG16(
    weights="imagenet",
    include_top=False)
conv_base.trainable = False

"""
**Assigning weights to the model**"""

conv_base.trainable = True
print("This is the number of trainable weights "
      "before freezing the conv base:", len(conv_base.trainable_weights))

conv_base.trainable = False
print("This is the number of trainable weights "
      "after freezing the conv base:", len(conv_base.trainable_weights))

"""**Adding a data augmentation stage and a classifier to the convolutional base**"""

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.2),
    ]
)

inputs = keras.Input(shape=(180, 180, 3))
x = data_augmentation(inputs)
x = keras.applications.vgg16.preprocess_input(x)
x = conv_base(x)
x = layers.Flatten()(x)
x = layers.Dense(256)(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs, outputs)
model.compile(loss="binary_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="feature_extraction_with_data_augmentation.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=10,
    validation_data=validation_dataset,
    callbacks=callbacks)

"""**Evaluating the model on the test set**"""

test_model = keras.models.load_model(
    "feature_extraction_with_data_augmentation.keras")
test_loss, test_acc = test_model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""The outcome of this technique failed!
Data augmentation was unavle to improve the model performance. There is one last try we could use - fine tuning. We could fine tune all the layers except the last 4 and try check the accuracy of the model.

**STEP 6 - FINE TUNING A PRETRAINED MODEL**
"""

conv_base.summary()

"""**Freezing all layers until the fourth from the last**"""

conv_base.trainable = True
for layer in conv_base.layers[:-4]:
    layer.trainable = False

"""We need to keep in mind that we are freezing all the layers except for the first 2 layers because they are convolution base. Convolution base are the nodes. The second part to this is the Classifier, which sits on the top of the convolution base. This could play the trick of deciding the accuracy of the entire model as a whole.

**Fine-tuning the model**
"""

model.compile(loss="binary_crossentropy",
              optimizer=keras.optimizers.RMSprop(learning_rate=1e-5),
              metrics=["accuracy"])

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath="fine_tuning.keras",
        save_best_only=True,
        monitor="val_loss")
]
history = model.fit(
    train_dataset,
    epochs=10,
    validation_data=validation_dataset,
    callbacks=callbacks)

model = keras.models.load_model("fine_tuning.keras")
test_loss, test_acc = model.evaluate(test_dataset)
print(f"Test accuracy: {test_acc:.3f}")

"""**ANSWER 4)** We could see that we were able to push our model to gain more accuracy by freezing some of the layers and retraining it on our dataset.

**Conclusion**

**Sample selection and sizes**

After training and testing the dogs vs cats dataset I think that the choice of the network and the way to build your model is very important. In this assignment, I saw the significance if different methods to reduce overfitting and exactly how they classify images.

While working with training samples, I saw that it played a cruical role when we worked from scratch. A large enough training sample helps your model to converge better by picking up the signals. However, we might not need this in a pretrained model. When it comes to the pretrained model, we already have the weights for that model. 

**Importance of layers**

All we need to do is run our data through it and get the desired result. But, there is a way to improve this as well. We can freeze some it's layers and train the model again with our data so that it can perform well on our data. The most important thing that I learnt was about layers. After we assigned weights we had the weights of those layers intact. This saves us alot of time and computational power. 

If we were to train a similar model from the scratch, it would take alot of time, computational power and there is a good chance that it might not even converge for us. So by freezing some layers helps us skip that trouble entirely. Now we can train the last few layers of the model as this will enable the model to grasp that special signals that might only be unique to our dataset. This will ultimately give us a model that works perfectly well for us on unseen data and we can even improve it later on by the above mentioned method.


**Findings**

1) In this step I used Data Augmentation where we have a model with just 4 conv2D layers and 4 maxpooling layers. Even though it is not a big model, we have 991,041 parameters to work with. We went on to calculate overfitting and use some of the techniques to properly classify these images into their categories. In this step we also saw that the model performed well on the training set until it started to overfit. We can also see that the validation accuracy ans test accuracy did not improve. We can try to imporve our model and reduce overfitting using data augmentation and regularization.

Result - loss: 0.5825 - accuracy: 0.6870
Test accuracy: 0.687

2) When I used the Dropout Model we were able to achieve the accuracy of 100% for the training set.But the model didn't perfromed that well for validation and test set, so we will use data augmentation and dropout to optimize this network and then look at the acuracies again to see their performance. The is a significant growth in the accuracy. Also, the model is converging at a realy good rate not to fast or slow and the ame is with the rates of train and validation.

Result - loss: 0.5989 - accuracy: 0.7230
Test accuracy: 0.723

3) At this point I re-ran the same methods and we had a well trained optimized model at this point. This is because that the training and validation accuracy is moving at similar pace and by increasing the number of epochs we can converge the model.

Result - loss: 0.4747 - accuracy: 0.7770
Test accuracy: 0.777

4) Now, the last step was to use Fine Tunining to see the training and validation accuracy which moved at a similar pace and just by running for 20 epochs, we were able to get the accuracy of 98% which is much better than before. The outcome of this technique failed! Data augmentation was unavle to improve the model performance. There is one last try we could use - fine tuning. We could fine tune all the layers except the last 4 and try check the accuracy of the model.We could see that we were able to push our model to gain more accuracy by freezing some of the layers and retraining it on our dataset.

Result - loss: 0.2441 - accuracy: 0.9850
Test accuracy: 0.985

I think according to this assignment, fine tuning worked the best. I also gave a thought about using only regularization (with and without dropout), but then chose to expand and see if there could be any significant difference in terms of minimizing the loss and increasing the accuracy. If I were to build from this model, I would like to add another parameter to match and classify like-featured animals. The ones that fall under the crack of classification. Examples, in terms or haircolor, eyecolor, fur type etc.
"""