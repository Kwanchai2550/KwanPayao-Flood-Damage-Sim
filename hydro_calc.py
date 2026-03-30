import numpy as np

def hQ_Calc(Para1, Para2, H):
    return max(0.0, Para1 * (H - Para2))

def params_dat():
    return [0.024,0.056,0.000012,0.0523,0.0000223,0.0077,0.0297,1.00072,
            75.0,0.31,0.01626,0.00126,5.0,0.01,6.5,17.734, 1.1]

def run_tank_simulation(params, rain, basin_area):
    n = len(rain)
    calc_matrix = np.zeros((n, 12))
    calc_matrix[0, 2], calc_matrix[0, 5], calc_matrix[0, 8], calc_matrix[0, 11] = params[12:16]

    for k in range(n):
        if k > 0:
            calc_matrix[k, 2]  = (rain[k-1] * params[16]) + calc_matrix[k-1, 2] - sum(calc_matrix[k-1, [0,1,3]])
            calc_matrix[k, 5]  = calc_matrix[k-1, 5] + calc_matrix[k-1, 3] - sum(calc_matrix[k-1, [4,6]])
            calc_matrix[k, 8]  = calc_matrix[k-1, 8] + calc_matrix[k-1, 6] - sum(calc_matrix[k-1, [7,9]])
            calc_matrix[k, 11] = calc_matrix[k-1, 11] + calc_matrix[k-1, 9] - calc_matrix[k-1, 10]

        calc_matrix[k, 0] = hQ_Calc(params[0], params[8],  calc_matrix[k, 2])
        calc_matrix[k, 1] = hQ_Calc(params[2], params[9],  calc_matrix[k, 2])
        calc_matrix[k, 3] = hQ_Calc(params[1], 0.0,        calc_matrix[k, 2])
        calc_matrix[k, 4] = hQ_Calc(params[4], params[10], calc_matrix[k, 5])
        calc_matrix[k, 6] = hQ_Calc(params[3], 0.0,        calc_matrix[k, 5])
        calc_matrix[k, 7] = hQ_Calc(params[6], params[11], calc_matrix[k, 8])
        calc_matrix[k, 9] = hQ_Calc(params[5], 0.0,        calc_matrix[k, 8])
        calc_matrix[k, 10]= hQ_Calc(params[7], 0.0,        calc_matrix[k, 11])
        
    q_sum = calc_matrix[:, 0] + calc_matrix[:, 1] + calc_matrix[:, 4] + calc_matrix[:, 7]
    return (q_sum * (basin_area * 1000.0)) / 3600.0