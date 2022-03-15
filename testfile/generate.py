
import numpy as np
import pandas as pd



def generate():
    np.random.seed(1)
    for i in range(5):
        x_range = np.random.rand(20)
        x_range *= 10
        if i == 0:
            y_range = x_range ** 2
        elif i == 1:
            y_range = x_range ** 3
        elif i == 2:
            y_range = np.sin(x_range)
        elif i == 3:
            y_range = np.exp(x_range)
        elif i == 4:
            y_range = np.log(x_range)
        data = np.hstack((x_range.reshape(20, 1), y_range.reshape(20, 1)))
        frame = pd.DataFrame(data=data, columns=["x", 'y'])
        frame.to_csv("test"+str(i+1)+'.csv', header=False, index=False)
    return


if __name__ == "__main__":
    generate()