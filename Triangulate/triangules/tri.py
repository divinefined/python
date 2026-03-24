import math
import re
import os

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def distance_to(self, other):
        """Расстояние между двумя точками"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def __repr__(self):
        return f"Triangle({self.p1}, {self.p2}, {self.p3})"
    
    def area(self):
        """Вычисление площади треугольника по формуле Герона"""
        a = self.p1.distance_to(self.p2)
        b = self.p2.distance_to(self.p3)
        c = self.p3.distance_to(self.p1)

        # Проверяем, если одна из сторон имеет нулевую длину (треугольник вырожден)
        if a == 0 or b == 0 or c == 0:
            return 0
        
        s = (a + b + c) / 2  # полупериметр
        
        # Проверяем, что выражение для площади не дает отрицательное значение
        area = s * (s - a) * (s - b) * (s - c)
        if area <= 0:
            return 0  # Возвращаем 0, если выражение для площади приводит к некорректному результату

        # Возвращаем площадь, если все проверки пройдены
        return math.sqrt(area)
    
    # Реализация операторов сравнения
    def __lt__(self, other):
        return self.area() < other.area()
    
    def __le__(self, other):
        return self.area() <= other.area()
    
    def __eq__(self, other):
        return self.area() == other.area()
    
    def __ne__(self, other):
        return self.area() != other.area()
    
    def __gt__(self, other):
        return self.area() > other.area()
    
    def __ge__(self, other):
        return self.area() >= other.area()

def read_points_from_file(file_path):
    """Чтение точек из текстового файла (в формате [x,y][x,y]...)"""
    points = []
    with open(file_path, 'r') as file:
        data = file.read().strip()

        # Используем улучшенное регулярное выражение для поиска всех точек в формате [x,y]
        point_strings = re.findall(r'\[([-\d.]+),\s*([-\d.]+)\]', data)
        
        # Отладочный вывод
        print(f"Найдено точек: {len(point_strings)}")
        
        for point_str in point_strings:
            try:
                x, y = map(float, point_str)
                points.append(Point(x, y))
            except ValueError:
                print(f"Ошибка в точке: {point_str} - не удалось преобразовать в координаты.")
    
    # Отладочный вывод
    print(f"Точек после преобразования: {len(points)}")
    
    return points

def find_min_max_triangles(points):
    triangles = []
    n = len(points)
    
    if n < 3:
        print("Недостаточно точек для формирования треугольников.")
        return None, None
    
    # Генерация всех возможных треугольников
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                p1, p2, p3 = points[i], points[j], points[k]
                triangle = Triangle(p1, p2, p3)
                # Добавляем только те треугольники, которые имеют ненулевую площадь
                if triangle.area() > 0:
                    triangles.append(triangle)

    if not triangles:
        print("Не удалось сформировать треугольники.")
        return None, None

    # Находим треугольники с минимальной и максимальной площадью
    min_triangle = min(triangles, key=lambda t: t.area())
    max_triangle = max(triangles, key=lambda t: t.area())
    
    return min_triangle, max_triangle

# Путь к файлу с точками
file_path = os.path.join(os.path.dirname(__file__), 'plist.txt')

# Чтение точек из файла
points = read_points_from_file(file_path)

if not points:
    print("Нет данных о точках.")
else:
    # Находим треугольники с минимальной и максимальной площадью
    min_triangle, max_triangle = find_min_max_triangles(points)

    if min_triangle and max_triangle:
        # Выводим результат
        print(f"Треугольник с минимальной площадью: {min_triangle} (площадь: {min_triangle.area()})")
        print(f"Треугольник с максимальной площадью: {max_triangle} (площадь: {max_triangle.area()})")
