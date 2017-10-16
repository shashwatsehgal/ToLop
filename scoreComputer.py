# Class to compute suspician score of an an item.
import math

class ScoreComputer:
    # TODO: Use an abstract class ScoreComputer with different speciailizations
    # corresponding to different platforms (eBay, Craigslist, etc.).
    def __init__(self, listPrice):
        # TODO: Read this values from a config file.
        self.listPrice = listPrice

    def getScore(item):
        return __getPriceScore(item.price, item.shippingCost, self.listPrice) * __getDistanceScore(item.distance)

    def __getPriceScore(sellingPrice, shippingCost, listPrice):
        discount = listPrice - sellingPrice - shippingCost
        if discount < 0:
            return 0
        sigma = listPrice / 10;
        return 1 - math.exp(- discount * discount / (2 * sigma * sigma)) / (sigma * 0.3989)

    def __getDistanceScore(distance):
        return 1 / (1 + math.exp(distance - 500))

