import json
import matplotlib.pyplot as plt


class TradeAnalyzer:
    def __init__(self, file):
        self.data = self.parse_file(file)
        self.__x_axis = []
        self.__y_axis = []

    def parse_file(self, file):
        with open(file, 'r') as fp:
            return json.load(fp)

    def draw(self, second_interval):
        start_time = self.data[0]['T']
        for data in self.data:
            seconds = (data['T'] - start_time)
            self.__x_axis.append(data['T'] - start_time)
            self.__y_axis.append(float(data['p']))
            if seconds >= second_interval:
                break
        plt.plot(self.__x_axis, self.__y_axis)
        plt.xlabel("miliseconds")
        plt.ylabel("price")

    def save_graph(self, path):
        plt.savefig(path)

    def show(self):
        plt.show()
