#Adopted from https://www.tensorflow.org/tutorials/keras/save_and_load
import os
import sys

import tensorflow as tf
from tensorflow import keras

print(tf.version.VERSION)

(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

train_labels = train_labels[:1000]
test_labels = test_labels[:1000]

train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

# Define a simple sequential model
def create_model():
  model = tf.keras.Sequential([
    keras.layers.Dense(512, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

  return model



epoch_steps=int(sys.argv[1])


checkpoint_path = "training_1/{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1,
                                                 period=10)


# Create a basic model instance
model = create_model()

# Display the model's architecture
model.summary()

# Train the model with the new callback


if os.path.exists(checkpoint_dir):
  latest = tf.train.latest_checkpoint(checkpoint_dir)
   # Load the previously saved weights
  model.load_weights(latest)

  # Re-evaluate the model
  loss, acc = model.evaluate(test_images, test_labels, verbose=2)
  print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
  
else:
  initialEpoch=0
  # Save the weights using the `checkpoint_path` format
  model.save_weights(checkpoint_path.format(epoch=0))
   
model.fit(train_images, 
          train_labels,  
          epochs=epoch_steps,
          validation_data=(test_images, test_labels),
          callbacks=[cp_callback])  # Pass callback to training