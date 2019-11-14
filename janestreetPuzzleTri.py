import math 
import re

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class tri(object):
    area = -1
    legs = []
    orientationIndex = -1
    legIndex = -1
    coordinate = ()
#global variables
fittedTriangles = Stack()
trianglesToFix = Stack()
currentTri = tri()
prevTri = tri()
def customPrint(arr) :
    for row in arr: 
        print([re.sub(r"^0"," ",str(i).zfill(2)) for i  in row])
        print("\n")

def getLegs(n) : 
    i = 1
    divisors = []
    while i <= math.sqrt(n): 
        if (n % i == 0) : 
            if (n / i == i) : 
                divisors.append(i) 
                divisors.append(i)
            else : 
                # Otherwise print both 
                divisors.append(i)
                divisors.append(n/i)
        i = i + 1
    divisors.remove(1)
    divisors.remove(n)
    return divisors

def getTriangles(arr):
    areaList = []
    triList = []
    coordinateList = []
    for i in range(0,17):
        for j in range(0,17):
            if arr[i][j] > 0:
                areaList.append(arr[i][j])
                coordinateList.append(tuple((i, j)))
    triList = sortTriangles(areaList, coordinateList)
    for triangle in triList:
        triLegs = sortLegs(arr, triangle[0], triangle[1])
        leg = triLegs[0]
        currentTri.area = triangle[0]
        currentTri.coordinate = triangle[1]
        currentTri.legs = triLegs
        currentTri.legIndex = 0
        currentTri.orientationIndex = 0
        triedFit = fitTriangleHelper(arr, leg[1],currentTri.coordinate,currentTri.area, currentTri.orientationIndex)
        if triedFit == False:
            # could not fit using legs provided in any orientation, need to try other leg combos
            for i in range (1, len(triLegs)):
                leg = triLegs[i]
                print("trying different leg combos")
                triedFit = fitTriangleHelper(arr, leg[1],currentTri.coordinate,currentTri.area, 0)
            if triedFit == False:
                #could not fit using any legs/any orientation. need to change prevTri. Push currentTri
                #to fixingTriangles stack. try to fit prev tri with different orientation then fit current tri, 
                #else fit prev tri with different legs then fit current tri
                checkNTris = 0
                exhaustedOrientations = fittedTriangles.size()
                while (triedFit == False):
                    # while i cannot get current to fit, need to repeat this process. This process involves 
                    # travelling linearly from triangles to fix stack, popping each one and push to fittedtriangles
                    # stack until you get to current, check if current fits, if it doesnt, need to go one more triangle back, first repeat this process
                    # only changing orientation of prev triangles, then if still cannot fit newest tri go back and change legs
                    if exhaustedOrientations > 0:
                        if checkNTris < fittedTriangles.size():
                            checkNTris += 1
                            print("calling process to check prev orientation")
                            print("going this far back", checkNTris)
                            triedFit = theProcess(checkNTris, True)
                            exhaustedOrientations -= 1
                    else:
                        if checkNTris < fittedTriangles.size():
                            checkNTris += 1
                            print("calling process to check prev legs")
                            triedFit = theProcess(checkNTris, False)
        
def theProcess(trust, type):
    print("the process was called")
    triedFit = False
    global currentTri
    for i in range(0, trust):
        if fittedTriangles.size() > 0:
            print("fixing triangle")
            tempTri = fittedTriangles.pop()
            print(tempTri.area, tempTri.coordinate)
            print(currentTri.area, currentTri.coordinate)
            trianglesToFix.push(tempTri)
    while trianglesToFix.size() > 0:
        currentTri = trianglesToFix.pop()
        if type == True: #changing prev orientations 
            leg = currentTri.legs[0]
            triedFit = fitTriangleHelper(arr, leg[1],currentTri.coordinate,currentTri.area, currentTri.orientationIndex + 1)
        else: #changing prev legs
            leg = currentTri.legs[currentTri.legIndex + 1]
            currentTri.legIndex +=1
            triedFit = fitTriangleHelper(arr, leg[1],currentTri.coordinate,currentTri.area, 0)
    return triedFit

    

def sortTriangles(areaList, coordinateList):
    triangleMap = list(zip(areaList, coordinateList))
    triangleMap.sort()
    print("this is tri list: \n")
    print(triangleMap)
    return(triangleMap)

def sortLegs(arr, area, areaXY):
    #first get leg lengths from get legs
    #need to prioritize leg lengths that are similar in size(small delta)
    legs = getLegs(area*2)
    newLegs = []
    for x in range(0,len(legs) - 1):
        if x%2 == 0 and x + 1 <= len(legs) - 1:
            #new leg pair
            legPair = tuple((legs[x],legs[x+1]))
            legDistance = abs(legs[x] - legs[x+1])
            newLegs.append(tuple((legDistance, legPair)))
    newLegs.sort()
    return newLegs
    #need to check all four orientations. +x +y, +x -y, -x +y, -x -y
    
def fitTriangleHelper(arr, legs, areaXY, area, oIndex):
    success = False
    for x in range(oIndex,4): #four orientations
        check = True
        currentTri.orientationIndex = x
        for i in range(1, int(legs[0])):
            if x == 0: #+x +y
                i = i * 1
            elif x == 1: #+x -y
                i = i * 1
            elif x == 2: # -x +y
                i = i * -1
            elif x == 3:
                i = i * -1
            if areaXY[0] + i <= 16 and areaXY[0] + i >= 0:
                if arr[areaXY[0] + i][areaXY[1]] > 0:
                    check = False
            else: 
                check = False
        for j in range(1, int(legs[1])):
            if x == 0: #+x +y
                j = j * 1
            elif x == 1: #+x -y
                j = j * -1
            elif x == 2: # -x +y
                j = j * 1
            elif x == 3:
                j = j * -1
            if areaXY[1] + j <= 16 and areaXY[1] + j >= 0:
                if arr[areaXY[0]][areaXY[1] + j] > 0:
                    check = False
            else:
                check = False
        if check == True:
            for i in range(1, int(legs[0])):
                if x == 0: #+x +y
                     i = i * 1
                elif x == 1: #+x -y
                    i = i * 1
                elif x == 2: # -x +y
                    i = i * -1
                elif x == 3:
                    i = i * -1
                arr[areaXY[0] + i][areaXY[1]] = area
            for j in range(1, int(legs[1])):
                if x == 0: #+x +y
                    j = j * 1
                elif x == 1: #+x -y
                    j = j * -1
                elif x == 2: # -x +y
                    j = j * 1
                elif x == 3:
                    j = j * -1
                arr[areaXY[0]][areaXY[1] + j] = area    
            print("fitted a triangle")
            print(currentTri.area, currentTri.coordinate)
            if currentTri.area == 4:
                customPrint(arr)
            fittedTriangles.push(currentTri)
            global prevTri
            prevTri = currentTri
            success = True
            break
    return success

# setting up the grid

rows, cols = (17, 17)
arr = [[0 for i in range(cols)] for j in range(rows)]
arr[0][9] = 8
arr[0][13] = 2
arr[1][3] = 12
arr[1][14] = 7
arr[2][0] = 4
arr[2][5] = 10
arr[2][12] = 3
arr[3][16] = 5
arr[4][7] = 7
arr[4][13] = 10
arr[5][2] = 3
arr[6][1] = 7
arr[6][11] = 3
arr[6][16] = 3
arr[8][8] = 20
arr[10][0] = 4
arr[10][5] = 14
arr[10][15] = 18
arr[11][14] = 8
arr[12][3] = 9
arr[12][9] = 11
arr[13][0] = 6
arr[14][4] = 3
arr[14][11] = 7
arr[14][16] = 6
arr[15][2] = 12
arr[15][13] = 4
arr[16][3] = 2
arr[16][7] = 18
#customPrint(arr)
getTriangles(arr)
customPrint(arr)
