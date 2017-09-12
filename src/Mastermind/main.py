#ampy -p COM3 put test01.py /main.py
import numpy as np

def compare(a, b):
    corrects = 0;
    semiCorrects = 0;
    x = 0
    while(x < a.size):
        if (a[x] == b[x]):
            a = np.delete(a,x)
            b = np.delete(b,x)
            corrects += 1
            x = x-1
        x += 1

    x = 0
    y = 0
    while(x < a.size):
        y = 0
        while (y < b.size):
            if(a[x] == b[y]):
                a = np.delete(a, x)
                b = np.delete(b, y)
                semiCorrects += 1
                x -= 1
                break
            y += 1
        x += 1

    return(corrects,semiCorrects)

def getSimilarArrays(arr, index, result):
    k = arr[index]
    arr = np.delete(arr,index, axis = 0)
    x = 0
    while (x < arr.size / 4):
        #print(arr[x])
        #print(k)
        sol = compare(arr[x], k)
        #print("compare", sol, " and ", result)
        if (sol != result):
            arr = np.delete(arr, x, axis = 0)
            x -= 1
        x += 1
    return arr;

tries = 0

def solveMastermind(arr, solution):
    global tries

    #index = (arr.size//8//6) #avg case 4.770833333333333 worst 7
    #index = 0 #avg case 5.764660493827161 worst 9 lexikographic
    #index = arr.size//8 #avg case 4.911265432098766 worst 9
    #index = arr.size//12 #avg case 4.817901234567901 worst 7
    #index = (arr.size//8//6)-1 #avg case 4.641203703703703 worst 7
    #index = (arr.size // 13) #avg case 4.636574074074074 worst 7
    #index = (int)(arr.size //4 //3.14159265359) #avg case = 4.677469135802469
    #index = (arr.size // 13)-1 #avg case 4.589506172839506
    index = (int)(pow(arr.size//4,0.5))-1 #avg case 4.582561728395062

    #try to always get XXYY #avg case 4.753086419753086 worst 8
    '''index = arr.size//8//6
    for x in range(0, arr.size//4):
        testArr = np.array([0, 0, 0, 0, 0, 0])
        for y in range(0,4):
            testArr[(int)(arr[x][y])] += 1
        count = 0
        for k in range(0,6):
            if(testArr[k] == 2):
                count+=1
        if(count == 2):
            index = x
            break'''


    touple = compare(arr[index],solution)
    #print("Tried ", arr[index] ," and got ",touple[0], "hits and ", touple[1], " correct colors.")

    arr = getSimilarArrays(arr,index, touple)


    #print("__________________________")
    if(arr.size == 0):
       # print("solved in ", tries+1, " tries")
        return
    tries += 1
    solveMastermind(arr,solution)

def getFilledArray():
    arr = np.array([])

    for x in range(0, 6):
        for y in range(0, 6):
            for z in range(0, 6):
                for j in range(0, 6):
                    arr = np.append(arr, x)
                    arr = np.append(arr, y)
                    arr = np.append(arr, z)
                    arr = np.append(arr, j)
    arr = np.reshape(arr, (arr.size//4,4))
    return arr

def getAverageCase():
    global tries
    tester = getFilledArray()
    value = 0
    worstValue = 0
    index = 0

    for x in range(0, 6):
        for y in range(0, 6):
            for z in range(0, 6):
                for j in range(0, 6):
                    tries = 0
                    arr = np.array([x,y,z,j])
                    solveMastermind(tester,arr)
                    print(index)
                    value += tries+1;
                    if(tries + 1 > worstValue ):
                        worstValue = tries+1
                    index += 1
    print("Average Case = ", value/index)
    print("Worst case = ", worstValue)

a = np.array([3,5,4,2])
b = np.array([0,1,0,3])

#print(compare(a,b))


#solveMastermind(getFilledArray(),a)

getAverageCase()

