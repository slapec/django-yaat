# coding: utf-8


class YaatData:
    def __init__(self, columns, rows, page):
        self.columns = columns
        self.rows = rows
        self.page = page


class YaatRow:
    def __init__(self, id, cells):
        self.id = id
        self.cells = cells
