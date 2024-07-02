import math
import re


def count_liste(text, liste):
    for i in range(len(text)):
        zeichen = text[i]
        if zeichen in liste:
            liste[zeichen] += 1
        else:
            liste.update({zeichen: 1})
    print("Häufigkeit der Zeichen: " + str(liste))
    print("Gesamtanzahl der Zeichen: " + str(len(text)))


def wahrscheinlichkeiten(liste, liste_w, gesamt):
    for character in liste:
        # wahrscheinlichkeit = float(format((liste[character] / gesamt), '.3f'))
        wahrscheinlichkeit = liste[character] / gesamt
        liste_w.update({character: wahrscheinlichkeit})
        # print("Wahrscheinlichkeit fuer " + str(character))
        # print(wahrscheinlichkeit)
    print("Wahrscheinlichkeiten der Zeichen: " + str(liste_w))


def Z_statistik(fileName):
    listeZ = {}
    liste_wahrscheinlichkeitenZ = {}
    print("Z_Statistik" + "\n")
    print(f'Dateiname: {fileName}' + "\n")
    fobj = open(fileName, "r")
    textinhalt = fobj.read()
    gesamtanzahl_zeichenZ = len(textinhalt)
    print(textinhalt + "\n")
    count_liste(textinhalt, listeZ)
    wahrscheinlichkeiten(listeZ, liste_wahrscheinlichkeitenZ, gesamtanzahl_zeichenZ)
    fobj.close()
    return liste_wahrscheinlichkeitenZ


def liste_teilen(liste_W_values, dic_w_values):
    sum1 = 0
    sum_list = sum(liste_W_values)
    sum_list_half = sum_list / 2
    for i in range(len(liste_W_values)):
        if len(liste_W_values) == 2:
            key_fnc = liste_W_values[0]
            dic_w_values[key_fnc] += '0'

            key_fnc = liste_W_values[1]
            dic_w_values[key_fnc] += '1'
            return
        elif len(liste_W_values) <= 1:
            return

        sum1 += liste_W_values[i]

        if sum1 > sum_list_half:
            differenz = liste_W_values[0] - sum(liste_W_values[1:])
            if 0.1 >= differenz >= -0.1:
                if i == 0:
                    range_number = 1
                else:
                    range_number = i
            else:
                range_number = i + 1

            for index in range(range_number):
                key_fnc = liste_W_values[index]
                dic_w_values[key_fnc] += '0'
            for index in range(range_number, len(liste_W_values)):
                dic_w_values[liste_W_values[index]] += '1'

            liste_teilen(liste_W_values[:range_number], dic_w_values)
            liste_teilen(liste_W_values[range_number:], dic_w_values)
            return


def Q_Fanoencoder(fileName):
    fobj = open(fileName, "r")
    textinhalt = fobj.read()
    test = []

    # Sortieren nach Wahrscheinlichkeit
    dict_W = Z_statistik(fileName)
    dict_W = sorted(dict_W.items(), key=lambda x: x[1], reverse=True)
    dict_W = dict(dict_W)

    # Seperate Liste von den Zeichen und der jeweiligen Wahrscheinlichkeit
    liste_W_values = list(dict_W.values())
    liste_W_keys = list(dict_W.keys())
    print(liste_W_keys)
    print(liste_W_values)
    # liste_W_values = [0.05, 0.03, 0.17, 0.23, 0.01, 0.32, 0.19]
    liste_W_values.sort(reverse=True)
    dic_W_values = {key: '' for key in liste_W_values}

    liste_teilen(liste_W_values, dic_W_values)

    codewords_fnc = {}
    for i in range(len(liste_W_keys)):
        key = liste_W_keys[i]
        value = dic_W_values[liste_W_values[i]]
        codewords_fnc.update({key: value})

    encoded_fnc = [""]
    for i in range(len(textinhalt)):
        zeichen = textinhalt[i]
        if zeichen in codewords_fnc:
            code = codewords_fnc[zeichen]
            encoded_fnc[0] += code

    fobj.close()
    return codewords_fnc, encoded_fnc


if __name__ == '__main__':
    shannon = "shannon.txt"
    test = "test.txt"
    codeword, encoded = Q_Fanoencoder(test)
    for key, value in codeword.items():
        print(f"Zeichen: {key} Codewort: {value}")
    print(encoded)

