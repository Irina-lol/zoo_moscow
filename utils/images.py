from telegram import InputFile
import os


def get_animal_image(animal):
    image_path = f"data/images/{animal}.jpg"

    # Проверяем, существует ли файл
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Изображение для животного '{animal}' не найдено!")

    with open(image_path, "rb") as file:
        return InputFile(file)