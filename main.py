# main.py - Оптимизированная версия для Android
import pygame
import random
import sys
import math

# Инициализация PyGame
pygame.init()

# Автоматическое определение размера экрана
try:
    info = pygame.display.Info()
    SCREEN_WIDTH = min(info.current_w, 1200)
    SCREEN_HEIGHT = min(info.current_h, 800)
except:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

print(f"Экран: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

# Адаптивные настройки
GRID_SIZE = 8
CELL_SIZE = min(45, SCREEN_HEIGHT // 15)
MARGIN = 10

class SeaBattle:
    def __init__(self):
        # Создаем окно
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Морской Бой")
        
        # Шрифты
        self.big_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Игровые поля
        self.player_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ai_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Корабли
        self.player_ships = []
        self.ai_ships = []
        
        # Состояние игры
        self.state = "setup"  # setup, player_turn, ai_turn, game_over
        self.player_hits = 0
        self.ai_hits = 0
        self.turns = 0
        self.selected_ship = None
        self.ship_orientation = 'h'
        
        # Расстановка
        self.setup_game()
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        print("Игра 'Морской Бой' запущена!")
        print("Режим: Расстановка кораблей")
    
    def setup_game(self):
        """Начальная настройка игры"""
        # Очищаем поля
        self.player_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ai_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_ships = []
        self.ai_ships = []
        
        # Упрощенные корабли для мобильной версии
        ship_sizes = [3, 2, 2, 1, 1, 1]
        
        # Автоматическая расстановка кораблей ИИ
        for size in ship_sizes:
            self.place_ship_random(self.ai_grid, self.ai_ships, size)
        
        self.state = "setup"
        self.message = "Выберите и расставьте корабли"
    
    def place_ship_random(self, grid, ships, size):
        """Случайная расстановка корабля"""
        placed = False
        attempts = 0
        
        while not placed and attempts < 100:
            orientation = random.choice(['h', 'v'])
            
            if orientation == 'h':
                max_x = GRID_SIZE - size
                x = random.randint(0, max_x if max_x > 0 else 0)
                y = random.randint(0, GRID_SIZE - 1)
            else:
                max_y = GRID_SIZE - size
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, max_y if max_y > 0 else 0)
            
            # Проверка возможности
            can_place = True
            positions = []
            
            for i in range(size):
                if orientation == 'h':
                    px = x + i
                    py = y
                else:
                    px = x
                    py = y + i
                
                if not (0 <= px < GRID_SIZE and 0 <= py < GRID_SIZE):
                    can_place = False
                    break
                
                # Проверяем клетку и соседей
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = px + dx, py + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            if grid[ny][nx] != 0:
                                can_place = False
                                break
                    if not can_place:
                        break
                
                if not can_place:
                    break
                
                positions.append((px, py))
            
            if can_place:
                # Размещаем корабль
                for px, py in positions:
                    grid[py][px] = size  # Храним размер для отображения
                ships.append((size, positions))
                placed = True
            
            attempts += 1
    
    def can_place_player_ship(self, x, y, size, orientation):
        """Проверка возможности размещения корабля игроком"""
        positions = []
        
        for i in range(size):
            if orientation == 'h':
                px = x + i
                py = y
            else:
                px = x
                py = y + i
            
            if not (0 <= px < GRID_SIZE and 0 <= py < GRID_SIZE):
                return False, []
            
            # Проверяем клетку и соседей
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = px + dx, py + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if self.player_grid[ny][nx] != 0:
                            return False, []
            
            positions.append((px, py))
        
        return True, positions
    
    def place_player_ship(self, x, y, size, orientation):
        """Размещение корабля игрока"""
        can_place, positions = self.can_place_player_ship(x, y, size, orientation)
        
        if can_place:
            for px, py in positions:
                self.player_grid[py][px] = size
            
            self.player_ships.append((size, positions))
            return True
        
        return False
    
    def draw_grid(self, grid, x, y, show_ships=False):
        """Отрисовка игрового поля"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(
                    x + col * CELL_SIZE,
                    y + row * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                
                # Фон клетки
                pygame.draw.rect(self.screen, (40, 40, 70), rect)
                
                # Граница
                pygame.draw.rect(self.screen, (80, 130, 180), rect, 2)
                
                # Содержимое клетки
                cell = grid[row][col]
                
                if cell > 0 and show_ships:
                    # Корабль (цвет зависит от размера)
                    colors = {
                        1: (100, 100, 150),
                        2: (120, 120, 170),
                        3: (140, 140, 190),
                        4: (160, 160, 210)
                    }
                    color = colors.get(cell, (100, 100, 150))
                    inner = rect.inflate(-8, -8)
                    pygame.draw.rect(self.screen, color, inner, border_radius=4)
                
                elif cell == -1:  # Промах
                    pygame.draw.circle(self.screen, (180, 180, 220), rect.center, 8)
                
                elif cell == -2:  # Попадание
                    pygame.draw.circle(self.screen, (220, 60, 60), rect.center, 10)
                    # Крестик
                    pygame.draw.line(self.screen, (255, 255, 255),
                                    (rect.left + 6, rect.top + 6),
                                    (rect.right - 6, rect.bottom - 6), 3)
                    pygame.draw.line(self.screen, (255, 255, 255),
                                    (rect.right - 6, rect.top + 6),
                                    (rect.left + 6, rect.bottom - 6), 3)
    
    def draw(self):
        """Отрисовка всей игры"""
        # Фон
        self.screen.fill((25, 25, 45))
        
        # Заголовок
        title = self.big_font.render("МОРСКОЙ БОЙ", True, (100, 150, 255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        # Сообщение
        msg = self.font.render(self.message, True, (255, 255, 255))
        self.screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 80))
        
        # Поле игрока
        player_label = self.font.render("ВАШИ КОРАБЛИ", True, (150, 200, 255))
        player_x = SCREEN_WIDTH // 4 - player_label.get_width() // 2
        self.screen.blit(player_label, (player_x, 120))
        
        player_grid_x = SCREEN_WIDTH // 4 - (GRID_SIZE * CELL_SIZE) // 2
        player_grid_y = 160
        self.draw_grid(self.player_grid, player_grid_x, player_grid_y, show_ships=True)
        
        # Поле компьютера (если игра начата)
        if self.state != "setup":
            ai_label = self.font.render("КОМПЬЮТЕР", True, (255, 150, 150))
            ai_x = 3 * SCREEN_WIDTH // 4 - ai_label.get_width() // 2
            self.screen.blit(ai_label, (ai_x, 120))
            
            ai_grid_x = 3 * SCREEN_WIDTH // 4 - (GRID_SIZE * CELL_SIZE) // 2
            ai_grid_y = 160
            self.draw_grid(self.ai_grid, ai_grid_x, ai_grid_y, show_ships=False)
        
        # Кнопки
        self.draw_buttons()
        
        # Статистика
        if self.state != "setup":
            stats = f"Вы: {self.player_hits} | Компьютер: {self.ai_hits}"
            stats_text = self.small_font.render(stats, True, (255, 255, 200))
            self.screen.blit(stats_text, (SCREEN_WIDTH//2 - stats_text.get_width()//2, 400))
    
    def draw_buttons(self):
        """Отрисовка кнопок управления"""
        button_height = 50
        
        if self.state == "setup":
            # Кнопка "Начать игру"
            start_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 450, 200, button_height)
            pygame.draw.rect(self.screen, (60, 160, 60), start_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), start_rect, 2, border_radius=8)
            start_text = self.font.render("НАЧАТЬ ИГРУ", True, (255, 255, 255))
            self.screen.blit(start_text, (start_rect.centerx - start_text.get_width()//2,
                                         start_rect.centery - start_text.get_height()//2))
            
            # Кнопка "Авторасстановка"
            auto_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 520, 200, button_height)
            pygame.draw.rect(self.screen, (80, 120, 200), auto_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), auto_rect, 2, border_radius=8)
            auto_text = self.font.render("АВТОРАССТАНОВКА", True, (255, 255, 255))
            self.screen.blit(auto_text, (auto_rect.centerx - auto_text.get_width()//2,
                                        auto_rect.centery - auto_text.get_height()//2))
        else:
            # Кнопка "Новая игра"
            new_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, 150, button_height)
            pygame.draw.rect(self.screen, (60, 100, 160), new_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255), new_rect, 2, border_radius=8)
            new_text = self.font.render("НОВАЯ", True, (255, 255, 255))
            self.screen.blit(new_text, (new_rect.centerx - new_text.get_width()//2,
                                       new_rect.centery - new_text.get_height()//2))
        
        # Кнопка "Выход"
        exit_rect = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 70, 150, button_height)
        pygame.draw.rect(self.screen, (160, 60, 60), exit_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), exit_rect, 2, border_radius=8)
        exit_text = self.font.render("ВЫХОД", True, (255, 255, 255))
        self.screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()//2,
                                    exit_rect.centery - exit_text.get_height()//2))
    
    def handle_click(self, pos):
        """Обработка кликов"""
        x, y = pos
        
        if self.state == "setup":
            # Проверяем кнопки
            if SCREEN_WIDTH//2 - 100 <= x <= SCREEN_WIDTH//2 + 100:
                if 450 <= y <= 500:  # Кнопка "Начать игру"
                    if len(self.player_ships) >= 6:  # Проверяем, что все корабли расставлены
                        self.state = "player_turn"
                        self.message = "Ваш ход! Стреляйте по компьютеру"
                        print("Игра начата!")
                    else:
                        self.message = f"Расставьте все корабли! ({len(self.player_ships)}/6)"
                
                elif 520 <= y <= 570:  # Кнопка "Авторасстановка"
                    self.setup_game()
                    # Автоматически расставляем корабли игрока
                    ship_sizes = [3, 2, 2, 1, 1, 1]
                    for size in ship_sizes:
                        self.place_ship_random(self.player_grid, self.player_ships, size)
                    self.message = "Корабли расставлены автоматически"
                    print("Корабли расставлены автоматически")
            
            # Поле игрока для расстановки
            player_grid_x = SCREEN_WIDTH // 4 - (GRID_SIZE * CELL_SIZE) // 2
            player_grid_y = 160
            
            if (player_grid_x <= x <= player_grid_x + GRID_SIZE * CELL_SIZE and
                player_grid_y <= y <= player_grid_y + GRID_SIZE * CELL_SIZE):
                
                grid_x = (x - player_grid_x) // CELL_SIZE
                grid_y = (y - player_grid_y) // CELL_SIZE
                
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    if self.selected_ship:
                        # Пытаемся разместить выбранный корабль
                        size = self.selected_ship
                        if self.place_player_ship(grid_x, grid_y, size, self.ship_orientation):
                            print(f"Корабль размером {size} размещен")
                            self.selected_ship = None
                        else:
                            self.message = "Нельзя разместить здесь!"
                    else:
                        # Проверяем, есть ли здесь корабль для удаления
                        if self.player_grid[grid_y][grid_x] > 0:
                            # Удаляем корабль
                            for ship in self.player_ships[:]:
                                size, positions = ship
                                if (grid_x, grid_y) in positions:
                                    self.player_ships.remove(ship)
                                    for px, py in positions:
                                        self.player_grid[py][px] = 0
                                    print(f"Корабль размером {size} удален")
                                    break
        
        elif self.state == "player_turn":
            # Поле компьютера для стрельбы
            ai_grid_x = 3 * SCREEN_WIDTH // 4 - (GRID_SIZE * CELL_SIZE) // 2
            ai_grid_y = 160
            
            if (ai_grid_x <= x <= ai_grid_x + GRID_SIZE * CELL_SIZE and
                ai_grid_y <= y <= ai_grid_y + GRID_SIZE * CELL_SIZE):
                
                grid_x = (x - ai_grid_x) // CELL_SIZE
                grid_y = (y - ai_grid_y) // CELL_SIZE
                
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    # Стрельба
                    if self.ai_grid[grid_y][grid_x] > 0:  # Попадание
                        self.ai_grid[grid_y][grid_x] = -2
                        self.player_hits += 1
                        self.message = "Попадание! Стреляйте снова"
                        print(f"Попадание в ({grid_x}, {grid_y})")
                        
                        # Проверяем победу
                        if self.player_hits >= sum(size for size, _ in self.ai_ships):
                            self.state = "game_over"
                            self.message = "ВЫ ПОБЕДИЛИ!"
                            print("Игрок победил!")
                    else:  # Промах
                        self.ai_grid[grid_y][grid_x] = -1
                        self.state = "ai_turn"
                        self.message = "Промах. Ход компьютера..."
                        print(f"Промах в ({grid_x}, {grid_y})")
        
        # Кнопка "Новая игра"
        if 50 <= x <= 200 and SCREEN_HEIGHT - 70 <= y <= SCREEN_HEIGHT - 20:
            self.setup_game()
            print("Новая игра")
        
        # Кнопка "Выход"
        if SCREEN_WIDTH - 200 <= x <= SCREEN_WIDTH - 50 and SCREEN_HEIGHT - 70 <= y <= SCREEN_HEIGHT - 20:
            return False
        
        return True
    
    def ai_turn(self):
        """Ход компьютера"""
        # Ищем случайную свободную клетку
        empty_cells = []
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.player_grid[y][x] >= 0:  # Еще не стреляли
                    empty_cells.append((x, y))
        
        if empty_cells:
            x, y = random.choice(empty_cells)
            
            if self.player_grid[y][x] > 0:  # Попадание
                self.player_grid[y][x] = -2
                self.ai_hits += 1
                self.state = "ai_turn"  # Компьютер ходит снова
                self.message = "Компьютер попал! Он ходит снова..."
                print(f"Компьютер попал в ({x}, {y})")
                
                # Проверяем победу ИИ
                if self.ai_hits >= sum(size for size, _ in self.player_ships):
                    self.state = "game_over"
                    self.message = "КОМПЬЮТЕР ПОБЕДИЛ!"
                    print("Компьютер победил!")
            else:  # Промах
                self.player_grid[y][x] = -1
                self.state = "player_turn"
                self.message = "Компьютер промахнулся. Ваш ход!"
                print(f"Компьютер промахнулся в ({x}, {y})")
    
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        if not self.handle_click(event.pos):
                            self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.state == "setup":
                        # Поворот корабля
                        self.ship_orientation = 'v' if self.ship_orientation == 'h' else 'h'
                        print(f"Ориентация: {'вертикальная' if self.ship_orientation == 'v' else 'горизонтальная'}")
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4] and self.state == "setup":
                        # Выбор корабля цифрами
                        sizes = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}
                        self.selected_ship = sizes.get(event.key)
                        if self.selected_ship:
                            print(f"Выбран корабль размером {self.selected_ship}")
            
            # Ход компьютера
            if self.state == "ai_turn":
                pygame.time.delay(1000)  # Пауза для наглядности
                self.ai_turn()
            
            # Отрисовка
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("=" * 50)
    print("ЗАПУСК МОРСКОГО БОЯ")
    print("=" * 50)
    
    try:
        game = SeaBattle()
        game.run()
    except Exception as e:
        print(f"\nОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")