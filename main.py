#identfiy gender
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

image_size=(180,180)
input_shape=(180,180,3)
batch_size=16
epochs=3
num_classes=2

train_ds=keras.preprocessing.image_dataset_from_directory(
    "./Dataset/Train/",
    validation_split=0.2,
    seed=1337,
    subset="training",
    image_size=image_size,
    batch_size=batch_size,
)
val_ds=keras.preprocessing.image_dataset_from_directory(
    "./Dataset/Validation/",
    validation_split=0.2,
    seed=1337,
    subset="validation",
    image_size=image_size,
    batch_size=batch_size,
)
train_ds=train_ds.prefetch(buffer_size=32)
val_ds=val_ds.prefetch(buffer_size=32)

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.experimental.preprocessing.Rescaling(1.0/255),
        layers.Conv2D(32,kernel_size=(3,3),activation="relu"),
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(1,activation="sigmoid"),
    ]
)

model.summary()
model.compile(loss="binary_crossentropy",optimizer=keras.optimizers.Adam(1e-3),metrics=["accuracy"])
model.fit(
    train_ds,epochs=epochs,validation_data=val_ds,
)
