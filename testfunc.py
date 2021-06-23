import numpy as np
def z( x, y):
    # Calculo do valor da função de Akley
    primeiro_termo = np.exp(-0.2 * np.sqrt(0.5*(np.float_power(x, 2) + np.float_power(y, 2))))
    segundo_termo = np.exp(0.5 * (np.cos(2*np.pi*x)+np.cos(2*np.pi*y)))
    var = -20 * primeiro_termo - segundo_termo + np.exp(1) + 20
    return var


print("maior",str(z(-1.0,-1.0)))
print("menor",str(z(-0.5,-1.0)))
print("menor",str(z(0,0)))