import numpy as np
from sympy import *


def mul(lst):
    result = 1
    for item in lst:
        result *= item
    return result


def lagrange(x_list, y_list, x_target):
    x_list = np.array(x_list, dtype=float)
    y_list = np.array(y_list, dtype=float)
    x_target = float(x_target)
    result = 0.0
    for i in range(len(x_list)):
        x0 = x_list[i]
        y0 = y_list[i]
        if i == 0:
            upper = mul(x_target - x_list[1:])
            downer = mul(x0 - x_list[1:])
            result += upper / downer * y0
        elif i == len(x_list) - 1:
            upper = mul(x_target - x_list[:-1])
            downer = mul(x0 - x_list[:-1])
            result += upper / downer * y0
        else:
            upper = mul(x_target - np.concatenate((x_list[:i], x_list[i + 1:])))
            downer = mul(x0 - np.concatenate((x_list[:i], x_list[i + 1:])))
            result += upper / downer * y0
    return result


def newton(x_list, y_list, x_target):
    """列表形式参数,类型全部换成float"""
    x_list = list(map(float, x_list))
    y_list = list(map(float, y_list))
    x_target = float(x_target)
    number = len(x_list)
    k = number - 1
    diff_quotient = [y_list]
    parameters = [y_list[0]]
    for i in range(1, k + 1):  # 从一阶差商开始一直到k阶差商
        last_quotient = diff_quotient[i - 1]
        tmp_quotient = []
        for j in range(0, len(last_quotient) - 1):  # 遍历上一层差商的数值
            a = last_quotient[j]
            b = last_quotient[j + 1]
            """这里的索引需要仔细推敲"""
            tmp_quotient.append((b - a) / (x_list[j + i] - x_list[j]))
        diff_quotient.append(tmp_quotient)
        parameters.append(tmp_quotient[0])

    acumen_pro = 1.0
    result = 0.0
    for i in range(number):
        result += acumen_pro * parameters[i]
        acumen_pro *= (x_target - x_list[i])

    return result


def init(size):
    j = 0
    data = []
    while j < size:
        data.append(0)
        j += 1
    return data


def calcEquationPara(x):
    parameter = []
    size_of_interval = len(x) - 1
    i = 1
    while i < len(x) - 1:
        data = init(size_of_interval * 4)
        data[(i - 1) * 4] = x[i] * x[i] * x[i]
        data[(i - 1) * 4 + 1] = x[i] * x[i]
        data[(i - 1) * 4 + 2] = x[i]
        data[(i - 1) * 4 + 3] = 1
        data1 = init(size_of_interval * 4)
        data1[i * 4] = x[i] * x[i] * x[i]
        data1[i * 4 + 1] = x[i] * x[i]
        data1[i * 4 + 2] = x[i]
        data1[i * 4 + 3] = 1
        temp = data[2:]
        parameter.append(temp)
        temp = data1[2:]
        parameter.append(temp)
        i += 1
    data = init(size_of_interval * 4 - 2)
    data[0] = x[0]
    data[1] = 1
    parameter.append(data)
    data = init(size_of_interval * 4)
    data[(size_of_interval - 1) * 4] = x[-1] * x[-1] * x[-1]
    data[(size_of_interval - 1) * 4 + 1] = x[-1] * x[-1]
    data[(size_of_interval - 1) * 4 + 2] = x[-1]
    data[(size_of_interval - 1) * 4 + 3] = 1
    tmp = data[2:]
    parameter.append(tmp)
    i = 1
    while i < size_of_interval:
        data = init(size_of_interval * 4)
        data[(i - 1) * 4] = 3 * x[i] * x[i]
        data[(i - 1) * 4 + 1] = 2 * x[i]
        data[(i - 1) * 4 + 2] = 1
        data[i * 4] = -3 * x[i] * x[i]
        data[i * 4 + 1] = -2 * x[i]
        data[i * 4 + 2] = -1
        temp = data[2:]
        parameter.append(temp)
        i += 1
    # 端点函数二阶导数值相等为n-1个方程。加上前面的方程为4n-2个方程。且端点处的函数值的二阶导数为零，为两个方程。总共为4n个方程。
    i = 1
    while i < len(x) - 1:
        data = init(size_of_interval * 4)
        data[(i - 1) * 4] = 6 * x[i]
        data[(i - 1) * 4 + 1] = 2
        data[i * 4] = -6 * x[i]
        data[i * 4 + 1] = -2
        temp = data[2:]
        parameter.append(temp)
        i += 1
    return parameter


def solutionOfEquation(x_list, y_list):
    size_of_interval = len(x_list) - 1
    result = init(size_of_interval*4-2)
    i = 1
    while i < size_of_interval:
        result[(i-1)*2] = y_list[i]
        result[(i-1)*2+1] = y_list[i]
        i += 1
    result[(size_of_interval-1)*2] = y_list[0]
    result[(size_of_interval-1)*2+1] = y_list[-1]
    a = np.array(calcEquationPara(x_list))
    b = np.array(result)
    """for data_x in b:
        print(data_x)"""
    return np.linalg.solve(a, b)


def calculate(parameters, x):
    result = []
    for data_x in x:
        result.append(parameters[0] * data_x * data_x * data_x + parameters[1] * data_x * data_x + parameters[2] * data_x + parameters[3])
    return result


def cubic(x_list, y_list, x_target):
    x_list = list(map(float, x_list))
    y_list = list(map(float, y_list))
    x_target = float(x_target)
    parameters = solutionOfEquation(x_list, y_list)
    k = 0
    result = 0
    X_range = []
    Y_res = []
    for i in range(len(x_list) - 1):
        x_range = np.arange(x_list[i], x_list[i+1], (x_list[i+1] - x_list[i])/1000)
        x_para = []
        if i == 0:
            x_para.extend([0, 0, parameters[k], parameters[k+1]])
            k += 2
        else:
            x_para.extend([parameters[k], parameters[k+1], parameters[k+2], parameters[k+3]])
            k += 4
        if x_list[i] < x_target < x_list[i + 1]:
            result = x_para[0] * (x_target ** 3) + x_para[1] * (x_target ** 2) + x_para[2] * x_target + x_para[3]
        y_res = calculate(x_para, x_range)
        X_range.extend(x_range)
        Y_res.extend(y_res)
        i += 1
    return result, X_range, Y_res


if __name__ == "__main__":
    xlist = [3, 4.5, 7, 9, 9.5]
    ylist = [2.5, 1, 2.5, 0.5, -5]
    target = 9.3
    #print(newton(xlist, ylist, target))
    #print(lagrange(xlist, ylist, target))
    #res, _x, _y = cubic(xlist, ylist, target)
    #print(_x)
    #print(_y)

