import numpy as np
import random
import matplotlib.pyplot as plt
import time

start_time = time.time()


def nachricht_senden(nachricht, fehler_wahrscheinlichkeit, pos_fehlerwahrscheinlichkeit):
    # Nachricht verschlüsseln
    Ldata_encoded = hamming_encoder(nachricht)
    # Nachricht durch Kanal senden
    Ldata_encoded_error = channel_bsc(Ldata_encoded, fehler_wahrscheinlichkeit)
    # Nachricht entschlüsseln
    Ldata_decoded, Ldata_after_corrected = hamming_decoder(Ldata_encoded_error)

    # Anzahl der Unterschiede der gesendeten Nachricht
    # und der empfangenen Nachricht
    Bitfehler = hamming_distanz(nachricht, Ldata_decoded)
    Bitfehler_gesamt[pos_fehlerwahrscheinlichkeit] += Bitfehler

    # Anzahl der Unterschiede der verschlüsselten Nachricht
    # und der Nachricht nachdem der durch den Kanal ging
    Kanalfehler = hamming_distanz(Ldata_encoded_error, Ldata_encoded)
    Kanalfehler_gesamt[pos_fehlerwahrscheinlichkeit] += Kanalfehler


def hamming_distanz(array1, array2):
    anzahl = 0
    for a, b in zip(array1, array2):
        if a != b:
            anzahl += 1
    return anzahl


def channel_bsc(encoded_data, prob):
    fehlerwort = []
    for _ in range(len(encoded_data)):
        if random.random() < prob:
            fehlerwort.append(1)
        else:
            fehlerwort.append(0)

    nachricht_nach_kanal = np.array(encoded_data) ^ np.array(fehlerwort)
    return nachricht_nach_kanal


def pruefgleichung_berechnen(tupel_7, pruefmatrix):
    tmp = 0
    vektor_ergebnis = []
    for q in range(3):
        for k in range(7):
            tmp += pruefmatrix[q][k] * tupel_7[k]
        vektor_ergebnis.append(tmp % 2)
        tmp = 0
    return vektor_ergebnis


def syndrom_korrigieren(tupel_7, pruefmatrix, syndrom):
    syndrom = np.array(syndrom).reshape(3, 1)
    equal_columns = np.all(pruefmatrix == syndrom, axis=0)

    for index, t in enumerate(equal_columns):
        if t:
            pos_of_syndrom = index
            break

    # print("\nPoistion des Syndroms in H:")
    # print(pos_of_syndrom + 1)
    tupel_7[pos_of_syndrom] = tupel_7[pos_of_syndrom] ^ 1
    # print("\nKorrigierte Tupel 7: ")
    # print(tupel_7)


def nullen_hinzufuegen(data, anzahl_rest_nullen):
    for _ in range(anzahl_rest_nullen):
        data.append(0)
    # print("Hinzugefügte Nullen: " + str(anzahl_rest_nullen))
    # print("\nData nach hinzufügen der Nullen: ")
    # print(data)


def hamming_encoder(data):
    # print("ENCODE")
    G = [[1, 0, 0, 0, 1, 1, 1],
         [0, 1, 0, 0, 1, 1, 0],
         [0, 0, 1, 0, 1, 0, 1],
         [0, 0, 0, 1, 0, 1, 1]]
    data_length = len(data)
    data_coded = []
    anzahl_rest_nullen = 4 - (data_length % 4)

    # print(data)
    # print("\nLänge der Daten: " + str(len(data)))

    if data_length % 4 != 0:
        nullen_hinzufuegen(data, anzahl_rest_nullen)

    for f in range(0, data_length, 4):
        tupel_4 = [data[f:f + 4]]
        # print("\n4Tupel:")
        # print(tupel_4)
        matrix_ergebnis = np.transpose(tupel_4) * G
        tupel4_coded = matrix_ergebnis[0]
        '''
        # Gibt zeilen aus
        for i in range(4):
            if tupel_4[0][i] == 1:
                print(str(i + 1) + "te Zeile des Generatorpolynoms")
                print(G[i])
        '''
        for g in range(1, 4):
            for k in range(7):
                tupel4_coded[k] = tupel4_coded[k] ^ matrix_ergebnis[g][k]

        # print("\n4Tupel codiert:")
        # print(tupel4_coded)
        data_coded.extend(tupel4_coded)

    # print("\nGesamt Daten codiert:")
    # print(data_coded)
    # print("Länge der Codierten Daten:" + str(len(data_coded)))
    return data_coded


def hamming_decoder(encoded_data):
    # print("\n\nDECODE")
    # decoded_data = [1, 0, 0, 0, 1, 1, 0]
    data_decoded = []
    data_nach_korrektur = []
    H = [[1, 1, 1, 0, 1, 0, 0],
         [1, 1, 0, 1, 0, 1, 0],
         [1, 0, 1, 1, 0, 0, 1]]
    # print(decoded_data)
    data_length = len(encoded_data)
    # print("\nLänge der verschlüsselten Daten: " + str(len(decoded_data)))

    for o in range(0, data_length, 7):
        tupel_7 = encoded_data[o:o + 7]
        # print("\n7Tupel:")
        # print(tupel_7)
        syndrom = pruefgleichung_berechnen(tupel_7, H)

        # print("\nSyndrom:")
        # print(syndrom)
        if np.sum(syndrom) != 0:
            syndrom_korrigieren(tupel_7, H, syndrom)

        data_nach_korrektur.extend(tupel_7)
        tupel_4 = tupel_7[:-3]
        data_decoded.extend(tupel_4)

    return data_decoded, data_nach_korrektur


if __name__ == '__main__':
    N_iteration = 100
    Bitfehler_gesamt = [0] * 19
    Kanalfehler_gesamt = [0] * 19
    p_array = []

    # Array mit den p Werten aus Aufgabenteil d)
    for i in range(0, 22, 2):
        p_array.append(i / 100)
    for i in range(3, 11, 1):
        p_array.append(i / 10)

    for pos, p in enumerate(p_array):
        for _ in range(N_iteration):
            orig_nachricht = [random.randint(0, 1) for _ in range(100)]
            nachricht_senden(orig_nachricht, p, pos)

    Bitfehler_gesamt = np.array(Bitfehler_gesamt) / N_iteration
    Kanalfehler_gesamt = np.array(Kanalfehler_gesamt) / N_iteration
    x_axis = []

    x = p_array
    y_b = Bitfehler_gesamt
    y_k = Kanalfehler_gesamt

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(x)), y_b, marker='o', linestyle='-', color='red')
    plt.plot(range(len(x)), y_k, marker='o', linestyle='-', color='blue')
    plt.xticks(range(len(x)), x)
    plt.yscale('log')

    plt.xlabel('Fehlerwahrscheinlichkeit')
    plt.ylabel('Anzahl der Fehler')
    plt.title('BER in Rot und CER in Blau')
    plt.grid(True)

    # Display the plot
    plt.show()

    end_time = time.time()
    execution_time = end_time - start_time

    print("Rechendauer: {:.3f} seconds".format(execution_time))
