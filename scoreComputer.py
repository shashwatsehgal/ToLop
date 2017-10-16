# Class to compute suspician score of an an item.
import math

class ScoreComputer:
    # TODO: Use an abstract class ScoreComputer with different speciailizations
    # corresponding to different platforms (eBay, Craigslist, etc.).
    def __init__(self, listPrice):
        # TODO: Read these values from a config file.
        self.listPrice = listPrice

    def getScore(self, item):
        print(item.distance)
        return self.__getPriceScore(item.price, item.shippingCost,
                self.listPrice) * self.__getDistanceScore(item.distance)

    def __getPriceScore(self, sellingPrice, shippingCost, listPrice):
        discount = listPrice - sellingPrice - shippingCost
        if discount < 0:
            return 0
        sigma = listPrice / 10;
        return 1 - math.exp(- discount * discount / (2 * sigma * sigma)) / (sigma * 2.506628)

    def __getDistanceScore(self, distance):
        try:
            return 1 / (1 + math.exp(distance - 1000))
        except OverflowError:
            return 0

