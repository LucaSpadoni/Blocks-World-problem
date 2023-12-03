import numpy as np
from tensorflow import keras as keras
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPool2D
import matplotlib.pyplot as plt

def remove(digit, x, y):
    idx = (y != digit).nonzero()

    return x[idx], y[idx]

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data() 

# Rimuove le cifre da 7 a 9 dal dataset
for i in range(7, 10): 
    x_train, y_train = remove(i, x_train, y_train)
    x_test, y_test = remove(i, x_test, y_test)

# Rimuove la cifra 0 dal dataset
x_train, y_train = remove(0, x_train, y_train)
x_test, y_test = remove(0, x_test, y_test)

x_train = np.expand_dims(x_train, -1)
x_train = x_train.astype("float32") / 255
x_test = np.expand_dims(x_test, -1)
x_test = x_test.astype("float32") / 255

# Costruzione layers
model = keras.Sequential()  # Crea un modello sequenziale ed aggiunge i vari layer
model.add(Conv2D(filters=24, kernel_size=(3, 3), activation = "relu"))    # Layer collegato all'input (512)
model.add(MaxPool2D(pool_size=(2, 2)))      # Lunghezza, altezza
model.add(Dropout(0.5))     # Setta randomicamente a 0 le unità di input con una frequenza di 0.5 (evita l'overfitting) 
model.add(Conv2D(filters=36, kernel_size=(3, 3)))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(0.5))     
model.add(Flatten())    # Appiattisce gli array per livelli fully-connected
model.add(Dense(128, activation = "relu"))    # 256
model.add(Dense(7, activation = "softmax"))    # Layer di output per le 6 cifre

model.predict(x_train[[0]])

model.summary() 

BATCH_SIZE = 64     # 128
EPOCHS = 10     # 15

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])   # Crossentropy

history = model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Crezione del grafico per l'accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper left')
plt.show()

# Crezione del grafico per la loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper left')
plt.show()

model.save("./models/model.h5")  # Salviamo il modello per utilizzarlo nel riconoscimento delle cifre

