#Name: Analisa Wood
#UNI: aaw2182


from BaseAI import BaseAI
import random
import time

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        time_start = time.process_time()
        available_cells = len(grid.getAvailableCells())
        # Dynamically adjust depth based on the number of empty cells
        depth = 3 if available_cells < 5 else 4
        bestMove, _ = self.maximize(grid, depth=depth, alpha=-float('inf'), beta=float('inf'), time_start=time_start)
        return bestMove

    def maximize(self, grid, depth, alpha, beta, time_start):
        # Base Case!!!
        if depth == 0 or time.process_time() - time_start > 0.19 or not grid.canMove():
            return None, self.evaluateGrid(grid)

        maxUtility = -float('inf')
        bestMove = None

        for move, newGrid in grid.getAvailableMoves():
            _, utility = self.minimize(newGrid, depth - 1, alpha, beta, time_start)
            if utility > maxUtility:
                maxUtility = utility
                bestMove = move

            # alpha and prune
            alpha = max(alpha, maxUtility)
            if alpha >= beta:
                break

        return bestMove, maxUtility

    def minimize(self, grid, depth, alpha, beta, time_start):
        # Base Case
        if depth == 0 or time.process_time() - time_start > 0.19 or not grid.canMove():
            return None, self.evaluateGrid(grid)

        expectedUtility = 0
        availableCells = grid.getAvailableCells()
        numEmptyCells = len(availableCells)

        if numEmptyCells == 0:
            return None, self.evaluateGrid(grid)

        for cell in availableCells:
            for value, probability in [(2, 0.9), (4, 0.1)]:
                # Adjust prob based on the numb of empty cells
                adjustedProbability = probability / numEmptyCells
                newGrid = grid.clone()
                newGrid.setCellValue(cell, value)
                _, utility = self.maximize(newGrid, depth - 1, alpha, beta, time_start)
                expectedUtility += adjustedProbability * utility

                # Early pruning if possible
                if expectedUtility >= beta:
                    return None, expectedUtility

        return None, expectedUtility

    def evaluateGrid(self, grid):
        # Simplified heuristic weights to balance their effect
        return (self.availableMovesHeuristic(grid) * 5 +   # Reduced weight
                self.maxTileValue(grid) * 0.5 +            # Slightly increased weight
                self.snakeHeuristic(grid) * 50 +           # Reduced weight for balance
                self.minChangeHeuristic(grid) * 0.1)

    def availableMovesHeuristic(self, grid):
        # want to max the num of available moves
        return len(grid.getAvailableMoves())

    def maxTileValue(self, grid):
        # want to reach larger tiles
        return grid.getMaxTile()

    def snakeHeuristic(self, grid):
        # Original snake weights
        weights = [
            [65536, 32768, 16384, 8192],
            [512, 1024, 2048, 4096],
            [256, 128, 64, 32],
            [2, 4, 8, 16]
        ]

        score = 0
        for i in range(grid.size):
            for j in range(grid.size):
                score += grid.getCellValue((i, j)) * weights[i][j]

        return score

    def minChangeHeuristic(self, grid):
        # Min change in min val. max merging
        minValue = float('inf')

        for row in grid.map:
            for value in row:
                if value != 0:
                    minValue = min(minValue, value)
        return minValue


#minimize and maximize functions that call ea1chother and what not

#heuristic that is based on the remaining number of moves given a choice


