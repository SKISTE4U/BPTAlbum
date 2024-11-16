import os
import shutil
from PIL import Image, ExifTags
import re

def rename_files(directory):
    pattern = re.compile(r" \((\d+)\)\.jpg")
    for filename in os.listdir(directory):
        match = pattern.search(filename)
        if match:
            number = match.group(1)
            new_filename = f"{number}.jpg"
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            os.rename(old_file, new_file)
            print(f"Переименовано: {old_file} -> {new_file}")

def copy_files(source_directory, target_directories):
    # Получаем список всех файлов в исходной папке
    files = os.listdir(source_directory)
    for filename in files:
        source_file = os.path.join(source_directory, filename)
        # Копируем файл в каждую из целевых папок
        for target_directory in target_directories:
            target_file = os.path.join(target_directory, filename)
            shutil.copy2(source_file, target_file)
            print(f"Скопировано: {source_file} -> {target_file}")

def create_li(start,end):
    temp = ''
    start = start -1
    for x in range(start,end):
        temp += f'<li><img id="img_{x}" src="thumbs/{x+1}.jpg" data-image="{x+1}" alt="SAMPLE TEXT" onclick="OpenImage(this)"/></li> \n'
    open('temp.txt','w').write(temp)

def copy_and_resize_images(source_directory, image_directory, thumb_directory):
    # Получаем список всех файлов в исходной папке
    files = os.listdir(source_directory)
    for filename in files:
        source_file = os.path.join(source_directory, filename)

        # Проверяем, является ли файл изображением
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Копируем изображение в папку images
            image_target_file = os.path.join(image_directory, filename)
            shutil.copy2(source_file, image_target_file)
            print(f"Скопировано в images: {source_file} -> {image_target_file}")

            # Открываем изображение и уменьшаем его размер в два раза
            with Image.open(source_file) as img:

                try:
                    exif = img._getexif()
                    if exif:
                        for tag, value in exif.items():
                            if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'Orientation':
                                orientation = value
                                if orientation == 3:
                                    img = img.rotate(180, expand=True)
                                elif orientation == 6:
                                    img = img.rotate(270, expand=True)
                                elif orientation == 8:
                                    img = img.rotate(90, expand=True)
                                break
                except AttributeError:
                    pass

                new_size = (img.width, img.height)
                print(new_size)
                while new_size[0] > 1000 and new_size[1] > 1000:
                    new_size = (new_size[0] // 2, new_size[1] // 2)
                    print(new_size)
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Сохраняем уменьшенное изображение в папку thumbs
                thumb_target_file = os.path.join(thumb_directory, filename)
                resized_img.save(thumb_target_file)
                print(f"Скопировано и уменьшено в thumbs: {source_file} -> {thumb_target_file}")
        else:
            # Копируем файл, если он не является изображением
            image_target_file = os.path.join(image_directory, filename)
            thumb_target_file = os.path.join(thumb_directory, filename)
            shutil.copy2(source_file, image_target_file)
            shutil.copy2(source_file, thumb_target_file)
            print(f"Скопировано в images и thumbs: {source_file}")

def rename_jpg_files(directory):
    for filename in os.listdir(directory):
        # Проверяем, заканчивается ли файл на .JPG
        if filename.lower().endswith('.jpg') and filename.endswith('.JPG'):
            # Изменяем расширение на .jpg
            new_filename = filename[:-4] + '.jpg'
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            os.rename(old_file, new_file)
            print(f"Переименовано: {old_file} -> {new_file}")

# rename_files("images")
# rename_files("thumbs")

# copy_files("test", ["images", "thumbs"])

# create_li(66,112)

copy_and_resize_images('test','images','thumbs')

# rename_jpg_files('thumbs')
# rename_jpg_files('test')
# rename_jpg_files('images')