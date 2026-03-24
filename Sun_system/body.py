import pygame
import math

# Константы
WIDTH, HEIGHT = 1000, 800
SUN_RADIUS = 20

# Цвета
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Создание шрифта
font = pygame.font.Font(None, 30)

class Planet:
    def __init__(self, name, radius, distance, period, image_path):
        self.name = name
        self.radius = radius
        self.distance = distance
        self.period = period * 0.05
        self.angle = 0
        self.image = pygame.image.load(image_path)

    def update(self, dt):
        self.angle += (dt / self.period) * 2 * math.pi  
        if self.angle > 360:
            self.angle -= 360

    def draw(self, screen):
        scaled_image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        x = math.cos(math.radians(self.angle)) * self.distance + WIDTH / 2
        y = math.sin(math.radians(self.angle)) * self.distance + HEIGHT / 2
        screen.blit(scaled_image, (x - scaled_image.get_width() / 2, y - scaled_image.get_height() / 2))
    
    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - (WIDTH / 2 + self.distance * math.cos(math.radians(self.angle)))
        dy = mouse_y - (HEIGHT / 2 + self.distance * math.sin(math.radians(self.angle)))
        return math.sqrt(dx**2 + dy**2) <= self.radius

    def get_info(self):
        return f"Planet: {self.name}, Distance: {self.distance}, Angle: {self.angle}"


# Создание планет
planets = [
    Planet("Mercury", 2, 40, 88, 'mercury.png'),
    Planet("Venus", 4.4, 60, 224.7,  'venus.png'),
    Planet("Earth", 4.8, 80, 365.2, 'earth.png'),
    Planet("Mars", 2.4, 100, 686.98, 'mars.png'),
    Planet("Jupiter", 68.4, 190, 4332.59, 'jupiter.png'),
    Planet("Saturn", 48, 320, 10759.22, 'saturn.png'),
    Planet("Uranus", 19.6, 400, 30688.5, 'uranus.png'),
    Planet("Neptune", 5.2, 450, 60182, 'neptune.png'),
]

# Счетчик дней
day_count = 0

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление и отрисовка планет
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), SUN_RADIUS)
    for planet in planets:
        planet.update(clock.tick(600))
        planet.draw(screen)
        if planet.is_mouse_over():
            text = font.render(planet.get_info(), True, WHITE)
            screen.blit(text, (10, 10))

    # Вычисление текущего дня
    day_count = round(planets[2].angle / 360 * 365.2)

    # Вывод счетчика дней
    day_text = font.render(f"Day: {day_count}", True, WHITE)
    screen.blit(day_text, (10, 50))
    pygame.display.flip()

    print(planet)

pygame.quit()
