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
        self.tetha0 = 0
        self.tetha1 = 0
    def saveTetha(self, tetha0, tetha1, kmscale, pricescale):
        try:
            tethas = open("tethas.txt", "w")
            tethas.write(f"{tetha0:.20f} {tetha1:.20f} {kmscale} {pricescale}") 
            tethas.close()
        except Exception:
            sys.exit("Couldn't write tethas in tethas.txt file")

    def getTetha(self ):
        try:
            tethas = open("tethas.txt", "r")
            values = tethas.read().rstrip().strip()
            tethas.close()
            splitted = values.split(" ")
            if len(splitted) != 4:
                print("Couldn't read tetha values from tethas.txt, defaulting to 0");
                return (0, 0, 1, 1)   
            self.tetha0 = float(splitted[0])
            self.tetha1 = float(splitted[1])
            kmscale = float(splitted[2])
            pricescale = float(splitted[3])
            return (tetha0, tetha1, kmscale, pricescale)
        except Exception:
            print("Couldn't read tetha values from tethas.txt, defaulting to 0");
            return (0, 0, 1, 1)

    def parsing(self, path):
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

    def calculateTetha(self, data):
        tmp0 = 0
        tmp1 = 0
        for index, dat in enumerate(data):
            prix = self.prixEstime(dat.km, self.tetha0, self.tetha1)
            tmp0 += (prix - dat.price)
            tmp1 += ((prix - dat.price) * dat.km)

        tmp0 = tmp0 * (1 / (index + 1))
        tmp1 = tmp1 * (1 / (index + 1))

        tmp0 = tmp0 * 0.000001
        tmp1 = tmp1 * 0.000001
        print(self.tetha0 - tmp0, self.tetha1 - tmp1)
        self.tetha0 = self.tetha0 + tmp0
        self.tetha1 = self.tetha1 + tmp1

    def prixEstime(self, kilometrage, tetha0, tetha1):
        value = tetha0 + (tetha1 * kilometrage)
        return value

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

    def getMax(self, datas):
        maxkm = 0
        maxprice = 0
        for data in datas:
            if data.price > maxprice:
                maxprice = data.price
            if data.km > maxkm:
                maxkm = data.km
        return maxkm, maxprice

    def normalizeData(self, datas, kmmax, pricemax):
        retval = []
        for data in datas:
            retval.append(Data(data.km / kmmax, data.price / pricemax))
        return retval

    def main(self, ac, av):
        if ac != 2:
            sys.exit("usage: python3 ft_linear_regression_train `data to train on`")
        data = self.parsing(av[1])
        tetha0, tetha1,_,_ = self.getTetha()
        kmmax, pricemax = self.getMax(data)
    #display(data)
        data = self.normalizeData(data, kmmax, pricemax)
        for i in range(10000):
            self.calculateTetha(data)
        self.saveTetha(self.tetha0, self.tetha1, kmmax, pricemax)

if __name__ == "__main__":
    reg = Regression()
    reg.main(len(sys.argv), sys.argv)

