import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 200
LINE_WIDTH = 8
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
X_COLOR = (0, 0, 0)
O_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 191, 255)
BUTTON_HOVER_COLOR = (0, 191, 200)
TEXT_COLOR = (255, 255, 255)

# Классы игры
class Board:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.draw_flag = False  # Переименованная переменная для флага ничьей

    def draw(self, screen):
        for row in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_HEIGHT), LINE_WIDTH)

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "X":
                    pygame.draw.line(screen, X_COLOR, (col * CELL_SIZE + 20, row * CELL_SIZE + 20), ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
                    pygame.draw.line(screen, X_COLOR, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20), (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
                elif self.board[row][col] == "O":
                    pygame.draw.circle(screen, O_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE * 6 // 15, LINE_WIDTH * 2 // 3)

    def mark_cell(self, row, col):
        if self.board[row][col] == "" and self.winner is None and not self.draw_flag:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
            elif self.check_draw():
                self.draw_flag = True
            self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        # Проверяем, все ли клетки заняты, и нет ли победителя
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":
                    return False  # Если есть пустая клетка, ничьей нет
        return True  # Если все клетки заняты и нет победителя, значит ничья

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.draw_flag = False  # Сброс флага ничьей

class Game:
    def __init__(self):
        self.board = Board()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Крестики-Нолики")
        self.font = pygame.font.SysFont("Arial", 20)
        self.reset_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40, 140, 30)  # Кнопка перезапуска

    def draw_text(self, text, color, position):
        label = self.font.render(text, True, color)
        self.screen.blit(label, position)

    def draw_reset_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.reset_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, self.reset_button_rect)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, self.reset_button_rect)

        self.draw_text("Перезапуск", TEXT_COLOR, (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 35))

    def handle_reset_button_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.reset_button_rect.collidepoint(mouse_x, mouse_y):
            self.board.reset()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill(WHITE)
            self.board.draw(self.screen)

            # Показываем сообщение в зависимости от результата
            if self.board.winner:
                self.draw_text(f"Победитель: {self.board.winner}", (0, 255, 0), (10, 10))
            elif self.board.draw_flag:
                self.draw_text("Ничья!", (255, 0, 0), (10, 10))
            else:
                self.draw_text(f"Ход игрока: {self.board.current_player}", (0, 191, 255), (10, 10))

            self.draw_reset_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    self.board.mark_cell(row, col)
                    self.handle_reset_button_click()  # Проверка клика на кнопку перезапуска

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()