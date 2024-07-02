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


def count_liste2er(text, liste):
    for i in range(len(text)):
        paar = text[i:i+2]
        if paar in liste:
            liste[paar] += 1
        else:
            if len(paar) == 1:
                break
            liste.update({paar: 1})
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


def informationsgehalt(liste_w,liste_i):
    for character in liste_w:
        wahrscheinlichkeit = liste_w[character]
        # infogehalt = float(format((-1*math.log2(wahrscheinlichkeit)), '.3f'))
        infogehalt = -1 * math.log2(wahrscheinlichkeit)
        liste_i.update({character: infogehalt})
    print("Informationsgehalt der Zeichen: " + str(liste_i))


def entropie(liste, liste_w, liste_i):
    entropie_ = 0
    for character in liste:
        wahrscheinlichkeit = liste_w[character]
        infogehalt = liste_i[character]
        entropie_ += wahrscheinlichkeit * infogehalt
    # entropie_ = float(format(entropie_, '.4f'))
    print("Entropie: " + str(entropie_) + "\n")
    return entropie_



def Z_statistik(fileName):
    listeZ = {}
    liste_wahrscheinlichkeitenZ = {}
    liste_informationsgehaltZ = {}
    print("Z_Statistik" + "\n")
    print(f'Dateiname: {fileName}' + "\n")
    fobj = open(fileName, "r")
    textinhalt = fobj.read()
    gesamtanzahl_zeichenZ = len(textinhalt)
    print(textinhalt + "\n")

    count_liste(textinhalt, listeZ)
    wahrscheinlichkeiten(listeZ, liste_wahrscheinlichkeitenZ, gesamtanzahl_zeichenZ)
    informationsgehalt(liste_wahrscheinlichkeitenZ, liste_informationsgehaltZ)
    entropieZ = entropie(listeZ, liste_wahrscheinlichkeitenZ, liste_informationsgehaltZ)

    fobj.close()


def Z2_statistik(fileName):
    listeZ2 = {}
    liste_wahrscheinlichkeitenZ2 = {}
    liste_informationsgehaltZ2 = {}
    print("Z2_Statistik" + "\n")
    print(f'Dateiname: {fileName}' + "\n")
    fobj = open(fileName, "r")
    textinhalt = fobj.read()
    gesamtanzahl_zeichenZ2 = len(textinhalt)

    print(textinhalt + "\n")

    count_liste2er(textinhalt, listeZ2)
    wahrscheinlichkeiten(listeZ2,liste_wahrscheinlichkeitenZ2, gesamtanzahl_zeichenZ2)
    informationsgehalt(liste_wahrscheinlichkeitenZ2, liste_informationsgehaltZ2)
    entropieZ2 = entropie(listeZ2, liste_wahrscheinlichkeitenZ2, liste_informationsgehaltZ2)

    fobj.close()


def W_statistik(fileName):
    listeW = {}
    liste_wahrscheinlichkeitenW = {}
    liste_informationsgehaltW = {}
    print("W_Statistik" + "\n")
    print(f'Dateiname: {fileName}' + "\n")
    fobj = open(fileName, "r")
    textinhalt = fobj.read()
    print(str(textinhalt) + "\n")
    textinhalt = re.split('[\\ ,.:;/?!()&\'\" \n]', textinhalt)
    textinhalt = [item for item in textinhalt if item.strip()]
    gesamtanzahl_zeichen = len(textinhalt)
    print("Nach Split: " + str(textinhalt) + "\n")

    count_liste(textinhalt, listeW)
    wahrscheinlichkeiten(listeW,liste_wahrscheinlichkeitenW, gesamtanzahl_zeichen)
    informationsgehalt(liste_wahrscheinlichkeitenW, liste_informationsgehaltW)
    entropieW = entropie(listeW, liste_wahrscheinlichkeitenW, liste_informationsgehaltW)

    fobj.close()


if __name__ == '__main__':
    shannon = "shannon.txt"
    fileName2 = "test.txt"
    fileName3 = "test2.txt"
    fileNameW = "testW.txt"
    Z_statistik(shannon)
    Z2_statistik(shannon)
    W_statistik(shannon)

