import sys
import io
import re
import math

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

def prixEstime(kilometrage, tetha0, tetha1):
    value = tetha0 + (tetha1 * kilometrage)
    return value

def main(ac, av):
    if ac != 2:
        sys.exit("usage: python3 ft_linear_regression `kilometrage`")
    try:
        kilometrage = int(av[1])
    except Exception as e:
        sys.exit("Couldn't read a number from argument given")
    tetha0, tetha1,kmscale, pricescale = getTetha()
    value = prixEstime(kilometrage, tetha0, tetha1)
    print(value)


if __name__ == "__main__":
        main(len(sys.argv), sys.argv)
