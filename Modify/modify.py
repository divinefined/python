class My_list(list):
    def __init__(self, *args):
        # Передаем все аргументы в list
        super().__init__(args)

    def __sub__(self, other):
        if isinstance(other, My_list):
            return My_list(item for item in self if item not in other)
        else:
            return My_list(item - other for item in self)

    def __truediv__(self, divisor):
        if divisor == 0:
            raise ValueError("Division by zero is not allowed.")
        return My_list(item / divisor for item in self)

    def __str__(self):
        original_str = super().__str__()
        return f"My_list contains: {original_str}"

# Пример использования
l1 = My_list(1, 2, 3)  # Создаём объект My_list с несколькими аргументами
l2 = My_list(3, 4, 5)
l3 = l2 - l1
l4 = l1 - l2

print(l1 / 5)
print(l3)
print(l4)
