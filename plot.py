import matplotlib.pyplot as plt
import numpy as np
import os
from interpolation import *

from frozen_dir import app_path

def plot_and_save(x, y, target_x, result, method, times):
    x = np.array(x, dtype=float)
    x = np.append(x, target_x)
    min_x = x[np.argmin(x)]
    max_x = x[np.argmax(x)]
    x = np.delete(x, len(x)-1)
    y = np.array(y, dtype=float)
    target_x = float(target_x)
    result = float(result)
    plt.figure()
    plt.scatter(x, y, c='r', marker='o', s=20, label='Original')
    plt.scatter(target_x, result, c='b', marker='x', s=30, label='Target')
    x_line = np.arange(min_x, max_x, (max_x - min_x) / 1000)
    y_line = np.zeros(len(x_line))
    if method == "Newton":
        plt.title("Inerpolation-Newton")
        for i in range(len(x_line)):
            y_line[i] = newton(list(x), list(y), float(x_line[i]))
    elif method == "Lagrange":
        plt.title("Inerpolation-Lagrange")
        for i in range(len(x_line)):
            y_line[i] = lagrange(list(x), list(y), float(x_line[i]))
    plt.plot(x_line, y_line, c='g', label='Line')
    plt.legend()
    if not os.path.exists(os.path.join(app_path(), "tmpresults")):
        os.mkdir(os.path.join(app_path(), "tmpresults"))
    plt.savefig(os.path.join(app_path(), "tmpresults\\" + str(times) + ".png"), bbox_inches='tight')
    plt.show()


def plot_and_save_forCubic(x, y, target_x, result, X_range, Y_res, times):
    plt.figure()
    plt.scatter(x, y, c='r', marker='o', s=20, label='Original')
    plt.scatter(target_x, result, c='b', marker='x', s=30, label='Target')
    plt.plot(X_range, Y_res, c='g', label='line')
    plt.legend()
    plt.title("Inerpolation-Cubic")
    if not os.path.exists(os.path.join(app_path(), "tmpresults")):
        os.mkdir(os.path.join(app_path(), "tmpresults"))
    plt.savefig(os.path.join(app_path(), "tmpresults\\" + str(times) + ".png"), bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    x = [1, 4, 9]
    y = [1, 2, 3]
    target = 7
    result = 2.7
    method = "Lagrange"
    plot_and_save(x, y, target, result, method, 1)

