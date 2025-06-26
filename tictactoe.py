import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 900
BOARD_SIZE = 600
BOARD_PADDING = 50

BACKGROUND = (25, 30, 45)
GRID_COLOR = (70, 130, 180)
X_COLOR = (220, 20, 60) 
O_COLOR = (50, 205, 50) 
TEXT_COLOR = (240, 248, 255) 
BUTTON_COLOR = (65, 105, 225) 
BUTTON_HOVER = (100, 149, 237)  
WIN_LINE = (255, 215, 0)  

BOARD_EMPTY = 0
BOARD_PLAYER_X = 1
BOARD_PLAYER_O = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

title_font = pygame.font.SysFont("arial", 60, bold=True)
status_font = pygame.font.SysFont("arial", 40)
button_font = pygame.font.SysFont("arial", 35)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 3, border_radius=15)
        
        text_surface = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def draw_board():

    screen.fill(BACKGROUND)
    
    title = title_font.render("TIC TAC TOE", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
    board_rect = pygame.Rect(
        (WIDTH - BOARD_SIZE) // 2,
        (HEIGHT - BOARD_SIZE) // 2 - 20,
        BOARD_SIZE,
        BOARD_SIZE
    )
    pygame.draw.rect(screen, (40, 45, 60), board_rect, border_radius=15)
    cell_size = BOARD_SIZE // 3
    for i in range(1, 3):
        pygame.draw.line(
            screen, GRID_COLOR,
            (board_rect.left + i * cell_size, board_rect.top + 15),
            (board_rect.left + i * cell_size, board_rect.bottom - 15),
            10
        )
        pygame.draw.line(
            screen, GRID_COLOR,
            (board_rect.left + 15, board_rect.top + i * cell_size),
            (board_rect.right - 15, board_rect.top + i * cell_size),
            10
        )

def draw_figures(board):
    cell_size = BOARD_SIZE // 3
    board_rect = pygame.Rect(
        (WIDTH - BOARD_SIZE) // 2,
        (HEIGHT - BOARD_SIZE) // 2 - 20,
        BOARD_SIZE,
        BOARD_SIZE
    )
    
    for row in range(3):
        for col in range(3):
            index = row * 3 + col
            center_x = board_rect.left + col * cell_size + cell_size // 2
            center_y = board_rect.top + row * cell_size + cell_size // 2
            
            if board[index] == BOARD_PLAYER_X:
                size = cell_size // 3
                pygame.draw.line(screen, X_COLOR, 
                                (center_x - size, center_y - size),
                                (center_x + size, center_y + size), 15)
                pygame.draw.line(screen, X_COLOR, 
                                (center_x + size, center_y - size),
                                (center_x - size, center_y + size), 15)
                
            elif board[index] == BOARD_PLAYER_O:
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), cell_size // 3, 12)

def draw_status(message):
    text = status_font.render(message, True, TEXT_COLOR)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 150))

def player(board):
    """Determine current player (X or O) based on moves made."""
    x_count = sum(1 for cell in board if cell == BOARD_PLAYER_X)
    o_count = sum(1 for cell in board if cell == BOARD_PLAYER_O)
    return BOARD_PLAYER_X if x_count == o_count else BOARD_PLAYER_O

def terminal(board):
    """Check if game is over. Return winner (X/O), 0 for tie, or None if ongoing."""
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != BOARD_EMPTY:
            return board[i]

    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != BOARD_EMPTY:
            return board[i]
    if board[0] == board[4] == board[8] != BOARD_EMPTY:
        return board[0]
    if board[2] == board[4] == board[6] != BOARD_EMPTY:
        return board[2]
    

    if BOARD_EMPTY not in board:
        return 0 
    
    return None 

def minimax(board):
    """AI move using a smarter strategy."""
    valid_moves = [i for i, cell in enumerate(board) if cell == BOARD_EMPTY]

    if not valid_moves:
        return None

    for move in valid_moves:
        test_board = board.copy()
        test_board[move] = BOARD_PLAYER_O
        if terminal(test_board) == BOARD_PLAYER_O:
            return move

    for move in valid_moves:
        test_board = board.copy()
        test_board[move] = BOARD_PLAYER_X
        if terminal(test_board) == BOARD_PLAYER_X:
            return move

    if 4 in valid_moves:
        return 4

    corners = [0, 2, 6, 8]
    corner_moves = [m for m in corners if m in valid_moves]
    if corner_moves:
        return random.choice(corner_moves)

    sides = [1, 3, 5, 7]
    side_moves = [m for m in sides if m in valid_moves]
    if side_moves:
        return random.choice(side_moves)

    return random.choice(valid_moves)

def draw_winning_line(board):
    board_rect = pygame.Rect(
        (WIDTH - BOARD_SIZE) // 2,
        (HEIGHT - BOARD_SIZE) // 2 - 20,
        BOARD_SIZE,
        BOARD_SIZE
    )
    cell_size = BOARD_SIZE // 3

    for row in range(3):
        if board[row*3] == board[row*3+1] == board[row*3+2] != BOARD_EMPTY:
            start_x = board_rect.left + cell_size // 2
            end_x = board_rect.right - cell_size // 2
            y = board_rect.top + row * cell_size + cell_size // 2
            pygame.draw.line(screen, WIN_LINE, (start_x, y), (end_x, y), 15)
            return
    
    for col in range(3):
        if board[col] == board[col+3] == board[col+6] != BOARD_EMPTY:
            start_y = board_rect.top + cell_size // 2
            end_y = board_rect.bottom - cell_size // 2
            x = board_rect.left + col * cell_size + cell_size // 2
            pygame.draw.line(screen, WIN_LINE, (x, start_y), (x, end_y), 15)
            return

    if board[0] == board[4] == board[8] != BOARD_EMPTY:
        pygame.draw.line(screen, WIN_LINE, 
                        (board_rect.left + cell_size // 2, board_rect.top + cell_size // 2),
                        (board_rect.right - cell_size // 2, board_rect.bottom - cell_size // 2), 
                        15)
        return
    if board[2] == board[4] == board[6] != BOARD_EMPTY:
        pygame.draw.line(screen, WIN_LINE, 
                        (board_rect.right - cell_size // 2, board_rect.top + cell_size // 2),
                        (board_rect.left + cell_size // 2, board_rect.bottom - cell_size // 2), 
                        15)

def main():
    board = [BOARD_EMPTY] * 9
    game_over = False
    winner = None
    player_turn = BOARD_PLAYER_X
    message = "Your Turn (X)"
    
    reset_button = Button(WIDTH//2 - 120, HEIGHT - 90, 240, 60, "New Game")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if reset_button.is_clicked(mouse_pos, event):

                board = [BOARD_EMPTY] * 9
                game_over = False
                winner = None
                player_turn = BOARD_PLAYER_X
                message = "Your Turn (X)"
            
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and player_turn == BOARD_PLAYER_X:
                mouseX, mouseY = mouse_pos

                board_rect = pygame.Rect(
                    (WIDTH - BOARD_SIZE) // 2,
                    (HEIGHT - BOARD_SIZE) // 2 - 20,
                    BOARD_SIZE,
                    BOARD_SIZE
                )
                
                if board_rect.collidepoint(mouseX, mouseY):
                    col = (mouseX - board_rect.left) // (BOARD_SIZE // 3)
                    row = (mouseY - board_rect.top) // (BOARD_SIZE // 3)
                    idx = row * 3 + col
                    
                    if 0 <= idx < 9 and board[idx] == BOARD_EMPTY:
                        board[idx] = BOARD_PLAYER_X
                        player_turn = BOARD_PLAYER_O
                        message = "Computer's Turn (O)"
                        
                        winner = terminal(board)
                        if winner is not None:
                            game_over = True
                            if winner == BOARD_PLAYER_X:
                                message = "You Win!"
                            elif winner == BOARD_PLAYER_O:
                                message = "Computer Wins!"
                            else:
                                message = "It's a Tie!"
        

        if not game_over and player_turn == BOARD_PLAYER_O:
            pygame.time.delay(500)
            move = minimax(board)
            if move is not None:
                board[move] = BOARD_PLAYER_O
                player_turn = BOARD_PLAYER_X
                message = "Your Turn (X)"

                winner = terminal(board)
                if winner is not None:
                    game_over = True
                    if winner == BOARD_PLAYER_X:
                        message = "You Win!"
                    elif winner == BOARD_PLAYER_O:
                        message = "Computer Wins!"
                    else:
                        message = "It's a Tie!"

        draw_board()
        draw_figures(board)

        if winner in [BOARD_PLAYER_X, BOARD_PLAYER_O]:
            draw_winning_line(board)
        
        draw_status(message)
        
        reset_button.check_hover(mouse_pos)
        reset_button.draw()
        
        pygame.display.update()

if __name__ == "__main__":
    main()
