#Jordan Young
#69691458
#Game Mechanics



class gameState:
    def __init__(self, rows, columns, contents):
        self._numRows = rows
        self._numCols = columns
        self._earlyContents = contents
        self._field = []

    def getNumCols(self) -> int:
        ''' returns number of columns '''
        return self._numCols

    def getNumRows(self) -> int:
        ''' returns number of rows '''
        return self._numRows

    def setUpEmptyField(self):
        ''' sets up empty field '''
        for col in range(self._numCols):
            self._field.append([])
            for row in range(self._numRows):
                self._field[-1].append('   ')
        return self._field

    def setUpContentField(self, inputList: str) -> list:
        ''' sets up a field with preset contents '''
        for col in range(self._numCols):
            self._field.append([])
            for row in range(self._numRows):
                self._field[-1].append('   ')
        for i in range(len(inputList)):
            for value in range(len(inputList[i])):
                if inputList[i][value] != ' ':
                    self._field[value][i] = ' ' + inputList[i][value] + ' '
        return self._field

    def _findLastEmptyCell(self, lst: list) -> int:
        ''' finds last empty cell in a given column '''
        for i in range(len(lst)):
            if lst[i] == '   ':
                temp = i
            if '   ' not in lst:
                temp = 0
        return temp
    
    def _individualListGravity(self, lst: list) -> list:
        ''' moves jewels in a given list down - crude gravity '''
        lst.reverse()
        for i in range(len(lst)-1):
            if (lst[i] == '   ') and (lst[i+1] != '   '):
                lst[i] = lst[i+1]
                lst[i+1] = '   '
        lst = lst.reverse()
        return lst
        
    def gravity(self, gameField: list) -> list:
        ''' moves all jewels the list down like gravity '''
        for lst in gameField:
            self._individualListGravity(lst)
        self._field = gameField
        return gameField

    def createFaller(self, fallerInput: str) -> str:
        ''' makes new faller to put in board '''
        fallerInfo = fallerInput.split()
        faller = []
        faller.append('[' + fallerInfo[4] + ']')
        faller.append('[' + fallerInfo[3] + ']')
        faller.append('[' + fallerInfo[2] + ']')
        return faller

    def fallerFalling(self, fallerInput: str, gameField: list, faller: str) -> list:
        ''' moves faller on gameField down '''
        fallerInfo = fallerInput.split()
        #faller = self.createFaller(fallerInput)
        fallerColumn = int(fallerInfo[1])
        lastEmptyCell = self._findLastEmptyCell(gameField[fallerColumn - 1])
        if lastEmptyCell != None:
            gameField[fallerColumn - 1][0] = faller[0]
        return gameField

############################

    def tick(self, gameField: list, faller: str, temp: str, fallerInfo: str, state: str) -> list:
        ''' passes time in terms of game '''
        if state == 'falling':
            self.gravity(gameField)
            if temp < 3:
                self.fallerFalling(fallerInfo, gameField, faller[temp:])
            checkLanding = self.checkLanding(gameField, fallerInfo, faller)
        if state == 'rotating':
            if self.checkIfFallerIsLanded(gameField, fallerInfo, faller):
                newJewel = self.rotateLandedJewel(faller)
                gameField = self.replaceJewelWithNew(gameField, newJewel)
                newJewelForLanding = self.rotateJewelForFallerVar(faller)
                pass
            else:
                newJewel = self.rotateJewel(faller)
                gameField = self.replaceJewelWithNew(gameField, newJewel)
                newJewelForLanding = self.rotateJewelForFallerVar(faller)
            checkLanding = self.checkLanding(gameField, fallerInfo, newJewelForLanding)
        if state == 'movingRight':
            gameField = self.moveJewelRight(gameField, faller)
            checkLanding = self.checkLanding(gameField, fallerInfo, faller)
        if state == 'movingLeft':
            gameField = self.moveJewelLeft(gameField, faller)
            checkLanding = self.checkLanding(gameField, fallerInfo, faller)
        #checkLanding = self.checkLanding(gameField, fallerInfo, faller)
        '''
        if checkLanding and (state == 'rotating'):
            gameField = self.changeFallingtoLanding(gameField, fallerInfo, newJewel)
        '''
        if checkLanding:
            gameField = self.changeFallingtoLanding(gameField, fallerInfo, faller)
        return gameField

############################
    '''
    def checkLanding(self, fallerInfo, gameField):
        #NEEDS FIXING
        searchJewel = '[' + fallerInfo[-1] + ']'
        searchOnTop = False
        for i in range(len(gameField)):
            if searchJewel in gameField[i]:
                searchCol = i
        print(gameField[searchCol])
        lastEmptyCell = self._findLastEmptyCell(gameField[searchCol])
        if searchJewel == lastEmptyCell:
            searchOnTop = True
    '''

    def rotateJewelForFallerVar(self, faller: str) -> str:
        ''' rotates jewel for faller variable '''
        newJewel = []
        newJewel.append(faller[1])
        newJewel.append(faller[2])
        newJewel.append(faller[0])
        return newJewel

    def rotateLandedJewel(self, faller: str) -> dict:
        ''' rotates jewel when R is input and landed '''
        tempFaller = []
        for jewel in faller:
            tempFaller.append('|' + jewel[1] + '|')
        newJewel = {}
        newJewel[tempFaller[2]] = tempFaller[0]
        newJewel[tempFaller[0]] = tempFaller[1]
        newJewel[tempFaller[1]] = tempFaller[2]
        return newJewel

    def rotateJewel(self, faller: str) -> dict:
        ''' rotates jewel and makes it a dictionary '''
        newJewel = {}
        newJewel[faller[2]] = faller[0]
        newJewel[faller[0]] = faller[1]
        newJewel[faller[1]] = faller[2]
        return newJewel

    def replaceJewelWithNew(self, gameField: list, newJewel: str) -> list:
        ''' puts rotated jewel in field in place of old one '''
        for lst in range(len(gameField)):
            for value in range(len(gameField[lst])):
                if gameField[lst][value] in newJewel:
                    gameField[lst][value] = newJewel[gameField[lst][value]]
        return gameField

    def findJewelInField(self, gameField: list, checkJewel1: str, checkJewel2: str) -> tuple:
        ''' finds where the jewel is in the field '''
        for x in range(len(gameField)):
            for i in range(len(gameField[x])):
                if (gameField[x][i] == checkJewel1) or (gameField[x][i] == checkJewel2):
                    return x, i
                
    def checkFieldToRight(self, gameField: list, coordinate: tuple) -> str:
        ''' checks if spalce to right of bottom jewel is empty '''
        col = coordinate[0] + 1
        row = coordinate[1]
        if col >= self._numCols:
            return 'full'
        elif gameField[col][row] == '   ':
            return 'empty'
        else:
            return 'full'

    def moveJewelRightOnBoard(self, gameField: list, faller: str) -> list:
        ''' moves jewel to the right on board '''
        colNum = self._numCols
        for jewel in faller:
            tempJewel = jewel[1]
            checkJewel1 = '[' + tempJewel + ']'
            checkJewel2 = '|' + tempJewel + '|'
            coordinate = self.findJewelInField(gameField, checkJewel1, checkJewel2)
            if coordinate == None:
                continue
            elif coordinate[0] == colNum:
                continue
            gameField[coordinate[0] + 1][coordinate[1]] = jewel
            gameField[coordinate[0]][coordinate[1]] = '   '
        return gameField

    def moveJewelRight(self, gameField: list, faller: str) -> list:
        ''' sets up field to move jewel right '''
        tempJewel = faller[0][1]
        checkJewel1 = '[' + tempJewel + ']'
        checkJewel2 = '|' + tempJewel + '|'
        coordinate = self.findJewelInField(gameField, checkJewel1, checkJewel2)
        colNum = self._numCols
        if (coordinate[0] + 1) == colNum:
            return gameField
        emptyOrFull = self.checkFieldToRight(gameField, coordinate)
        if emptyOrFull == 'full':
            return gameField
        elif emptyOrFull == 'empty':
            gameField = self.moveJewelRightOnBoard(gameField, faller)
            return gameField

    #########

    def checkFieldToLeft(self, gameField: list, coordinate: tuple) -> str:
        ''' checks spot to left of jewel '''
        col = coordinate[0] - 1
        row = coordinate[1]
        if gameField[col][row] == '   ':
            return 'empty'
        else:
            return 'full'

    def moveJewelLeftOnBoard(self, gameField: list, faller: str) -> list:
        ''' moves jewel to the left on the board '''
        colNum = self._numCols
        for jewel in faller:
            tempJewel = jewel[1]
            checkJewel1 = '[' + tempJewel + ']'
            checkJewel2 = '|' + tempJewel + '|'
            coordinate = self.findJewelInField(gameField, checkJewel1, checkJewel2)
            if coordinate == None:
                continue
            elif coordinate[0] == 0:
                continue
            gameField[coordinate[0] - 1][coordinate[1]] = jewel
            gameField[coordinate[0]][coordinate[1]] = '   '
        return gameField

    def moveJewelLeft(self, gameField: list, faller: str) -> list:
        ''' moves jewel to the left on the board '''
        tempJewel = faller[0][1]
        checkJewel1 = '[' + tempJewel + ']'
        checkJewel2 = '|' + tempJewel + '|'
        coordinate = self.findJewelInField(gameField, checkJewel1, checkJewel2)
        colNum = self._numCols
        if (coordinate[0]) == 0:
            return gameField
        emptyOrFull = self.checkFieldToLeft(gameField, coordinate)
        if emptyOrFull == 'full':
            return gameField
        elif emptyOrFull == 'empty':
            gameField = self.moveJewelLeftOnBoard(gameField, faller)
            return gameField

    

    def changeFallerInfo(self, fallerInfo: str, state: str) -> str:
        ''' changes faller information for when moved '''
        if state == 'movingRight':
            temp = int(fallerInfo.split()[1])
            newTemp = str(temp + 1)
            temp = str(temp)
            newInfo = fallerInfo.replace(temp, newTemp)
        elif state == 'movingLeft':
            temp = int(fallerInfo.split()[1])
            newTemp = str(temp - 1)
            temp = str(temp)
            newInfo = fallerInfo.replace(temp, newTemp)
        return newInfo

    def checkLanding(self, gameField: list, fallerInfo: str, faller: str) -> bool:
        ''' checks if faller is in landed state '''
        otherCheckJewel = '|' + faller[0][1] + '|'
        jewelCol = int(int(fallerInfo.split()[1]) - 1)
        for i in range(len(gameField[jewelCol])):
            if (gameField[jewelCol][i] == faller[0]) or (gameField[jewelCol][i] == otherCheckJewel):
                temp = i
        if temp == (self._numRows - 1):
            return True
        elif temp < (self._numRows - 1):
            if gameField[jewelCol][temp+1] != '   ':
                return True

    
    def createFallingToLandingDic(self, gameField: list, faller: list) -> dict:
        ''' makes faller to landed dictionary '''
        landerDic = {}
        for jewel in faller:
            jewelColor = jewel[1]
            landerDic[jewel] = '|' + jewelColor + '|'
        return landerDic

    def changeFallingtoLanding(self, gameField: list, fallerInfo: str, faller: str) -> list:
        ''' changes the faller to a landed state '''
        jewelCol = int(int(fallerInfo.split()[1]) - 1)
        landerDic = self.createFallingToLandingDic(gameField, faller)
        for i in range(len(gameField[jewelCol])):
            if gameField[jewelCol][i] in landerDic:
                gameField[jewelCol][i] = landerDic[gameField[jewelCol][i]]
        return gameField

    def checkIfFallerIsLanded(self, gameField: list, fallerInfo: str, faller: str) -> bool:
        ''' checks if the faller is landed '''
        jewelCol = int(int(fallerInfo.split()[1]) - 1)
        tempJewel = faller[0][1]
        checkJewel = '|' + tempJewel + '|'
        for i in gameField[jewelCol]:
            if i == checkJewel:
                return True

    def createLandingToFrozenDic(self, gameField: list, faller: str) -> dict:
        ''' makes landing to frozen dictionary '''
        frozenDic = {}
        for jewel in faller:
            jewelColor = jewel[1]
            frozenDic['|' + jewelColor + '|'] = ' ' + jewelColor + ' '
        return frozenDic

    def freezeJewel(self, gameField: list, fallerInfo: list, faller: str) -> list:
        ''' freezes the jewel in the field '''
        jewelCol = int(int(fallerInfo.split()[1]) - 1)
        frozenDic = self.createLandingToFrozenDic(gameField, faller)
        for i in range(len(gameField[jewelCol])):
            if gameField[jewelCol][i] in frozenDic:
                gameField[jewelCol][i] = frozenDic[gameField[jewelCol][i]]
        return gameField

    def checkIfValidColumn(self, col: int) -> bool:
        ''' checks if column is a valid input '''
        return 0 <= col < self._numCols

    def checkIfValidRow(self, row: int) -> bool:
        ''' checks if row is a valid input '''
        return 0 <= row < self._numRows

    def checkForMatches(self, gameField: list, col: int, row: int, colDelta: int, rowDelta: int) -> bool:
        ''' checks if there are matches in the current field '''
        startCell = gameField[col][row][1]
        if startCell == ' ':
            return False
        else:
            for i in range(1,3):
                if not self.checkIfValidColumn(col + colDelta * i) \
                   or not self.checkIfValidRow(row + rowDelta * i) \
                   or gameField[col + colDelta * i][row + rowDelta * i][1] != startCell:
                    return False
            return True

    def makeParallelColList(self, col: int) -> list:
        ''' makes list of columns to be deleted due to matches '''
        colList = []
        temp1 = col + 1
        temp2 = col + 2
        colList.append(col)
        colList.append(temp1)
        colList.append(temp2)
        return colList

    def makeParallelRowList(self, row: int) -> list:
        ''' makes list of columns to be deleted due to matches '''
        rowList = []
        temp1 = row + 1
        temp2 = row + 2
        rowList.append(row)
        rowList.append(temp1)
        rowList.append(temp2)
        return rowList

    def makeVoidParallelColList(self, col: int) -> list:
        ''' makes list of columns to be deleted due to matches '''
        colList = []
        colList.append(col)
        colList.append(col)
        colList.append(col)
        return colList

    def makeVoidParallelRowList(self, row: int) -> list:
        ''' makes list of columns to be delted due to matches '''
        rowList = []
        rowList.append(row)
        rowList.append(row)
        rowList.append(row)
        return rowList

    def makeParallelUpRowList(self, row: int) -> list:
        ''' makes list of rows to be delted due to matches '''
        rowList = []
        temp1 = row - 1
        temp2 = row - 2
        rowList.append(row)
        rowList.append(temp1)
        rowList.append(temp2)
        return rowList

    def rewriteMatchesOnBoard(self, gameField: list, colList: int, rowList: int) -> list:
        ''' writes matches with * on board '''
        for i in range(len(colList)):
            gameField[colList[i]][rowList[i]] = '*' + gameField[colList[i]][rowList[i]][1] + '*'
        return gameField

    def deleteMatchesOnBoard(self, gameField: list) -> list:
        ''' deletes the matches on the board '''
        for col in range(len(gameField)):
            for row in range(len(gameField[col])):
                if gameField[col][row][0] == '*':
                    gameField[col][row] = '   '
        return gameField

    def matchesPresent(self, gameField: list) -> bool:
        ''' sees if there are matches on the board '''
        for col in range(len(gameField)):
            for row in range(len(gameField[col])):
                if gameField[col][row][0] == '*':
                    return True
        return False
            
        
        
        
    
        
        
        

    
    
        



        
        
        

    

    
                    
                
                
        
    



