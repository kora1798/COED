import numpy as np, pandas as pd, math

def getDataFile():
    filename = "example.xls"
    return pd.read_excel(filename)

def improveDataFileForAccuracy(datafile):
    values = datafile.values
    m = np.size(values,0) 
    n = np.size(values,1)
    p = []
    for i in range (0,m):
        for j in range(0,n):
            if isinstance(values[i,j], basestring) or np.isnan(values[i,j]):
                p.append(i)
                break
    datafile = np.delete(values, p, axis = 0)
    datafile = datafile[:,51:61]
    return datafile
        
def getMeanOfColumn(index):
    rowscount = np.size(df, 0)
    sum = 0
    for i in range(0,rowscount):
        sum = df[i, index] + sum
    return sum/rowscount

def getDispersionOfColumn(index):
    mean = getMeanOfColumn(index)   
    sumOfSq = 0
    rowscount = np.size(df,0)
    for i in range(0, rowscount):
        sumOfSq = math.pow(df[i,index] - mean,2) + sumOfSq
    return sumOfSq/rowscount

def getDataFrame():
    datafile = getDataFile()
    datafile = improveDataFileForAccuracy(datafile)
    return datafile

def getStandardMatrix():
    rowscount = np.size(df,0)
    columnscount = np.size(df,1)
    standardMatrix = np.zeros((rowscount,columnscount))
    for i in range(0,columnscount):
        for j in range(0,rowscount):
            standardMatrix[j,i] = (df[j,i] - getMeanOfColumn(i))/math.sqrt(getDispersionOfColumn(i))
    return standardMatrix

def getCovMatrix():
    rowscount = np.size(df,0)
    columnscount = np.size(df,1)
    covMatrix = np.zeros((columnscount,columnscount))
    for i in range(0,columnscount):
        for j in range(0,columnscount):
            value = 0
            for k in range(0, rowscount):
                value = value + (df[k,i] - getMeanOfColumn(i))*(df[k,j] - getMeanOfColumn(j))
            covMatrix[i,j] = value/rowscount
    return covMatrix
    
def getCorrMatrix():
    rowscount = np.size(df,0)
    columnscount = np.size(df,1)
    corrMatrix = np.zeros((columnscount,columnscount))
    standardMatrix = getStandardMatrix()
    for i in range(0, columnscount):
        for j in range(0,columnscount):
            value = 0
            for k in range(0,rowscount):
                value = standardMatrix[k,i]*standardMatrix[k,j] + value
            corrMatrix[i,j] = value/rowscount
    return corrMatrix

def printMatrixOfAnalyzeHypothesisOfCorr():
    columnscount = np.size(df,1)
    corrMatrix = getCorrMatrix()
    matrixOfStatistics = np.zeros((columnscount, columnscount))
    for i in range(0, columnscount):
        for j in range(0, columnscount):
            r = corrMatrix[i,j]
            if i != j:
                t =  (r*math.sqrt(columnscount - 2))/math.sqrt(1 - math.pow(r,2))
                if abs(t) >= 2.228:
                    matrixOfStatistics[i,j] = True
                else: 
                    matrixOfStatistics[i,j] = False
    print matrixOfStatistics
    
def printMeans():
    p = []
    columnscount = np.size(df,1)
    print "Средние значения по столбцам: "
    for i in range(0, columnscount):
        print "%.2f" % (getMeanOfColumn(i)),
    print
    
def printDispersions():
    p = []
    columnscount = np.size(df,1)
    print "Значения дисперсий по столбцам: "
    for i in range(0,columnscount):
        print "%.2f" % (getDispersionOfColumn(i)),
    print

def printStandardMatrix():
    print "Стандартизованная матрица: "
    standardMatrix = getStandardMatrix()
    np.set_printoptions(precision = 3, suppress = True)
    print standardMatrix
    
def printCovMatrix():
    covMatrix = getCovMatrix()
    print "Ковариационная матрица: "
    np.set_printoptions(formatter={'float': '{:0.2f}'.format})
    print covMatrix
    
def printCorrMatrix():
    corrMatrix = getCorrMatrix()
    print "Корреляционная матрица: "
    np.set_printoptions(precision = 3, suppress = True)
    print corrMatrix
    
df = getDataFrame() 
printMeans()
printDispersions()
printStandardMatrix()
printCovMatrix()
printCorrMatrix()
printMatrixOfAnalyzeHypothesisOfCorr()