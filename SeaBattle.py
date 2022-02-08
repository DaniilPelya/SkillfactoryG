from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, len_, o):
        self.bow = bow
        self.len_ = len_
        self.o = o
        self.lives = len_

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.len_):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, height, width, hid=False):
        self.height = height
        self.width = width
        self.hid = hid

        self.count = 0

        self.field = [["O"] * width for _ in range(height)]

        self.busy = []
        self.ships = []

    def val(self):
        return [self.height, self.width]

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ' '
        for _ in range(1, self.width + 1):
            res += ' | ' + str(_)
        res += ' |'
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.height) and (0 <= d.y < self.width))

    def shot(self, d):
        if self.out(d):
            #self.busy.append(d)
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):  # эту строчку можно записать и иначе: if d in ship.dots
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy, filled=[], c=0):
        self.board = board
        self.enemy = enemy
        self.a = self.board.val()
        self.height, self.width = self.a
        self.filled = filled
        self.c = c

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)  # возвращает True или False
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):

    def ask(self):

        if self.enemy.count == self.c + 1:
            self.c = self.c + 1
            self.filled = []

        if self.enemy.count == self.c:
            if len(self.filled) == 0:
                d = Dot(randint(0, self.height-1), randint(0, self.width-1))
                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                for ship in self.enemy.ships:
                    if d in ship.dots and d not in self.enemy.busy:
                        self.filled.append(d)
                return d

            if len(self.filled) == 1:
                d1 = self.filled[0]
                b = True
                while b:
                    d = Dot(randint((d1.x - 1), (d1.x + 1)), randint((d1.y - 1), (d1.y + 1)))
                    if d == d1 or (
                            (d.x == d1.x - 1 and d.y == d1.y + 1) or
                            (d.x == d1.x - 1 and d.y == d1.y - 1) or
                            (d.x == d1.x + 1 and d.y == d1.y - 1) or
                            (d.x == d1.x + 1 and d.y == d1.y + 1)):
                        b = True
                    else:
                        b = False
                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                for ship in self.enemy.ships:
                    if d in ship.dots and d not in self.enemy.busy:
                        self.filled.append(d)
                return d

            if len(self.filled) == 2:
                d1 = self.filled[0]
                d2 = self.filled[1]
                if d1.x == d2.x and d1.y < d2.y:
                    b = True
                    while b:
                        d = Dot(d1.x, randint((d1.y - 1), (d2.y + 1)))
                        if d in self.enemy.busy:
                            b = True
                        else:
                            b = False

                if d1.x == d2.x and d1.y > d2.y:
                    b = True
                    while b:
                        d = Dot(d1.x, randint((d2.y - 1), (d1.y + 1)))
                        if d in self.enemy.busy:
                            b = True
                        else:
                            b = False

                if d1.x < d2.x and d1.y == d2.y:
                    b = True
                    while b:
                        d = Dot(randint((d1.x - 1), (d2.x + 1)), d1.y)
                        if d in self.enemy.busy:
                            b = True
                        else:
                            b = False

                if d1.x > d2.x and d1.y == d2.y:
                    b = True
                    while b:
                        d = Dot(d1.x, randint((d2.x - 1), (d1.x + 1)))
                        if d in self.enemy.busy:
                            b = True
                        else:
                            b = False

                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                for ship in self.enemy.ships:
                    if d in ship.dots and d not in self.enemy.busy:
                        self.filled.append(d)
                return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.greet()
        size = self.field_size()
        self.height = size[0]
        self.width = size[1]
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def field_size(self):
        while True:
            size = input("Введите высоту и ширину поля от 6 до 9: ").split()

            if len(size) != 2:
                print(" Введите 2 размера! ")
                continue

            height, width = size

            if not (height.isdigit()) or not (width.isdigit()):
                print(" Введите числа! ")
                continue

            height, width = int(height), int(width)

            if 9 < height < 6 and 9 < width < 6:
                print('Введите размеры от 6 до 9')
                continue

            size = [height, width]
            return size

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(self.height, self.width)
        attempts = 0
        for L in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.height), randint(0, self.width)), L, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-----------------------------")
        print("       Приветсвуем вас       ")
        print("            в игре           ")
        print("          морской бой        ")
        print("-----------------------------")
        print(" формат ввода: высота ширина ")
        print("   Высота поля - от 6 до 9   ")
        print("   Ширина поля - от 6 до 9   ")
        print("-----------------------------")
        print("      формат ввода: x y      ")
        print("      x - номер строки       ")
        print("      y - номер столбца      ")

    def print_boards(self):
        print("-" * 20)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 20)
        print("Доска компьютера:")
        print(self.ai.board)
        print("-" * 20)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.loop()


g = Game()
g.start()
