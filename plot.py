import numpy
import matplotlib.pyplot as plt


def plot(data):

    for guide in data.keys():

        if "gmm" in data[guide]:
            gmm = data[guide]["gmm"]
            print(gmm)
