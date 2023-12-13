from src.settings import SCREEN_SIZE, RESOURCES, COLORS, STATUSES
from src.state_machine import _State
import pygame as pg


class Game(_State):
    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    captured_pieces_white = []
    captured_pieces_black = []
    piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
    white_images = ["white_pawn", "white_queen", "white_king", "white_knight", "white_rook", "white_bishop"]
    black_images = ["black_pawn", "black_queen", "black_king", "black_knight", "black_rook", "black_bishop"]
    valid_moves = []

    counter = 0
    winner = ''
    game_over = False
    selection = 100

    def __init__(self):
        super().__init__()
        self.next = "MENU"
        self.timeout = 5
        self.alpha = 0
        self.alpha_speed = 2
        self.turn = 0  # 0 - White player, 1 - White player selected, 2 - Black player, 3 - Black Player selected
        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')

    def draw_pieces(self, surface):
        for i in range(len(self.white_pieces)):
            index = self.piece_list.index(self.white_pieces[i])
            if self.white_pieces[i] == 'pawn':
                surface.blit(RESOURCES["figures"]["white_pawn"],
                             (self.white_locations[i][0] * 100 + 22, self.white_locations[i][1] * 100 + 30))
            else:
                surface.blit(RESOURCES["figures"][self.white_images[index]],
                             (self.white_locations[i][0] * 100 + 10, self.white_locations[i][1] * 100 + 10))
            if self.turn < 2:
                if self.selection == i:
                    pg.draw.rect(surface, 'red',
                                 [self.white_locations[i][0] * 100 + 1, self.white_locations[i][1] * 100 + 1,
                                  100, 100], 2)

        for i in range(len(self.black_pieces)):
            index = self.piece_list.index(self.black_pieces[i])
            if self.black_pieces[i] == 'pawn':
                surface.blit(RESOURCES["figures"]["black_pawn"],
                             (self.black_locations[i][0] * 100 + 22, self.black_locations[i][1] * 100 + 30))
            else:
                surface.blit(RESOURCES["figures"][self.black_images[index]],
                             (self.black_locations[i][0] * 100 + 10, self.black_locations[i][1] * 100 + 10))
            if self.turn >= 2:
                if self.selection == i:
                    pg.draw.rect(surface, 'blue',
                                 [self.black_locations[i][0] * 100 + 1, self.black_locations[i][1] * 100 + 1,
                                  100, 100], 2)

    def draw_game_over(self, surface):
        pg.draw.rect(surface, 'black', [200, 200, 400, 70])
        surface.blit(RESOURCES["fonts"]["oswald"].render(f'{self.winner} won the game!', True, 'white'), (210, 210))
        surface.blit(RESOURCES["fonts"]["oswald"].render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

    def check_options(self, pieces, locations, turn):
        moves_list = []
        all_moves_list = []
        for i in range((len(pieces))):
            location = locations[i]
            piece = pieces[i]
            if piece == 'pawn':
                moves_list = self.check_pawn(location, turn)
            elif piece == 'rook':
                moves_list = self.check_rook(location, turn)
            elif piece == 'knight':
                moves_list = self.check_knight(location, turn)
            elif piece == 'bishop':
                moves_list = self.check_bishop(location, turn)
            elif piece == 'queen':
                moves_list = self.check_queen(location, turn)
            elif piece == 'king':
                moves_list = self.check_king(location, turn)
            all_moves_list.append(moves_list)
        return all_moves_list

    def check_king(self, position, color):
        moves_list = []
        if color == 'white':
            enemies_list = self.black_locations
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations

        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    def check_queen(self, position, color):
        moves_list = self.check_bishop(position, color)
        second_list = self.check_rook(position, color)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list

    def check_bishop(self, position, color):
        moves_list = []
        if color == 'white':
            enemies_list = self.black_locations
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations
        for i in range(4):  # up-right, up-left, down-right, down-left
            path = True
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

    def check_rook(self, position, color):
        moves_list = []
        if color == 'white':
            enemies_list = self.black_locations
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations
        for i in range(4):  # down, up, right, left
            path = True
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list

    def check_pawn(self, position, color):
        moves_list = []
        if color == 'white':
            if (position[0], position[1] + 1) not in self.white_locations and \
                    (position[0], position[1] + 1) not in self.black_locations and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in self.white_locations and \
                    (position[0], position[1] + 2) not in self.black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in self.black_locations:
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in self.black_locations:
                moves_list.append((position[0] - 1, position[1] + 1))
        else:
            if (position[0], position[1] - 1) not in self.white_locations and \
                    (position[0], position[1] - 1) not in self.black_locations and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in self.white_locations and \
                    (position[0], position[1] - 2) not in self.black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in self.white_locations:
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in self.white_locations:
                moves_list.append((position[0] - 1, position[1] - 1))
        return moves_list

    def check_knight(self, position, color):
        moves_list = []
        if color == 'white':
            enemies_list = self.black_locations
            friends_list = self.white_locations
        else:
            friends_list = self.black_locations
            enemies_list = self.white_locations

        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    def check_valid_moves(self):
        if self.turn < 2:
            options_list = self.white_options
        else:
            options_list = self.black_options
        valid_options = options_list[self.selection]
        return valid_options

    def draw_valid(self, moves, surface):
        if self.turn < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pg.draw.circle(surface, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

    def draw_captured(self, surface):
        for i in range(len(self.captured_pieces_white)):
            captured_piece = self.captured_pieces_white[i]
            index = self.piece_list.index(captured_piece)
            surface.blit(RESOURCES["figures"][self.black_images[index]], (825, 5 + 50 * i))
        for i in range(len(self.captured_pieces_black)):
            captured_piece = self.captured_pieces_black[i]
            index = self.piece_list.index(captured_piece)
            surface.blit(RESOURCES["figures"][self.white_images[index]], (925, 5 + 50 * i))

    def draw_check(self, surface):
        if self.turn < 2:
            if 'king' in self.white_pieces:
                king_index = self.white_pieces.index('king')
                king_location = self.white_locations[king_index]
                for i in range(len(self.black_options)):
                    if king_location in self.black_options[i]:
                        if self.counter < 15:
                            pg.draw.rect(surface, 'dark red', [self.white_locations[king_index][0] * 100 + 1,
                                                               self.white_locations[king_index][1] * 100 + 1, 100, 100],
                                         5)
        else:
            if 'king' in self.black_pieces:
                king_index = self.black_pieces.index('king')
                king_location = self.black_locations[king_index]
                for i in range(len(self.white_options)):
                    if king_location in self.white_options[i]:
                        if self.counter < 15:
                            pg.draw.rect(surface, 'dark blue', [self.black_locations[king_index][0] * 100 + 1,
                                                                self.black_locations[king_index][1] * 100 + 1, 100,
                                                                100],
                                         5)

    def draw_board(self, surface):
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pg.draw.rect(surface, COLORS["light_gray"], [600 - (column * 200), row * 100, 100, 100])
            else:
                pg.draw.rect(surface, COLORS["light_gray"], [700 - (column * 200), row * 100, 100, 100])
            pg.draw.rect(surface, COLORS["gray"], [0, 800, SCREEN_SIZE[0], 100])
            pg.draw.rect(surface, COLORS["gold"], [0, 800, SCREEN_SIZE[0], 100], 5)
            pg.draw.rect(surface, COLORS["gold"], [800, 0, 200, SCREEN_SIZE[1]], 5)
            surface.blit(RESOURCES["fonts"]["oswald"].render(STATUSES[self.turn], True, COLORS["black"]), (20, 820))
            for i in range(9):
                pg.draw.line(surface, COLORS["black"], (0, 100 * i), (800, 100 * i), 2)
                pg.draw.line(surface, COLORS["black"], (100 * i, 0), (100 * i, 800), 2)
            surface.blit(RESOURCES["fonts"]["oswald"].render('FORFEIT', True, 'black'), (810, 830))

    def update(self, keys, now):
        self.now = now
        self.alpha = min(self.alpha + self.alpha_speed, 255)

    def draw(self, surface, interpolate):
        if self.counter < 30:
            self.counter += 1
        else:
            self.counter = 0
        surface.fill('dark gray')
        self.draw_board(surface)
        self.draw_pieces(surface)
        self.draw_captured(surface)
        self.draw_check(surface)
        if self.selection != 100:
            self.valid_moves = self.check_valid_moves()
            self.draw_valid(self.valid_moves, surface)

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                if self.turn <= 1:
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        self.winner = 'black'
                    if click_coords in self.white_locations:
                        self.selection = self.white_locations.index(click_coords)
                        if self.turn == 0:
                            self.turn = 1
                    print(self.valid_moves)
                    if click_coords in self.valid_moves and self.selection != 100:
                        self.white_locations[self.selection] = click_coords
                        if click_coords in self.black_locations:
                            black_piece = self.black_locations.index(click_coords)
                            self.captured_pieces_white.append(self.black_pieces[black_piece])
                            if self.black_pieces[black_piece] == 'king':
                                self.winner = 'white'
                            self.black_pieces.pop(black_piece)
                            self.black_locations.pop(black_piece)
                        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                        self.turn = 2
                        self.selection = 100
                        self.valid_moves = []
                if self.turn > 1:
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        self.winner = 'white'
                    if click_coords in self.black_locations:
                        self.selection = self.black_locations.index(click_coords)
                        if self.turn == 2:
                            self.turn = 3
                    if click_coords in self.valid_moves and self.selection != 100:
                        self.black_locations[self.selection] = click_coords
                        if click_coords in self.white_locations:
                            white_piece = self.white_locations.index(click_coords)
                            self.captured_pieces_black.append(self.white_pieces[white_piece])
                            if self.white_pieces[white_piece] == 'king':
                                self.winner = 'black'
                            self.white_pieces.pop(white_piece)
                            self.white_locations.pop(white_piece)
                        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                        self.turn = 0
                        self.selection = 100
                        self.valid_moves = []
            if event.type == pg.KEYDOWN and self.game_over:
                if event.key == pg.K_RETURN:
                    self.game_over = False
                    self.winner = ''
                    self.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                         'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    self.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    self.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                         'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    self.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                            (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    self.captured_pieces_white = []
                    self.captured_pieces_black = []
                    self.turn = 0
                    self.selection = 100
                    self.valid_moves = []
                    self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                    self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')

        if self.winner != '':
            self.game_over = True
            self.draw_game_over(surface)

    def get_event(self, event):
        pass
