import pygame
import os
import sys
import subprocess
from tkinter import Tk, filedialog

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (30, 30, 30)
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10
FONT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (50, 50, 50)
SAVE_FOLDER = os.path.join(os.path.expanduser('~'), 'Documents', 'DHub')
SAVE_FILE = os.path.join(SAVE_FOLDER, 'list.txt')

# Инициализация Pygame
pygame.init()

# Установка иконки приложения
icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
if os.path.exists(icon_path):
    app_icon = pygame.image.load(icon_path)
    pygame.display.set_icon(app_icon)

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("DHub")

# Шрифт
font = pygame.font.Font(None, 36)

# Список exe файлов с их иконками
exe_list = []
scroll_offset = 0
remove_mode = False

# Создание папки, если она не существует
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Загрузка сохраненного списка
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, 'r') as file:
        for line in file.readlines():
            parts = line.strip().split('|')
            if len(parts) == 2:
                exe_list.append(parts)
            elif len(parts) == 1:
                exe_list.append([parts[0], ""])  # Иконка не задана

# Функция для выбора exe файла
def select_exe():
    root = Tk()
    root.withdraw()
    exe_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
    if exe_path:
        ico_path = filedialog.askopenfilename(filetypes=[("Icon or Image Files", "*.ico *.png")])
        if exe_path not in [item[0] for item in exe_list]:
            exe_list.append([exe_path, ico_path if ico_path else ""])
    root.destroy()

# Основной цикл
running = True
while running:
    screen.fill(BG_COLOR)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:  # Левая кнопка мыши
                # Проверка нажатия на кнопку "Add EXE"
                if 10 <= mouse_x <= 200 and 10 <= mouse_y <= 60:
                    select_exe()

                # Проверка нажатия на кнопку "Remove"
                if 220 <= mouse_x <= 410 and 10 <= mouse_y <= 60:
                    remove_mode = not remove_mode

                # Проверка нажатия на элементы списка
                y = 80 - scroll_offset
                for exe_path, ico_path in exe_list:
                    if 10 <= mouse_x <= WINDOW_WIDTH - 20 and y <= mouse_y <= y + BUTTON_HEIGHT:
                        if remove_mode:
                            exe_list.remove([exe_path, ico_path])
                        else:
                            subprocess.Popen(exe_path, shell=True)
                        break
                    y += BUTTON_HEIGHT + BUTTON_MARGIN

            elif event.button == 4:  # Прокрутка вверх
                scroll_offset = max(scroll_offset - 20, 0)
            elif event.button == 5:  # Прокрутка вниз
                scroll_offset += 20

    # Отрисовка кнопки "Add EXE"
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (10, 10, 190, 50))
    add_text = font.render("Add EXE", True, FONT_COLOR)
    screen.blit(add_text, (20, 20))

    # Отрисовка кнопки "Remove"
    remove_color = (200, 50, 50) if remove_mode else HIGHLIGHT_COLOR
    pygame.draw.rect(screen, remove_color, (220, 10, 190, 50))
    remove_text = font.render("Remove", True, FONT_COLOR)
    screen.blit(remove_text, (230, 20))

    # Отрисовка списка exe
    y = 80 - scroll_offset
    for exe_path, ico_path in exe_list:
        exe_name = os.path.splitext(os.path.basename(exe_path))[0]
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (10, y, WINDOW_WIDTH - 20, BUTTON_HEIGHT))

        # Загрузка иконки
        if ico_path and os.path.exists(ico_path):
            try:
                icon = pygame.image.load(ico_path)
                icon = pygame.transform.scale(icon, (30, 30))
                screen.blit(icon, (20, y + 10))
            except pygame.error:
                pass

        # Отображение имени EXE файла
        exe_text = font.render(exe_name, True, FONT_COLOR)
        screen.blit(exe_text, (60, y + 10))
        y += BUTTON_HEIGHT + BUTTON_MARGIN

    # Обновление экрана
    pygame.display.flip()

# Сохранение списка при выходе
with open(SAVE_FILE, 'w') as file:
    for exe_path, ico_path in exe_list:
        file.write(f"{exe_path}|{ico_path}\n")

# Завершение Pygame
pygame.quit()
sys.exit()
