import tensorflow as tf

from tensorflow.keras import datasets, layers, models

model = models.Sequential()
model.add(layers.Conv2D(6,6, (1,1), activation='relu', input_shape=(36,2)))
model.add(layers.MaxPooling2D(4, (2,2)))
#model.add(layers.BatchNormalization(center=True, scale=True, scope='bn'))
#model.add(layers.Conv2D(36, (1,1), activation='relu'))
#model.add(layers.MaxPooling2D(4, (2,2)))
#model.add(layers.BatchNormalization(center=True, scale=True, scope='bn'))
#model.add(layers.Conv2D(36, (1,1), activation='relu'))
#model.add(layers.MaxPooling2D(4, (2,2)))
#model.add(layers.BatchNormalization(center=True, scale=True, scope='bn'))
#model.add(layers.dense(units=1024, activation=tf.nn.relu))
#model.add(tf.nn.softmax((2,4)))


print(model.summary())