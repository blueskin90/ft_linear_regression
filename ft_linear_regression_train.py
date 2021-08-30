# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_linear_regression_train.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: toliver <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/08/23 17:29:00 by toliver           #+#    #+#              #
#    Updated: 2021/08/23 17:32:38 by toliver          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import io
import re
import math
import matplotlib.pyplot as plt
from copy import deepcopy

class Data:
    def __init__(self, km, price):
        self.km = km
        self.price = price
    def __str__(self):
        return 'km: {}\t price: {}'.format(self.km, self.price)

class Regression:
    def __init__(self):
        self.setValues()

    def saveTetha(self):
        try:
            tethas = open("tethas.txt", "w")
            tethas.write(f"{self.tetha0:.20f} {self.tetha1:.20f} {self.kmscale} {self.pricescale}") 
            tethas.close()
        except Exception:
            sys.exit("Couldn't write tethas in tethas.txt file")

    def setValues(self):
        try:
            tethas = open("tethas.txt", "r")
            values = tethas.read().rstrip().strip()
            tethas.close()
            splitted = values.split(" ")
            if len(splitted) != 4:
                raise Exception()
            self.tetha0 = float(splitted[0])
            self.tetha1 = float(splitted[1])
            self.kmscale = float(splitted[2])
            self.pricescale = float(splitted[3])
        except Exception:
            print("Something went wrong when reading values from tethas.txt, defaulting to tethas to 0 and scales to 1");
            self.tetha0 = 0
            self.tetha1 = 0
            self.kmscale = 1
            self.pricescale = 1

    def getScale(self, datas):
        self.kmscale = 1
        self.pricescale = 1
        for data in datas:
            if data.price > self.pricescale:
                self.pricescale = data.price
            if data.km > self.kmscale:
                self.kmscale = data.km


    def calculateTetha(self, data):
        for i in range(1000000):
            tmp0 = 0
            tmp1 = 0
            for index, dat in enumerate(data):
                prix = self.prixEstime(dat.km)
                tmp0 += (prix - dat.price)
                tmp1 += ((prix - dat.price) * dat.km)

            tmp0 = tmp0 / (index + 1)
            tmp1 = tmp1 / (index + 1)

            tmp0 = tmp0 * 0.0001
            tmp1 = tmp1 * 0.0001
            self.tetha0 = self.tetha0 - tmp0
            self.tetha1 = self.tetha1 - tmp1

    def prixEstime(self, kilometrage):
        value = self.tetha0 + (self.tetha1 * kilometrage)
        return value

    def normalizeData(self, datas):
        retval = []
        for data in datas:
            retval.append(Data(data.km / self.kmscale, data.price / self.pricescale))
        return retval

def parsing(path):
    try:
        myfile = open(path, "r")
        content = myfile.read().rstrip().strip().split("\n")
        myfile.close()
        retval = []
        if content[0] != "km,price":
            sys.exit("not well formated data")
        del content[0]
        for cont in content:
            splitted = cont.split(",")
            if len(splitted) != 2:
                sys.exit("not well formated data")
            retval.append(Data(int(splitted[0]), int(splitted[1])))
        return retval
    except Exception as e:
        sys.exit("Couldn't read data file")

def display(self, data):
    x = []
    y = []

    for dat in data:
        y.append(dat.km)
        x.append(dat.price)
    plt.scatter(x, y)
    plt.xlabel('kilometres')
    plt.ylabel('prix')
    plt.title('price / km graph')
    plt.show()

def main(ac, av):
    if ac != 2:
        sys.exit("usage: python3 ft_linear_regression_train `data to train on`")
    reg = Regression()
    data = parsing(av[1])
    reg.getScale(data)
    #display(data)
    data = reg.normalizeData(data)
    reg.calculateTetha(data)

    for dat in data:
        print(dat)
    reg.saveTetha()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)

