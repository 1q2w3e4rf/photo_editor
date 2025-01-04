import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk, ImageFilter, ImageEnhance

# Глобальные переменные
current_image = None
photo = None
editing_mode = False  # Новая глобальная переменная для отслеживания режима редактирования
points = []           # Список для хранения координат точек
lines = []            # Список для хранения линий между точками

# Функция для обновления изображения в интерфейсе
def update_display(image):
    global canvas, photo
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor='nw', image=photo)

# Открытие изображения
def open_image():
    global current_image, original_image
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            current_image = Image.open(file_path)
            original_image = current_image.copy()  # Сохраняем оригинальную копию
            update_display(current_image)
        except Exception as e:
            print(f"Ошибка при открытии изображения: {e}")

# Сохранение изображения
def save_image():
    global current_image, original_image
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        # Создаем копию оригинального изображения без временных изменений
        final_image = original_image.copy()
        
        # Применяем альфа-канал (маску) к финальному изображению
        if current_image.mode == 'RGBA':
            final_image.putalpha(current_image.split()[3])
            
        # Сохраняем финальное изображение
        final_image.save(file_path)

# Регулировка яркости
def adjust_brightness(value):
    global current_image
    enhancer = ImageEnhance.Brightness(current_image)
    adjusted_image = enhancer.enhance(float(value))
    update_display(adjusted_image)

# Регулировка насыщенности
def adjust_saturation(value):
    global current_image
    enhancer = ImageEnhance.Color(current_image)
    adjusted_image = enhancer.enhance(float(value))
    update_display(adjusted_image)

# Поворот изображения
def rotate_image(angle):
    global current_image
    rotated_image = current_image.rotate(int(angle))
    update_display(rotated_image)

# Наклон изображения влево/вправо
def tilt_image(direction):
    global current_image
    if direction == "left":
        tilted_image = current_image.transpose(Image.ROTATE_270)
    elif direction == "right":
        tilted_image = current_image.transpose(Image.ROTATE_90)
    else:
        tilted_image = current_image
    update_display(tilted_image)

# Настройка резкости
def sharpen_image(amount):
    global current_image
    sharpener = ImageEnhance.Sharpness(current_image)
    sharpened_image = sharpener.enhance(float(amount))
    update_display(sharpened_image)

# Размытие изображения
def blur_image(radius):
    global current_image
    blurred_image = current_image.filter(ImageFilter.GaussianBlur(radius=float(radius)))
    update_display(blurred_image)

# Удаление заднего фона изображения
def remove_background():
    global current_image
    cropped_image = current_image.crop(current_image.width // 2, current_image.height // 2)
    update_display(cropped_image)

# Функция для переключения режима редактирования
def reset_points_and_lines():
    global points, lines
    points.clear()
    lines.clear()

def toggle_editing():
    global editing_mode
    editing_mode = not editing_mode
    edit_button.config(text="Выход из режима редактирования" if editing_mode else "Режим редактирования")
    if not editing_mode:
        reset_points_and_lines()

# Функция для обработки нажатий мыши
def on_click(event):
    global points, lines
    if editing_mode:
        x, y = event.x, event.y
        points.append((x, y))
        if len(points) >= 2:
            lines.append((points[-2], points[-1]))
        draw_polygon()
        draw_point(x, y)

# Функция для рисования точки
def draw_point(x, y, r=5):
    canvas.create_oval(x-r, y-r, x+r, y+r, outline="red", fill="red")

# Функция для рисования многоугольника по точкам
def draw_polygon():
    global current_image, photo, canvas
    draw = ImageDraw.Draw(current_image)
    for line in lines:
        draw.line(line, fill=(255, 0, 0), width=2)
    update_display(current_image)

# Функция для применения маски и удаления фона
def apply_mask():
    global current_image, points
    if len(points) > 0:
        mask = Image.new('L', current_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(points, fill=255)
        current_image.putalpha(mask)
        update_display(current_image)
    
    # Очистка точек и линий после применения маски
    reset_points_and_lines()

# Инициализация главного окна приложения
root = tk.Tk()
root.title = "Редактор изображений"
# Рамка для параметров
params_frame = tk.Frame(root, bg="#333")
params_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Кнопка открытия изображения
open_button = tk.Button(params_frame, text="Открыть", command=open_image, font=("Arial", 12), fg="white", bg="#555")
open_button.pack(pady=10)

# Кнопка сохранения изображения
save_button = tk.Button(params_frame, text="Сохранить", command=save_image, font=("Arial", 12), fg="white", bg="#555")
save_button.pack(pady=10)

# Кнопка для входа/выхода из режима редактирования
edit_button = tk.Button(params_frame, text="Режим редактирования", command=toggle_editing, font=("Arial", 12), fg="white", bg="#555")
edit_button.pack(pady=10)

# Кнопка для применения маски
apply_button = tk.Button(params_frame, text="Применить маску", command=apply_mask, font=("Arial", 12), fg="white", bg="#555")
apply_button.pack(pady=10)

# Яркость
brightness_label = tk.Label(params_frame, text="Яркость:", font=("Arial", 14), fg="white", bg="#333")
brightness_label.pack(pady=5)
brightness_scale = tk.Scale(params_frame, from_=0.0, to=4.0, resolution=0.01, orient=tk.HORIZONTAL, length=150, command=adjust_brightness, bg="#444", fg="white", highlightthickness=0)
brightness_scale.set(1.0)
brightness_scale.pack(pady=5)

# Насыщенность
saturation_label = tk.Label(params_frame, text="Насыщенность:", font=("Arial", 14), fg="white", bg="#333")
saturation_label.pack(pady=5)
saturation_scale = tk.Scale(params_frame, from_=0.0, to=4.0, resolution=0.01, orient=tk.HORIZONTAL, length=150, command=adjust_saturation, bg="#444", fg="white", highlightthickness=0)
saturation_scale.set(1.0)
saturation_scale.pack(pady=5)

# Поворот изображения
rotate_label = tk.Label(params_frame, text="Поворот:", font=("Arial", 14), fg="white", bg="#333")
rotate_label.pack(pady=5)
rotate_entry = tk.Entry(params_frame, width=8, font=("Arial", 12), bg="#444", fg="white", insertbackground="white")
rotate_entry.insert(0, "90")
rotate_button = tk.Button(params_frame, text="Повернуть", command=lambda: rotate_image(rotate_entry.get()), font=("Arial", 12), fg="white", bg="#555")
rotate_button.pack(pady=5)

# Наклон изображения влево/вправо
tilt_label = tk.Label(params_frame, text="Наклонить:", font=("Arial", 14), fg="white", bg="#333")
tilt_label.pack(pady=5)
tilt_menu = tk.StringVar()
tilt_menu.set('Нет')
tilt_options = tk.OptionMenu(params_frame, tilt_menu, 'Влево', 'Вправо', command=tilt_image)
tilt_options.config(font=("Arial", 12), fg="white", activebackground="#666", highlightthickness=0)
tilt_options["menu"].config(bg="#444", fg="white", activebackground="#666")
tilt_options.pack(pady=5)

# Резкость
sharpen_label = tk.Label(params_frame, text="Резкость:", font=("Arial", 14), fg="white", bg="#333")
sharpen_label.pack(pady=5)
sharpen_scale = tk.Scale(params_frame, from_=0.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, length=150, command=sharpen_image, bg="#444", fg="white", highlightthickness=0)
sharpen_scale.set(1.0)
sharpen_scale.pack(pady=5)

# Размытие
blur_label = tk.Label(params_frame, text="Размытие:", font=("Arial", 14), fg="white", bg="#333")
blur_label.pack(pady=5)
blur_scale = tk.Scale(params_frame, from_=0.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, length=150, command=blur_image, bg="#444", fg="white", highlightthickness=0)
blur_scale.set(0.0)
blur_scale.pack(pady=5)

# Область для отображения изображения
canvas = tk.Canvas(root, width=700, height=500, bg="black")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Привязываем событие клика мыши
canvas.bind("<Button-1>", on_click)

# Запускаем главный цикл
root.mainloop()
