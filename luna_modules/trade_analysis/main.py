import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    trades_path = "../../trades/"
    file_name = "MIRUSDT_2021-04-19_11.00.00.json"
    with open(trades_path+file_name, 'r') as fp:
        json_data = json.load(fp)
    x_axis = []
    y_axis = []
    start_time = json_data[0]['T']
    for data in json_data:
        x_axis.append((data['T']-start_time)/1000)
        y_axis.append(float(data['p']))
    plt.plot(x_axis, y_axis)
    plt.xlabel("seconds")
    plt.ylabel("price")
    plt.savefig(trades_path+file_name.replace(".json", ".png"))
