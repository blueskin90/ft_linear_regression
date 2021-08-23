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

def saveTetha(tetha0, tetha1, kmscale, pricescale):
    try:
        tethas = open("tethas.txt", "w")
        tethas.write(f"{tetha0:.20f} {tetha1:.20f} {kmscale} {pricescale}") 
        tethas.close()
    except Exception:
        sys.exit("Couldn't write tethas in tethas.txt file")

def getTetha():
    try:
        tethas = open("tethas.txt", "r")
        values = tethas.read().rstrip().strip()
        tethas.close()
        splitted = values.split(" ")
        if len(splitted) != 4:
            print("Couldn't read tetha values from tethas.txt, defaulting to 0");
            return (0, 0, 1, 1)   
        tetha0 = float(splitted[0])
        tetha1 = float(splitted[1])
        kmscale = float(splitted[2])
        pricescale = float(splitted[3])
        return (tetha0, tetha1, kmscale, pricescale)
    except Exception:
        print("Couldn't read tetha values from tethas.txt, defaulting to 0");
        return (0, 0, 1, 1)

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

def calculateTetha(data, t0, t1):
    tmp0 = 0
    tmp1 = 0
    for index, dat in enumerate(data):
        prix = prixEstime(dat.km, t0, t1)
        tmp0 += (prix - dat.price)
        tmp1 += ((prix - dat.price) * dat.km)

    tmp0 *= (1 / (index + 1))
    tmp1 *= (1 / (index + 1))

    tmp0 *= 0.0001
    tmp1 *= 0.0001
    print(t0, tmp0, t0 - tmp0)
    return t0 - tmp0, t1 - tmp1

def prixEstime(kilometrage, tetha0, tetha1):
    value = tetha0 + (tetha1 * kilometrage)
    return value

def display(data):
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

def getMax(datas):
    maxkm = 0
    maxprice = 0
    for data in datas:
        if data.price > maxprice:
            maxprice = data.price
        if data.km > maxkm:
            maxkm = data.km
    return maxkm, maxprice

def normalizeData(datas, kmmax, pricemax):
    retval = []
    for data in datas:
        retval.append(Data(data.km / kmmax, data.price / pricemax))
    return retval

def main(ac, av):
    if ac != 2:
        sys.exit("usage: python3 ft_linear_regression_train `data to train on`")
    data = parsing(av[1])
    tetha0, tetha1,_,_ = getTetha()
    kmmax, pricemax = getMax(data)
    display(data)
    data = normalizeData(data, kmmax, pricemax)
    for i in range(100):
        theta0, theta1 = calculateTetha(data, deepcopy(tetha0), deepcopy(tetha1))
    saveTetha(tetha0, tetha1, kmmax, pricemax)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)

