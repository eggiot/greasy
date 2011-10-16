class Grid(object):
    def __init__(self, rows, columns):
        self.columns = columns
        self.rows = rows
        self.matrix = []
        for row in range(rows):
            currentRow = []
            for column in range(columns):
                currentRow.append(0)
            self.matrix.append(currentRow)
    
    def setItem(self, item, row, column):
        self.matrix[row][column] = item
    
    def getItem(self, row, column):
        return self.matrix[row][column]
    
    def __iter__(self):
        for row in range(self.rows):
            for column in range(self.columns):
                yield (row, column)