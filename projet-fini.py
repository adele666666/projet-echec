#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:09:19 2026

@author: adla309
"""
print("coucou")
import random
import copy

# ================= POSITION =================
class Position:
    def __init__(self, column: str, row: int):
        self.column = column
        self.row = row

    def __str__(self):
        return f"{self.column}{self.row}"

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row

    def __hash__(self):
        return hash((self.column, self.row))


# ================= PIECES =================
class Piece:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.has_moved = False

    def isValidMove(self, newPosition, board):
        return True


class King(Piece):
    def __str__(self):
        return "K" if self.color == 0 else "k"

    def isValidMove(self, newPosition, board):
        dx = abs(ord(newPosition.column) - ord(self.position.column))
        dy = abs(newPosition.row - self.position.row)

        target = board.getPiece(newPosition)
        if target and target.color == self.color:
            return False

        return dx <= 1 and dy <= 1


class Queen(Piece):
    def __str__(self):
        return "Q" if self.color == 0 else "q"

    def isValidMove(self, newPosition, board):
        dx = abs(ord(newPosition.column) - ord(self.position.column))
        dy = abs(newPosition.row - self.position.row)

        target = board.getPiece(newPosition)
        if target and target.color == self.color:
            return False

        if dx == dy or dx == 0 or dy == 0:
            return board.isPathClear(self.position, newPosition)
        return False


class Rook(Piece):
    def __str__(self):
        return "R" if self.color == 0 else "r"

    def isValidMove(self, newPosition, board):
        dx = abs(ord(newPosition.column) - ord(self.position.column))
        dy = abs(newPosition.row - self.position.row)

        target = board.getPiece(newPosition)
        if target and target.color == self.color:
            return False

        if dx == 0 or dy == 0:
            return board.isPathClear(self.position, newPosition)
        return False


class Bishop(Piece):
    def __str__(self):
        return "B" if self.color == 0 else "b"

    def isValidMove(self, newPosition, board):
        dx = abs(ord(newPosition.column) - ord(self.position.column))
        dy = abs(newPosition.row - self.position.row)

        target = board.getPiece(newPosition)
        if target and target.color == self.color:
            return False

        if dx == dy:
            return board.isPathClear(self.position, newPosition)
        return False


class Knight(Piece):
    def __str__(self):
        return "N" if self.color == 0 else "n"

    def isValidMove(self, newPosition, board):
        dx = abs(ord(newPosition.column) - ord(self.position.column))
        dy = abs(newPosition.row - self.position.row)

        target = board.getPiece(newPosition)
        if target and target.color == self.color:
            return False

        return (dx, dy) in [(1, 2), (2, 1)]


class Pawn(Piece):
    def __str__(self):
        return "P" if self.color == 0 else "p"

    def isValidMove(self, newPosition, board):
        direction = 1 if self.color == 0 else -1
        dx = ord(newPosition.column) - ord(self.position.column)
        dy = newPosition.row - self.position.row

        target = board.getPiece(newPosition)

        if dx == 0:
            if target:
                return False
            if dy == direction:
                return True
            if not self.has_moved and dy == 2 * direction:
                intermediate = Position(self.position.column, self.position.row + direction)
                return board.getPiece(intermediate) is None
            return False

        if abs(dx) == 1 and dy == direction:
            return target is not None and target.color != self.color

        return False


# ================= BOARD =================
class Board:
    def __init__(self):
        self.pieces = {}
        self.initPieces()

    def initPieces(self):
        for c in "abcdefgh":
            self.pieces[Position(c, 2)] = Pawn(Position(c, 2), 0)
            self.pieces[Position(c, 7)] = Pawn(Position(c, 7), 1)

        placement = [
            (Rook, "a", "h"),
            (Knight, "b", "g"),
            (Bishop, "c", "f"),
            (Queen, "d", None),
            (King, "e", None)
        ]

        for pieceClass, c1, c2 in placement:
            self.pieces[Position(c1, 1)] = pieceClass(Position(c1, 1), 0)
            self.pieces[Position(c1, 8)] = pieceClass(Position(c1, 8), 1)
            if c2:
                self.pieces[Position(c2, 1)] = pieceClass(Position(c2, 1), 0)
                self.pieces[Position(c2, 8)] = pieceClass(Position(c2, 8), 1)

    def getPiece(self, position):
        return self.pieces.get(position)

    def movePiece(self, fromPos, toPos):
        piece = self.pieces.get(fromPos)
        if piece:
            del self.pieces[fromPos]
            piece.position = toPos
            piece.has_moved = True
            self.pieces[toPos] = piece

    def isPathClear(self, fromPos, toPos):
        dx = ord(toPos.column) - ord(fromPos.column)
        dy = toPos.row - fromPos.row

        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

        x = ord(fromPos.column) + step_x
        y = fromPos.row + step_y

        while (x != ord(toPos.column)) or (y != toPos.row):
            if self.getPiece(Position(chr(x), y)):
                return False
            x += step_x
            y += step_y

        return True

    # ================= ÉCHEC =================
    def findKing(self, color):
        for pos, piece in self.pieces.items():
            if isinstance(piece, King) and piece.color == color:
                return pos
        return None

    def isInCheck(self, color):
        king_pos = self.findKing(color)

        for pos, piece in self.pieces.items():
            if piece.color != color:
                if piece.isValidMove(king_pos, self):
                    return True
        return False

    def simulateMove(self, start, end):
        new_board = copy.deepcopy(self)
        new_board.movePiece(start, end)
        return new_board


# ================= PLAYER =================
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def askMove(self):
        return input(f"{self.name} joue (ex: e2 e4) : ")


class AIPlayer(Player):
    def askMove(self):
        return f"{random.choice('abcdefgh')}{random.randint(1,8)} {random.choice('abcdefgh')}{random.randint(1,8)}"


# ================= GAME =================
class Chess:
    def __init__(self):
        self.board = Board()
        self.players = []
        self.currentPlayer = None

    def initPlayers(self):
        for c, nom in [(0, "blanc"), (1, "noir")]:
            n = input(f"Nom joueur {nom} (ou AI): ")
            player = AIPlayer(n, c) if n.lower() == "ai" else Player(n, c)
            self.players.append(player)
        self.currentPlayer = self.players[0]

    def displayBoard(self):
        GREEN = "\033[92m"
        BLUE = "\033[94m"
        RESET = "\033[0m"

        print(f"    {BLUE}a b c d e f g h{RESET}")

        for r in range(8, 0, -1):
            row = f"{GREEN}{r}{RESET} | "
            for c in "abcdefgh":
                piece = self.board.getPiece(Position(c, r))
                row += str(piece) if piece else "."
                row += " "
            print(row)
        print()

    def parseMove(self, move):
        try:
            start, end = move.split()
            return Position(start[0], int(start[1])), Position(end[0], int(end[1]))
        except:
            return None, None

    def isValidMove(self, move):
        start, end = self.parseMove(move)
        if not start or not end:
            return False

        piece = self.board.getPiece(start)
        if not piece:
            return False

        if piece.color != self.currentPlayer.color:
            return False

        if not piece.isValidMove(end, self.board):
            return False

        #  interdit de se mettre en échec
        new_board = self.board.simulateMove(start, end)
        if new_board.isInCheck(self.currentPlayer.color):
            return False

        return True

    def updateBoard(self, move):
        start, end = self.parseMove(move)
        self.board.movePiece(start, end)

    def switchPlayer(self):
        self.currentPlayer = self.players[1] if self.currentPlayer == self.players[0] else self.players[0]

    def hasLegalMove(self, color):
        for start, piece in self.board.pieces.items():
            if piece.color != color:
                continue

            for c in "abcdefgh":
                for r in range(1, 9):
                    end = Position(c, r)
                    if piece.isValidMove(end, self.board):
                        new_board = self.board.simulateMove(start, end)
                        if not new_board.isInCheck(color):
                            return True
        return False

    def isCheckMate(self):
        color = self.currentPlayer.color
        return self.board.isInCheck(color) and not self.hasLegalMove(color)

    def play(self):
        self.initPlayers()

        while True:
            self.displayBoard()

            if self.board.isInCheck(self.currentPlayer.color):
                print(" ÉCHEC !")

            if self.isCheckMate():
                print(" ÉCHEC ET MAT ! FIN DE PARTIE")
                break

            move = ""
            while not self.isValidMove(move):
                move = self.currentPlayer.askMove()

            self.updateBoard(move)
            self.switchPlayer()


# ================= MAIN =================
if __name__ == "__main__":
    Chess().play()