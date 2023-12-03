import os
import numpy as np
from tensorflow import keras as keras
import cv2

model = keras.models.load_model("./models/model.h5") # Carica la nostra CNN pre-allenata sul dataset MNIST
detected_digits = [np.array([]) for x in range(6)] # Lista contenente le cifre rilevate di grandezza massima 6
digits_position = [None for x in range(6)] # Lista contenente la relative posizione (coordinate e altezza e larghezza relative) delle cifre rilevate di grandezza massima 6

# Ritorna lo stato per BlocksWorld
def get_state(path):
    area = image_processor(path)
    state = create_state(digits_position, area)

    return state

# Data l'immagine trova i numeri presenti e le relative posizioni
def image_processor(path):
    global detected_digits, digits_position
    
    detected_digits = [np.array([]) for x in range(6)]
    digits_position = [None for x in range(6)]
    box_size = 50   # 40

    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)    # Scala di grigi
    pre_processed_img = pre_process_image(img)
    final_img = box_processing(pre_processed_img, box_size)
    final_img = post_process_image(final_img)
    digits, area = box_detection(final_img)
    digits_detection(digits, ~final_img, img)

    for i in range(6):  # Evidenzia i blocchi in cui sono presenti le cifre per una rappresentazione grafica
        if detected_digits[i].size > 0:
            image = detected_digits[i]
            x, y, width, height = block_borders(digits_position[i], ~final_img)   # Per ogni cifra individuata prende le coordinate del blocco relativo
            digits_position[i] = (x, y, width, height)  
            colour = (0, 0, 0)
            thickness = 10
            cv2.rectangle(img, (x, y), (width, height), colour, thickness)

    cv2.namedWindow("Immagine Processata", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Immagine Processata",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    show_image("Immagine Processata", img)

    return area

# Definisce lo stato che BlocksWorld userà in base alle immagini passate
def create_state(digits_position, area):
    coordinates = []
    cols = [[] for x in range(6)]

    for i in range(6):
        if digits_position[i] is not None:
            x1, y1, x1_width, y1_height = digits_position[i]
            coordinates.append(((x1_width + x1) // 2, ((y1_height + y1) // 2)))  # Ogni blocco è formato da due coppie di coordinate, rappresentanti due vertici opposti
            c = [i+1]

            for j in range(6):
                if digits_position[j] is not None and j != i:
                    x3, y3, x3_width, y3_height = digits_position[j]
                    if coordinates_check((x1, x1_width, x3, x3_width)):
                        c.append(j + 1)
            c.sort()
            cols[i] = tuple([*c])
        else:
            cols[i] = ()

    temp_cols = list(set(tuple(cols)))
    cols = []

    if () in temp_cols:
        temp_cols.remove(())

    for t_col in temp_cols:
        col = list(t_col)
        col.sort(reverse=True, key=lambda e: coordinates[e-1][1])
        cols.append(tuple(col))

    cols.sort(key=lambda e: coordinates[e[0]-1][0])
    last = [col[0] for col in cols]
    distance = []
    x5, _, x6, _ = area
    x7, _, x7_width, _ = digits_position[last[0]-1]

    distance2 = abs(x7 - x5)
    distance2 = distance2 / (x7_width - x7)
    distance.append(distance2)

    for i in range(len(last) - 1):
        x1, _, x1_width, _ = digits_position[last[i]-1]
        x3, _, _, _ = digits_position[last[i+1]-1]
        distance2 = abs(x3 - x1_width)
        distance2 = distance2 / (x1_width - x1)
        distance.append(distance2)

    x7, _, x7_width, _ = digits_position[last[-1]-1]
    distance2 = abs(x6 - x7_width)
    distance2 = distance2 / (x7_width - x7)
    distance.append(distance2)

    for i in range(len(distance)):
        distance2 = distance[i]
        if distance2 - int(distance2) >= 0.5:
            distance[i] = int(distance2) + 1
        else:
            distance[i] = int(distance2)

    # n = sum(distance) + len(cols)

    n = 0
    for i in range(6):  # Trova quante cifre sono state identificate
        if detected_digits[i].size > 0:
            n += 1

    i = distance[0]
    state = []
    position = 1

    for col in cols:
        j = 0
        for square in col:
            state.append((square, j, i))    # Tripla che rappresenta il blocco (numero, coordinata y e coordinata x)
            j += 1
        i += distance[position] + 1
        position += 1
    state.append(n)

    return tuple(state)

# Controlla le coordinate del box
def coordinates_check(values):
    x1, x2, x3, x4 = values
    new_x = (x3 + x4) // 2  # Parte intera

    if x1 < new_x and x2 > new_x:
        return True

    return False

# Applica funzioni di blurring all'immagine per estrarre le sue features
def pre_process_image(img):	
    img = cv2.medianBlur(img, 3)
    img = cv2.GaussianBlur(img, (3, 3), 0) # Applica una Gaussian blur con un kernel di dimensioni 3x3 (deve essere sempre dispari)
    img = 255 - img

    return img 

# Individua e processa l'immagine del riquadro
def box_processing(img, box_size):
    new_img = np.zeros_like(img)   # Immagine binaria (trasforma l'array in zeri con la stessa shape di img) 

    for row in range(0, img.shape[0], box_size):
        for col in range(0, img.shape[1], box_size):
            idx = (row, col)
            block_idx = box_coordinates(img.shape, idx, box_size)
            new_img[tuple(block_idx)] = custom_adaptive_threshold(img[tuple(block_idx)])

    return new_img  

# Restituisce le coordinate del relativo box in una griglia. Facciamo il max per avere coordinate non negative dato che l'asse delle y è rivolto verso il basso
def box_coordinates(image_shape, coord, box_size):
    x = np.arange(max(0, coord[1] - box_size), min(image_shape[1], coord[1] + box_size)) 
    y = np.arange(max(0, coord[0] - box_size), min(image_shape[0], coord[0] + box_size))

    return np.meshgrid(y, x)    # N.B. La griglia ha coordinate invertite 

# Computa un thresholding (separa la parte in primo piano da quella in secondo piano) nella data regione di immagine date una certa soglia e mediana
def custom_adaptive_threshold(img):
    threshold = 40

    med = np.median(img)
    new_img = np.zeros_like(img)
    new_img[img - med < threshold] = 255

    return new_img

# Applica ancora funzioni di blurring all'immagine (che serviranno per estrarre le sue features) e trova i contorni dell'immagine binaria (post processata) eliminando il rumore per 
# facilitare il riconoscimento delle cifre (contorni la cui area inferiore ad una determinata soglia)
def post_process_image(img):
    img = cv2.medianBlur(img, 5)
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.erode(img, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approxed_box = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
        x, y, w, z = cv2.boundingRect(approxed_box)

        if noise_detection(contour, approxed_box, img.shape[::-1]):
            cv2.drawContours(img, [approxed_box], 0, 255, -1)

    return img

# Cerca il rumore che verrà poi eliminato dall'immagine
def noise_detection(contour, approxed_box, img_size):
    width, height = img_size
    x, y, height2, width2 = cv2.boundingRect(approxed_box)
    area = height * width

    if cv2.contourArea(contour) >= area/1000:
        return False
    if height2 >= height/50 or width2 >= width/50:
        return False

    return True

# Trova il perimetro dell'immagine che contiene i blocchi
def box_detection(img):
    height, width = img.shape[0:2]
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours.sort(reverse=True, key=lambda c: cv2.contourArea(c))
    contour = contours[1]
    approxed_box = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
    x, y, w, z = cv2.boundingRect(approxed_box)
    area = (x, y, x + w, y + z)
    img = img[y:y+z, x:x+w]
    sub = img.copy()
    bg = ~np.zeros((z + 50, w + 50), np.uint8)
    bg[25: 25 + z, 25: 25 + w] = img
    img = bg
    i = 0
    height2, width2 = img.shape[0:2]
    tot = np.zeros(shape=(height2, width2))

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approxed_box = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)

        if hierarchy[0][i][3] == 0:
            cv2.drawContours(tot, [approxed_box], 0, 255, -1)

        if hierarchy[0][i][3] == 1:
            cv2.drawContours(tot, [approxed_box], 0, 0, -1)

        i += 1

    tot = tot[25: 25 + z, 25: 25 + w]
    kernel = np.ones((5, 5), np.uint8)
    tot = cv2.dilate(tot, kernel, iterations=3)
    tot = tot.astype('uint32')
    sub = sub.astype('uint32')
    res = sub + tot
    res = np.where(res == 0, 255, 0)
    result = np.zeros((height, width), np.uint8)
    result[y:y+z, x:x+w] = res

    return (result, area)

# Trova i numeri e le relative posizioni nell'immagine passata, inserendoli in una lista 
def digits_detection(digits, final_img, img):
    i = 0
    contours, hierarchy = cv2.findContours(digits, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Cifre identificate nell'immagine: ")

    for contour in contours:
        approxed_box = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
        x, y, width, height = cv2.boundingRect(approxed_box)

        if hierarchy[0][i][3] == -1:
            predicted_digit = digit_prediction(final_img[y:y + height, x:x + width])

            if predicted_digit != -1:
                detected_digits[predicted_digit] = img[y:y + height, x:x + width]
                digits_position[predicted_digit] = (x, y, x + width, y + height)  
        i += 1

# Usa il nostro modello per predirre le cifre nell'immagine passata
def digit_prediction(img):
    height, width = img.shape
    l = int(max(img.shape) * 1.2)
    new_height = int((l - height) / 2)
    new_width = int((l - width) / 2)
    new_image = np.zeros((l, l), np.uint8)
    new_image[new_height : new_height + height, new_width : new_width + width] = img
    new_image = (new_image / 255).astype('float64')
    new_image = cv2.resize(new_image, (28, 28), interpolation = cv2.INTER_AREA)     # Dato che le cifre su MNIST sono tutte 28x28
    _in = np.array([new_image])
    _in = np.expand_dims(_in, -1)
    predicted_digit = np.argmax(model.predict(_in))
    print("-", predicted_digit)

    if predicted_digit > 0:
        return predicted_digit - 1
    else:
       return -1

# Trova i bordi (e i relativi parametri) del blocco che contiene la cifra
def block_borders(dims, img):
    x1, y1, width, height = dims
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    x3 = (width + x1) // 2
    y3 = (height + y1) // 2
    width2 = x1 - 1

    while img[y3, width2] != 255:
        width2 -= 1
    x1 = width2
    width2 = width + 1
    while img[y3, width2] != 255:
        width2 += 1
    width = width2
    width2 = y1 - 1
    while img[width2, x3] != 255:
        width2 -= 1
    y1 = width2
    width2 = height + 1
    while img[width2, x3] != 255:
        width2 += 1
    height = width2

    return (x1, y1, width, height)

# Mostra l'immagine finchè un tasto non è premuto
def show_image(str, img):
    cv2.imshow(str, img) 
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  # Chiude tutte le finestre