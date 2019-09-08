#Jordan Young
#69691458
#User Interface module

#4 rows 3 columns

import project4_game_mechanics

def run():
    ''' runs the userinterface of the game '''
    gameOver = False
    falling = True
    playing = True
    numRows = getInputRows()
    if numRows == 'Q':
        return
    numCols = getInputCols()
    if numCols == 'Q':
        return
    gameState = project4_game_mechanics.gameState(numRows, numCols, None)
    gameField = handlingThirdLineInput(numRows, gameState)
    if gameField == 'quit':
        return
    #matching will occur here too
    matchesForContentBoard(gameField, gameState, numRows, numCols)
    #printBoard(numRows, numCols, gameField)
    while playing:
        userMove = input()
        if userMove == 'Q':
            break
        gameField = nextMove(gameState, gameField, userMove)
        if userMove[0] == 'F':
            fallerInfo = userMove
            faller = gameState.createFaller(userMove)
            state = 'falling'
        printBoard(numRows, numCols, gameField)
        temp = 1
        while state != 'frozen':
            userMove = input()
            if userMove == 'Q':
                playing = False
                break
            if userMove == '':
                toBeFrozen = False
                toBeFrozen = gameState.checkIfFallerIsLanded(gameField, fallerInfo, faller)
                if toBeFrozen:
                    gameField = gameState.freezeJewel(gameField, fallerInfo, faller)
                    while True:
                        #gameField = checkingAndWritingMatches(gameField, gameState)
                        for col in range(len(gameField)):
                            for row in range(len(gameField[col])):
                                verticalMatchesPresent = gameState.checkForMatches(gameField, col, row, 0, 1)
                                horizontalMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, 0)
                                diagonalDownMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, 1)
                                diagonalUpMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, -1)
                                if verticalMatchesPresent:
                                    colList = gameState.makeVoidParallelColList(col)
                                    rowList = gameState.makeParallelRowList(row)
                                elif horizontalMatchesPresent:
                                    colList = gameState.makeParallelColList(col)
                                    rowList = gameState.makeVoidParallelRowList(row)
                                elif diagonalDownMatchesPresent:
                                    colList = gameState.makeParallelColList(col)
                                    rowList = gameState.makeParallelRowList(row)
                                elif diagonalUpMatchesPresent:
                                    colList = gameState.makeParallelColList(col)
                                    rowList = gameState.makeParallelUpRowList(row)
                                else:
                                    continue
                                gameField = gameState.rewriteMatchesOnBoard(gameField, colList, rowList)
                             
                                #print('print 1')
                                #printBoard(numRows, numCols, gameField)
                        if gameState.matchesPresent(gameField):
                            userMoveFormality = 'hello'
                            printBoard(numRows, numCols, gameField)
                            while userMoveFormality != '':
                                userMoveFormality = input()
                            gameField = gameState.deleteMatchesOnBoard(gameField)
                            for i in range(numRows):
                                gameField = gameState.gravity(gameField)
                            #print('print 2')
                            #printBoard(numRows, numCols, gameField)
                            continue
                            break
                        else:        
                            printBoard(numRows, numCols, gameField)
                            break
                    if temp < 3:
                        print('GAME OVER')
                        gameOver = True
                        break
                    else:
                        break
                else:
                    state = 'falling'
                    gameField = gameState.tick(gameField, faller, temp, fallerInfo, state)
                    printBoard(numRows, numCols, gameField)
                    temp += 1
            if userMove == 'R':
                state = 'rotating'
                gameField = gameState.tick(gameField, faller, temp, fallerInfo, state)
                faller = gameState.rotateJewelForFallerVar(faller)
                printBoard(numRows, numCols, gameField)
            if userMove == '<':
                state = 'movingLeft'
                tempJewel = faller[0][1]
                checkJewel1 = '[' + tempJewel + ']'
                checkJewel2 = '|' + tempJewel + '|'
                coordinate = gameState.findJewelInField(gameField, checkJewel1, checkJewel2)
                emptyOrFull = gameState.checkFieldToLeft(gameField, coordinate)
                if (int(fallerInfo.split()[1]) != 1) and (emptyOrFull == 'empty'):
                    fallerInfo = gameState.changeFallerInfo(fallerInfo, state)
                gameField = gameState.tick(gameField, faller, temp, fallerInfo, state)
                printBoard(numRows, numCols, gameField)
            if userMove == '>':
                state = 'movingRight'
                tempJewel = faller[0][1]
                checkJewel1 = '[' + tempJewel + ']'
                checkJewel2 = '|' + tempJewel + '|'
                coordinate = gameState.findJewelInField(gameField, checkJewel1, checkJewel2)
                emptyOrFull = gameState.checkFieldToRight(gameField, coordinate)
                if (int(fallerInfo.split()[1]) != numCols) and (emptyOrFull == 'empty'):
                    fallerInfo = gameState.changeFallerInfo(fallerInfo, state)
                gameField = gameState.tick(gameField, faller, temp, fallerInfo, state)
                printBoard(numRows, numCols, gameField)
        if gameOver == True:
            return

def getInputRows():
    ''' gets number of rows '''
    try:
        numRows = int(input())
        return numRows
    except ValueError:
        numRows = 'Q'
        return numRows

def getInputCols():
    ''' gets number of columns '''
    try:
        numCols = int(input())
        return numCols
    except ValueError:
        numCols = 'Q'
        return numCols

def handlingThirdLineInput(numRows: int, gameState: list) -> list:
    ''' takes third input then sets either empty or contents field depending on input'''
    emptyOrContent = input()
    if emptyOrContent == 'EMPTY':
        gameField = gameState.setUpEmptyField()
    elif emptyOrContent == 'Q':
        return 'quit'
    elif emptyOrContent == 'CONTENTS':
        inputList = []
        for i in range(numRows):
            inputList.append(input())
        gameField = gameState.setUpContentField(inputList)
        for i in range(numRows):
            gameField = gameState.gravity(gameField)
    return gameField
        
        #gameField = gameState.setUpContentField

def printBoard(numRows: int, numCols: int, gameField: list) -> None:
    ''' prints board based on gameField'''
    temp = 0
    for i in range(len(gameField[0])):
        print('|', end = '')
        for lst in gameField:
            print(lst[temp], end = '')
        print('|')
        temp += 1
    print(' ' + ('-' * (len(gameField)) * 3) + ' ')
    temp = 0

def useGravity(gameField):
    pass

def checkingAndWritingMatches(gameField, gameState):
    for col in range(len(gameField)):
        for row in range(len(gameField[col])):
            verticalMatchesPresent = gameState.checkForMatches(gameField, col, row, 0, 1)
            horizontalMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, 0)
            diagonalDownMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, 1)
            diagonalUpMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, -1)
            if verticalMatchesPresent:
                colList = gameState.makeVoidParallelColList(col)
                rowList = gameState.makeParallelRowList(row)
            elif horizontalMatchesPresent:
                colList = gameState.makeParallelColList(col)
                rowList = gameState.makeVoidParallelRowList(row)
            elif diagonalDownMatchesPresent:
                colList = gameState.makeParallelColList(col)
                rowList = gameState.makeParallelRowList(row)
            elif diagonalUpMatchesPresent:
                colList = gameState.makeParallelColList(col)
                rowList = gameState.makeParallelUpRowList(row)
            else:
                continue
            gameField = gameState.rewriteMatchesOnBoard(gameField, colList, rowList)
            return gameField
                        

def nextMove(gameState, gameField: list, userMove: str) -> list:
    ''' handles the users next input '''
    activeFaller = False
    if userMove == 'Q':
        playing = False
        return playing
    if userMove == '' and activeFaller == True:
        pass
    elif userMove == '':
        pass
    elif userMove[0] == 'F':
        faller = gameState.createFaller(userMove)
        gameField = gameState.fallerFalling(userMove, gameField, faller)
        # CHECK LANDING HERE THEN CHANGE TO LANDED IF LANDED
        checkLanding = gameState.checkLanding(gameField, userMove, faller)
        if checkLanding:
            gameField = gameState.changeFallingtoLanding(gameField, userMove, faller)
    return gameField

def matchesForContentBoard(gameField, gameState, numRows, numCols):
    while True:
        for col in range(len(gameField)):
            for row in range(len(gameField[col])):
                verticalMatchesPresent = gameState.checkForMatches(gameField, col, row, 0, 1)
                horizontalMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, 0)
                diagonalDownMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, 1)
                diagonalUpMatchesPresent = gameState.checkForMatches(gameField, col, row, 1, -1)
                if verticalMatchesPresent:
                    colList = gameState.makeVoidParallelColList(col)
                    rowList = gameState.makeParallelRowList(row)
                elif horizontalMatchesPresent:
                    colList = gameState.makeParallelColList(col)
                    rowList = gameState.makeVoidParallelRowList(row)
                elif diagonalDownMatchesPresent:
                    colList = gameState.makeParallelColList(col)
                    rowList = gameState.makeParallelRowList(row)
                elif diagonalUpMatchesPresent:
                    colList = gameState.makeParallelColList(col)
                    rowList = gameState.makeParallelUpRowList(row)
                else:
                    continue
                gameField = gameState.rewriteMatchesOnBoard(gameField, colList, rowList)
             
                #print('print 1')
                #printBoard(numRows, numCols, gameField)
        if gameState.matchesPresent(gameField):
            userMoveFormality = 'hello'
            printBoard(numRows, numCols, gameField)
            while userMoveFormality != '':
                userMoveFormality = input()
            gameField = gameState.deleteMatchesOnBoard(gameField)
            for i in range(numRows):
                gameField = gameState.gravity(gameField)
            #print('print 2')
            #printBoard(numRows, numCols, gameField)
            continue
            break
        else:        
            printBoard(numRows, numCols, gameField)
            break

    

        

if __name__=='__main__':
    run()
                
        
            
                
            
        
        
            
            
    
    



