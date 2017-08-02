# coding=utf-8
import csv
from datetime import datetime
import sqlite3
import os
import re
database = sqlite3.connect(r"/home/mushtaq/monarcha/database.db")
c = database.cursor()


def read_timestamps_out_of_txt(path):               #soll timestamps aus gegebener Datei auslesen und in einer Liste of Datetime speichern
    lol = list(csv.reader(open(path, 'r'), delimiter='\t'))
    timestamps=[]
    for e in lol:
        for value in e:
            try:
                dt = datetime.fromtimestamp(float(value) / 1000.0)
                if dt.year > 2000 and dt.year < 2020:
                    timestamps.append(str(value))
            except:
                pass
    return timestamps



def make_list_of_columns():                             #soll Liste erstellen, die so aufgebaut ist: [BAT, LOC, BLTH, ...]
    regex = re.compile('[^a-zA-Z]')
    dtypes = []
    for root, dirs, files in os.walk("/home/mushtaq/monarcha/MonarchaData"):
        dtypes.append([files])
    dtypes2 = []
    for e in dtypes:
        for i in e[0]:
            dtypes2.append(regex.sub("", i)[:-3])
    dtypes2 = list(set(dtypes2))
    for e in dtypes2:
        if e == "":
            dtypes2.remove(e)
    return dtypes2



def make_list_of_persons(path):                                     #schaut was im Ordner path ist und schreibt alle Unterordner in eine Liste
    output = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI))]
    return output



def make_database(persons, list_of_columns):
    for e in persons:
        c.execute('''CREATE TABLE IF NOT EXISTS {}({} STRING)'''.format(e + list_of_columns[0], list_of_columns[0]))
        for i in range(1,(len(list_of_columns)-1)):
            c.execute('''CREATE TABLE IF NOT EXISTS {}({} STRING)'''.format(e + list_of_columns[i], list_of_columns[i]))




def crawl_directory(list_of_columns, person):                             #gewuenschte Listenform: [ [ "LOC", [ ]], [ "BAT", [ ]],...] ]
    regex = re.compile('[^a-zA-Z]')
    output = []
    for e in list_of_columns:                                           #Listenstruktur aufstellen: [ ["LOC"], ["BAT"], ...]
        output.append([e])

    L = []
    for root, dirs, files in os.walk("/home/mushtaq/monarcha/MonarchaData/" + person):                             #L: alle Dateien der Person mit zugehörigem Baum
        L.append([root, files])                                         #L: [ [ "~/1-2", [...txt, ....txt ] ] ]


    for e in L:                                             # e = z.B. [pfad, [a.txt, b.txt]]
        for k in range(len(e[1])-1):                        # k = index von z.B. b.txt

            for i in range(len(output)-1):                  # i = index von z.B. ["BAT"]
                try:

                    if regex.sub("", e[1][k])[:-3] == output[i][0]:
                        p = e[0]+"/"+e[1][k]
                        output[i].append(p)
                except:
                    pass
    return output                                           # output = z.B. [ ["LOC", "/home/.../a.txt", ...], ["BAT", "..."] ]



def start():
    personen = make_list_of_persons("/home/mushtaq/monarcha/MonarchaData")
    columns = make_list_of_columns()
    make_database(personen, columns)
    for e in personen:                                              # e = z.B. "p0102"
        data_person = crawl_directory(columns, e)

        for i in data_person:                                       # i = z.B. [BAT, []]

            for u in range(1, len(i)-1):                            # betrachte einzelne Dateipfade

                timestamps = read_timestamps_out_of_txt(i[u])

                for k in timestamps:
                    c.execute( "INSERT INTO %s VALUES(%s)" %(e + i[0], k))
            fo = open('aktueller_stand.txt', 'w')
            fo.write(str(e+i[0]))
            fo.close()
            database.commit()

start()
print("success!")



