#!/usr/bin/env python
import urllib.request
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import sys

plt.style.use('seaborn-white')
plt.rcParams["figure.figsize"] = (20, 8)

# ID predmeta
predmeti = {"IF1": 40, "IM1": 12, "LAG": 44, "OE": 2093, "OR": 1, "IM2": 13, "MLTI": 2096, "OS": 2098, "TP": 2,
            "VIS": 2097, "ASP": 42, "DM": 4, "LD": 43, "OBP": 105, "RPR": 9, "SP": 10, "AFJ": 41, "OOAD": 104,
            "ORM": 6, "RA": 22, "RMA": 2102, "US": 2103}
godina = {"2020/21": 16, "2019/20": 15, "2018/19": 14, "2017/18": 13, "2016/17": 12}

global app
global comboPredmet
global comboGodina
global total


def dajocjenu(ocjena):
    """Vraca 5 ako je str /, inace vraca str"""
    if ocjena == '/':
        return '5'
    return ocjena


def dajbrojbodova(brojbodova):
    """Vraca -1 ako je str /, inace vraca str"""
    if brojbodova == '/':
        return '-1'
    return brojbodova


def dajlinkcvs(index, ag):
    """Vraca link excel fajla izvjestaja za predmet sa ID index u akademskoj godini ag"""
    return "https://zamger.etf.unsa.ba/index.php?sta=izvjestaj/csv_converter&koji_izvjestaj=izvjestaj/predmet&predmet" \
           "=%d&ag=%d&sm_arhiva=1" % (index, ag)


def dajsljedecudeseticu(broj):
    broj = round(broj)
    while broj % 10 != 0:
        broj = broj + 1
    return broj


def dajispite(url):
    i = 0
    ukupno = 0
    global total
    ispiti = {}
    poc_indeks = 4
    preskoci = False
    data = urllib.request.urlopen(url)
    for line in data:
        if preskoci:
            preskoci = False
            continue
        if i < 9:
            i = i + 1
            if i == 8:
                pom = line.decode('cp1250').split(';')
                poc_indeks = pom.index('Ispiti')
            if i == 9:
                pom = line.decode('cp1250').split(';')
                for x in pom:
                    ispiti[x] = []
                ispiti.popitem()
            continue
        value = line.decode('cp1250').split(';')
        if len(value) > 1:
            if value[0] == 'R.br.':
                preskoci = True
                continue
            ukupno = ukupno + 1
            pom = poc_indeks
            for key in ispiti:
                bodovi = float(dajbrojbodova(value[pom]).replace(',', '.'))
                if bodovi > -1:
                    ispiti[key].append(bodovi)
                pom = pom + 1
    total = ukupno
    return ispiti


def dajpodatke():
    global app
    global comboPredmet
    global comboGodina

    lista = dajispite(dajlinkcvs(predmeti[comboPredmet.get()], godina[comboGodina.get()]))
    app.destroy()
    app.quit()
    for key in lista:
        plt.ylabel("Bodovi")
        plt.title(key)
        plt.xlim([-1, len(lista[key]) + 5])
        plt.ylim([-3, 100])
        plt.xticks([-1, len(lista[key])], "")
        plt.yticks(range(0, 101, 5))

        if len(lista[key]) != 0:
            maxbodovi = dajsljedecudeseticu(max(lista[key]))
            boje = []
            polozili = 0
            for x in lista[key]:
                if x >= maxbodovi / 2.:
                    boje.append('b')
                    polozili = polozili+1
                else:
                    boje.append('r')
            plt.scatter(range(0, len(lista[key])), lista[key], color=boje)
            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')
            plt.text(-1, -8, "Broj studenata koji su pristupili ispitu: %d\nBroj studenata koji su položili ispit: %d" %
                     (len(lista[key]), polozili))
            plt.show()
    gui()


def izlaz():
    sys.exit()


def gui():
    global app
    global comboPredmet
    global comboGodina

    app = tk.Tk()
    app.title("Izaberi predmet i akademsku godinu")
    app.geometry('300x150')

    labelTop = tk.Label(app,
                        text="Izaberi predmet")
    labelTop.pack()
    comboPredmet = ttk.Combobox(app,
                                values=list(predmeti.keys()), state='readonly')
    comboPredmet.pack()
    labelBottom = tk.Label(app, text="Izaberi akademsku godinu")
    labelBottom.pack()
    comboGodina = ttk.Combobox(app, values=["2016/17", "2017/18", "2018/19", "2019/20", "2020/21"], state='readonly')
    comboGodina.current(0)
    comboPredmet.current(0)
    comboGodina.pack()
    btnOk = ttk.Button(app, text="Ok", command=dajpodatke)
    btnOk.pack()
    btnCancel = ttk.Button(app, text="Cancel", command=izlaz)
    btnCancel.pack()
    app.mainloop()


# ---MAIN---
gui()
