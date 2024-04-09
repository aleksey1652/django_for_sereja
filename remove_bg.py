import cv2
import numpy as np
from PIL import Image

def change_background_color(image_path, new_background_color, output_path):
    # Загрузка изображения
    image = cv2.imread(image_path)

    # Конвертация изображения из цветовой схемы BGR в RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Определение маски переднего плана на основе цветов
    lower_threshold = np.array([0, 0, 0], dtype=np.uint8)
    upper_threshold = np.array([70, 70, 70], dtype=np.uint8)
    foreground_mask = cv2.inRange(image_rgb, lower_threshold, upper_threshold)

    # Инвертирование маски переднего плана
    background_mask = cv2.bitwise_not(foreground_mask)

    # Применение нового цвета фона
    new_background = np.full(image.shape, new_background_color, dtype=np.uint8)
    new_background = cv2.bitwise_and(new_background, new_background, mask=background_mask)

    # Объединение переднего плана и нового фона
    result = cv2.bitwise_or(image, new_background)

    # Сохранение результата
    cv2.imwrite(output_path, result)

# Пример использования функции
#image_path = 'путь_к_фото.jpg'
#new_background_color = (0, 255, 0)  # Зеленый цвет фона (в формате RGB)
#output_path = 'путь_к_результату.jpg'

#change_background_color(image_path, new_background_color, output_path)



"""def replace_background_with_black(image_path, result_path):
    # Открываем изображение
    image = Image.open(image_path)

    # Создаем маску для замены фона (белый фон -> черный фон)
    mask = Image.new('L', image.size, color=0)

    # Создаем новое изображение, заменяя фон на черный с помощью маски
    result = Image.composite(image, Image.new('RGB', image.size, color=(0, 0, 0)), mask)

    # Сохраняем результат
    result.save(result_path)

# Пример использования
#replace_background_with_black('input.jpg')"""

#from PIL import Image
