import math,numpy as np, matplotlib.pyplot as plt

np.set_printoptions(precision = 2)
x = np.array([52,33,30,29,55,44,41,43,68,55,55,67,55,57,52,34,29,30,28,28,41,50,49,44,52,79,68,83,107,105])
# x = np.array([737,775,792,787,835,887,810,832,855,878,884,913,941,959,939,957,983,1000,1002,996
# ,993,1007,1003,1030,1055,1077,1040,1280,1090,1150])
print "Среднее временного ряда: ", np.mean(x)
print "Дисперсия временного ряда: ", np.var(x)

def linearPrediction(a0,a1,alpha):
    p1= np.array([])
    size = len(x)
    betta = 1 - alpha
    s0 = a0 - (betta/alpha)* a1
    p1= np.append(p1,s0)
    for i in range(size):
        s = alpha * x[i] + (betta)*p1[-1]
        p1= np.append(p1,s)
    p2 = np.array([])
    s0 = a0 - (2*betta/alpha)*a1
    p2 = np.append(p2,s0)
    for i in range(size):
        s = alpha*x[i] + betta * p2[-1]
        p2 = np.append(p2,s)
    print "График при однократном сглаживании сглаженных значений линейной модели при alpha = ",alpha,":"
    fig1,ax1 = plt.subplots()
    ax1.plot([i for i in range(size + 1)],p1)
    plt.show()
    print "График при двойном сглаживании сглаженных значений линейной модели при alpha = ",alpha,":"       
    fig2,ax2 = plt.subplots()
    ax2.plot([i for i in range(size + 1)],p2)
    plt.show()

def constPrediction(x,alpha):
    p = np.array([])
    size = len(x)
    betta = 1 - alpha
    s0 = np.mean(x[:5])
    p= np.append(p,s0)
    for i in range(size):
        s = alpha * x[i] + (betta) * p[-1]
        p= np.append(p,s)
    print "График сглаженных значений для постоянной модели при alpha = ",alpha,":"
    fig,ax = plt.subplots()
    ax.plot([i for i in range(size + 1)],p)
    plt.show()
    print "Ошибка предсказания для альфа = ",alpha, ":\n", np.array([a - b for (a,b) in zip(x,p)]),"\n"  
    print "Выборочная дисперсия для ошибки предсказания: ", np.var(p),"\n"

def linearRegr(values):
    y = values
    n = len(y)
    x = [i for i in range(n)]
    a1 = float(n * np.dot(x,np.transpose(y)) - sum(x) * sum(y))/(n*sum([i**2 for i in x]) - (sum(x))**2)
    a0 = float(sum(y) - a1*sum(x))/n
    y2 = [a0 + a1*i for i in x]
    ax1.plot(x,y2)
    print "График временного ряда и линейной модели(МНК):"
    return a0,a1

def prediction(a0,a1,alpha,m):
    size = len(x)
    betta = 1 - alpha
    a01 = np.array([])
    a11 = np.array([])
    a01 = np.append(a01,x[0] + betta**2*(a1 + a0 - x[0]))
    a11 = np.append(a11,a1 + alpha**2*(a1+a0-x[0]))
    for i in range(1,size):
        sums = a01[-1] + a11[-1] - x[i]
        a01 = np.append(a01,x[i] + betta**2*sums) 
        a11 = np.append(a11,a11[-1] + alpha**2*sums)
    xt = np.array([])
    for i in range(size):
        xt = np.append(xt,a01[i] + a11[i])
    error = np.array([])
    for i in range(m,size):
        error = np.append(error,x[i] - xt[i])
    print "Предсказанные значение Xt для alpha = ",alpha,"и m = ",m,":\n"
    for i in range(1,m+1):
        print "Xt[",size + i,"] = ", xt[-(m+1-i)]
    print "Ошибки предсказания на каждом шаге:\n", error,"\n"
    print "Выборочная дисперсия ошибки предсказания: ", np.var(error),"\n"
    print "График прогнозирования при alpha = ", alpha, "и m = ",m,":"
    fig,ax = plt.subplots()
    ax.plot([i + m for i in range(size)],xt)
    plt.show()

def getPolynominalDegree():
    r = x
    size = len(x)
    means = np.array([])
    for j in range(size - 1):
        r = [r[i] - r[i-1] for i in range(1,size - j)]
        means = np.append(means,abs(np.mean(r)))
#     print means
#     print np.amin(means)
    return np.argmin(means) - 1

fig1,ax1 = plt.subplots()
ax1.plot([i for i in range(len(x))],x)
coeffs = linearRegr(x)
plt.show()
print "Коэффициент А0 и А1 линейной регрессии: ",coeffs[0],coeffs[1],"\n"
constPrediction(x,0.1)
constPrediction(x,0.3)
linearPrediction(coeffs[0],coeffs[1],0.1)
linearPrediction(coeffs[0],coeffs[1],0.3)
prediction(coeffs[0],coeffs[1],0.1,1)
prediction(coeffs[0],coeffs[1],0.1,5)
prediction(coeffs[0],coeffs[1],0.3,1)
prediction(coeffs[0],coeffs[1],0.3,5)
print "Рекомендуемый порядок полинома: ",getPolynominalDegree()