class Position:
    def __init__(self, column, row):
        if column not in 'abcdefgh':
            raise ValueError('Colonne invalide, doit être entre a et h')
        if not (1 <= row <= 8):
            raise ValueError('Ligne invalide, doit être entre 1 et 8')

        self.column = column
        self.row = row

    def __str__(self):
        return f'{self.column}{self.row}'

    def get_column(self):
        return self.column

    def get_row(self):
        return self.row

    def set_column(self, column):
        if column not in 'abcdefgh':
            raise ValueError('Colonne invalide')
        self.column = column

    def set_row(self, row):
        if not (1 <= row <= 8):
            raise ValueError('Ligne invalide')
        self.row = row
        