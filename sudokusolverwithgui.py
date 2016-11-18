# Program for solving sudoku

from tkinter import *

root = Tk()

class cell:
    def __init__ (self,coordinate,sudoku):
        self.coordinate = coordinate
        self.sudoku = sudoku
        self.isSet = False
        self.possibleNumbers = [n for n in range(1,10)]
        self.currentNumber = 0
        [x,y] = self.coordinate
        self.sections = self.sudoku.findSections(x,y)
        for s in self.sections:
            s.addCell(self)
        self.displayCell = self.sudoku.gui.addCell(x,y,self)
        
    def eliminateNumber (self,n):
        if n in self.possibleNumbers:
            self.possibleNumbers.remove(n)
    
    def setNumber (self,n):
        if n in self.possibleNumbers:
            self.isSet = True
            self.possibleNumbers = []
            self.currentNumber = n
            for s in self.sections:
                s.eliminateNumber(n)
            self.displayCell.insert(END,str(n))
            print("Cell at " + str(self.coordinate) + " is " + str(n))
        else:
            print ("That number can't be there")

    def getNumber(self):
        n = self.displayCell.get()
        if n != "" and not self.isSet:
            self.displayCell.delete(0,END)
            self.setNumber(int(n))
            
class section:
    def __init__ (self,sudoku):
        self.sudoku = sudoku
        self.cellsInSection = []
        self.possibleNumbers = [n for n in range(1,10)]

    def addCell(self,cell):
        self.cellsInSection += [cell]

    def eliminateNumber(self,n):
        for c in self.cellsInSection:
            c.eliminateNumber(n)
        if n in self.possibleNumbers:
            self.possibleNumbers.remove(n)

    def findUniqueNumber(self):
        changeMade = False
        for n in self.possibleNumbers:
            numberOfPlaces = 0
            for c in self.cellsInSection:
                if not c.isSet:
                    if n in c.possibleNumbers:
                        numberOfPlaces += 1
                        currentPlace = c
            if numberOfPlaces == 1:
                currentPlace.setNumber(n)
                changeMade = True
        return changeMade

class sudoku:
    def __init__(self):
        self.rows = [section(self) for n in range(9)]
        self.columns = [section(self) for n in range(9)]
        self.squares = [section(self) for n in range(9)]
        self.sectionsInSudoku = self.rows + self.columns + self.squares
        self.cellsInSudoku = []
        self.gui = GUI(root,self)
        for y in range(9):
            for x in range(9):
                c = cell([x,y],self)
                self.cellsInSudoku += [c]

    
    def findSections(self,x,y):
        row = self.rows[y]
        column = self.columns[x]
        whichSquare = x//3 + (y//3)*3
        square = self.squares[whichSquare]
        return [row, column, square]

    def findUniqueCell(self):
        changeMade = False
        for c in self.cellsInSudoku:
            if len(c.possibleNumbers) == 1:
                c.setNumber(c.possibleNumbers[0])
                changeMade = True
        return changeMade

    def solve(self):
        changeMade = True
        while changeMade:
            changeMade = self.findUniqueCell()
        changeMade = True
        while changeMade:
            firstTechnique = self.findUniqueCell()
            for s in self.sectionsInSudoku:
                secondTechnique = False
                secondTechniqueTemporary = s.findUniqueNumber()
                if secondTechniqueTemporary:
                    secondTechnique = True
            changeMade = firstTechnique or secondTechnique

    def submit(self):
        for c in self.cellsInSudoku:
            c.getNumber()

    def reset(self):
        for c in self.cellsInSudoku:
            c.isSet = False
            c.possibleNumbers = [n for n in range(1,10)]
            c.currentNumber = 0
            c.displayCell.delete(0,END)
        for s in self.sectionsInSudoku:
            s.possibleNumbers = [n for n in range(1,10)]
            
    def setNumber(self,x,y,n):
        self.cellsInSudoku[x+9*y].setNumber(n)

class GUI:
    def __init__(self,master,sudoku):
        self.master = master
        self.sudoku = sudoku
        self.cellsInGUI = []
        master.title("A simple sudoku solver")

        self.resetButton = Button(master, text="Reset", command=self.sudoku.reset)
        self.resetButton.grid(row=10, column=0, columnspan=3)
        
        self.submitButton = Button(master, text="Submit", command=self.sudoku.submit)
        self.submitButton.grid(row=10, column=3, columnspan=3)

        self.solveButton = Button(master, text="Solve", command=self.sudoku.solve)
        self.solveButton.grid(row=10, column=6, columnspan=3)               

    def addCell(self,x,y,cell):
        c = Entry(width = 3, justify=CENTER)
        self.cellsInGUI.append(c)
        c.grid(row=y, column=x)
        return c

puzzle = sudoku()
root.mainloop()


'''
Solve method
1) use set number to eliminate possible numbers
2) check for cells with just one possible number (Unique cell)
3) check if only one of a number exists in as row, column or square (Unique number)

Have used as short hand in places
c = cell
n = number
s = section
'''


