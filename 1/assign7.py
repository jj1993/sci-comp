import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import minimize
import math
import pandas # for printing
import copy

# Set up parameters
N = 70
coordinates = [(x,y+1) for x in range(N+1) for y in range(N-1)]
Cons, delta_xy = 1/4.0, 1/float(N)
maxiters = 2000
epsilon = 0.0001 # Break-off value for convergence
omega = 1.7 # For SOR algoritm

def newMatrix():
    # Build empty matrix
    M = np.zeros((N+1,N+1))
    for n in range(N+1):
        M[n,0] = 0
        M[n,N] = 1
    return M

def analytic(y):
    return y*delta_xy

def Jacobi(M, epsilon, x1=0, x2=0, y1=0, y2=0):
    k = 0
    newM = copy.deepcopy(M)
    while (k < maxiters):
        k += 1

        for x, y in coordinates:
            if x in np.arange(x1, x2) and y in np.arange(y1,y2):
                continue
            newM[x,y] = Cons*(
                M[x-1,y] + M[(x+1)%N,y] + M[x,y-1] + M[x,y+1]
                )

        # Determine if system is converged
        difference = abs(M - newM)
        for x, y in coordinates:
            delta = difference[x,y]
            if delta > epsilon:
                break
        else:
            # obscure python code -> for-else statement,
            # fires else when break is not fired
            print("Jacobi terminated in iteration ",k)
            break

        M = copy.deepcopy(newM)

    return M, k

def GaussSeidel(M, epsilon, x1=0, x2=0, y1=0, y2=0):
    k  = 0
    while (k < maxiters):
        c = 0
        k += 1

        for x, y in coordinates:
            if x in np.arange(x1, x2) and y in np.arange(y1,y2):
                continue
            newValue = Cons*(M[x-1,y] + M[(x+1)%N,y] + M[x,y-1] + M[x,y+1])
            delta = abs(newValue - M[x,y])
            M[x,y] = newValue

        # Determine if system is converged
            if delta > epsilon:
                c += 1
        if c == 0:
            print("Gauss-Seidel terminated in iteration ",k) #add timer?
            break

    return M, k

def SOR(M, epsilon, omega, x1=0, x2=0, y1=0, y2=0):
    k  = 0
    while (k < maxiters):
        c = 0
        k += 1

        for x, y in coordinates:
            if x in np.arange(x1, x2) and y in np.arange(y1,y2):
                continue
            newValue = omega/4.0*(M[x-1,y] + M[(x+1)%N,y] + M[x,y-1] + M[x,y+1]) \
                            + (1 - omega)*M[x,y]
            delta = abs(newValue - M[x,y])
            M[x,y] = newValue

            # Determine if system is converged
            if delta > epsilon:
                c += 1

        if c == 0:
            print("SOR terminated in iteration ",k) #add timer?
            break

    return M, k


if __name__ == "__main__":
    # # Question G
    # JacobiSolution = Jacobi(newMatrix(), epsilon)[0]
    # GaussSeidelSolution = GaussSeidel(newMatrix(), epsilon)[0]
    # SORSolution = SOR(newMatrix(), epsilon, omega)[0]
    # analyticSolution = [analytic(y) for y in range(N+1)]
    #
    # plt.plot(JacobiSolution[0])
    # plt.plot(GaussSeidelSolution[0])
    # plt.plot(SORSolution[0])
    # plt.plot(analyticSolution)
    # plt.legend(['Jacobi','Gauss-Seidel','SOR','Analytic solution'])
    # plt.xlabel('y value')
    # plt.ylabel('solution value')
    # plt.show()

    # # Question H
    # epsilons = [10**-(i+1) for i in range(8)]
    # J, G, S1, S2 = [], [], [], []
    # for epsilon in epsilons:
    #     print("================")
    #     print("Epsilon = ",epsilon)
    #     print("================")
    #     J.append(Jacobi(newMatrix(), epsilon)[1])
    #     G.append(GaussSeidel(newMatrix(), epsilon)[1])
    #     S1.append(SOR(newMatrix(), epsilon, 1.4)[1])
    #     S2.append(SOR(newMatrix(), epsilon, 1.7)[1])
    #
    # plt.loglog(epsilons, J)
    # plt.loglog(epsilons, G)
    # plt.loglog(epsilons, S1)
    # plt.loglog(epsilons, S2)
    # plt.xlim(epsilons[0], epsilons[-1])
    # plt.legend(['Jacobi','Gauss-Seidel','SOR, $\omega = 1.4$','SOR, $\omega = 1.7$'])
    # plt.xlabel('$\epsilon$ -value')
    # plt.ylabel('number of iterations')
    # plt.show()

    # # Question I
    # def minSOR(omega):
    #     print(omega)
    #     M = newMatrix()
    #     k = SOR(M, 0.001, omega[0])[1]
    #     return k
    #
    # results = []
    # sizes = [50, 60, 70, 80, 100]
    # for N in sizes:
    #     coordinates = [(x,y+1) for x in range(N+1) for y in range(N-1)]
    #     Cons, delta_xy = 1/4.0, 1/float(N)
    #     res = minimize(minSOR, 1.8, method='nelder-mead')
    #     optimalOmega = res.x
    #     results.append(optimalOmega)
    #
    # plt.plot(sizes,results)
    # plt.xlabel('Grid size N')
    # plt.ylabel('Optimal $\omega$-value')
    # plt.show()

    # Question J
    # fig, axarr = plt.subplots(ncols=3, nrows=1)
    #
    # JacobiSolution = Jacobi(newMatrix(), epsilon)[0]
    # GaussSeidelSolution = GaussSeidel(newMatrix(), epsilon)[0]
    # SORSolution = SOR(newMatrix(), epsilon, omega)[0]
    #
    # axarr[0].matshow(JacobiSolution)
    # axarr[0].set_title('Jacobi Solution', fontsize=20)
    # axarr[0].xaxis.set_ticks_position('bottom')
    # axarr[1].matshow(GaussSeidelSolution)
    # axarr[1].set_title('Gauss-Seidel Solution', fontsize=20)
    # axarr[1].xaxis.set_ticks_position('bottom')
    # axarr[2].matshow(SORSolution)
    # axarr[2].set_title('SOR Solution', fontsize=20)
    # axarr[2].xaxis.set_ticks_position('bottom')
    #
    # axarr[0].set_ylabel("y value", fontsize=20)
    # axarr[0].set_xlabel("x value", fontsize=20)
    # axarr[1].set_xlabel("x value", fontsize=20)
    # axarr[2].set_xlabel("x value", fontsize=20)
    # # changing tick labels etc.
    # plt.setp([a.get_yticklabels() for i,a in enumerate(axarr) if i==1 or i==2], visible=False)
    # plt.setp([a.get_yticklabels() for i,a in enumerate(axarr) if i==0], fontsize=20)
    # plt.setp([a.get_xticklabels() for a in axarr], fontsize=20)
    # plt.show()

    #generation of image for website

    fig, axarr = plt.subplots()

    SORSolution = SOR(newMatrix(), epsilon, omega)[0]
    axarr.matshow(SORSolution)
    plt.show()
    # def minBoxSOR(omega):
    #     print(omega)
    #     M = newMatrix()
    #     k = SOR(M, 0.0001, omega[0], 40,45,40,45)[1]
    #     return k
    #
    # def minSOR(omega):
    #     print(omega)
    #     M = newMatrix()
    #     k = SOR(M, 0.0001, omega[0])[1]
    #     return k
    #
    # Cons, delta_xy = 1/4.0, 1/float(N)
    # resBox = minimize(minBoxSOR, 1.8, method='nelder-mead')
    # res = minimize(minSOR, 1.8, method='nelder-mead')
    # optimalOmega = res.x
    # optimalOmegaBox = res.x
    #
    # print("opt. omega: ",optimalOmega)
    # print("opt. omega box: ",optimalOmegaBox)
