"""
Программа для создания изображений на основе TKinter.
"""
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    """
    Приложение для создания изображений с графическим интерфейсом TKinter.
    """
    def __init__(self, root):
        """
        Конструктор приложения с графическим интерфейсом.
        :param root: Окно приложения.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")  # Установка заголовка окна приложения.

        # Создание объекта изображения (виртуального холста).
        self.image = Image.new("RGB", (600, 400), "white")

        # Инициализация объекта, позволяющего рисовать на объекте изображения (виртуальном холсте).
        self.draw = ImageDraw.Draw(self.image)

        # Создание виджета Canvas Tkinter, который отображает графический интерфейс для рисования.
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Настройка элементов управления интерфейса.
        self.setup_ui()

        # Начальные значения…
        self.last_x, self.last_y = None, None  # координат положения…
        self.brush_color = 'black'  # и цвета кисти.

        # Привязка обработчиков событий к холсту для отслеживания движений мыши при рисовании (<B1-Motion>)
        # и сброса состояния кисти при отпускании кнопки мыши (<ButtonRelease-1>).
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        """
        Настройка элементов управления интерфейса.
        """
        # Создание панели управления.
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Создание кнопки «Очистить».
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Создание кнопки «Выбрать цвет».
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Создание кнопки «Сохранить».
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Объект StringVar, хранящий текущее значение размера кисти.
        self.brush_size = tk.StringVar(value='1')

        # Создание выпадающего списка для выбора размера кисти. Интервал выбора: [1, 10].
        # При изменении текущего значения, меняется и текущее значение слайдера.
        self.brush_size_option = tk.OptionMenu(control_frame, self.brush_size, *[str(i) for i in range(1, 11)],
                                               command=self.set_brush_size_scale)
        self.brush_size_option.pack(side=tk.LEFT)

        # Создание слайдера для изменения размера кисти в интервале [1, 10].
        # При изменении текущего значения, меняется и текущее значение выпадающего списка.
        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, command=self.set_brush_size_option,
                                         orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

    def paint(self, event):
        """
        Рисование линии на холсте Tkinter и параллельно на объекте Image из Pillow.
        :param event: Событие <B1-Motion> содержит координаты мыши, которые используются для рисования.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=int(self.brush_size.get()), fill=self.brush_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.brush_color,
                           width=int(self.brush_size.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сброс последних координат кисти.
        :param event: Событие <ButtonRelease-1> означает окончание рисования линии.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очистка холста (и объекта рисования).
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Изменение цвета кисти, используя стандартное диалоговое окно выбора цвета.
        """
        self.brush_color = colorchooser.askcolor(color=self.brush_color)[1]

    def save_image(self):
        """
        Сохранение изображения, используя стандартное диалоговое окно сохранения файла.
        Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def set_brush_size_scale(self, event):
        """
        Установка текущего значения слайдера размера кисти, равного текущему значению выпадающего списка.
        :param event: Событие.
        """
        self.brush_size_scale.set(int(self.brush_size.get()))

    def set_brush_size_option(self, event):
        """
        Установка текущего значения выпадающего списка размера кисти, равного текущему значению слайдера.
        :param event: Событие.
        """
        self.brush_size.set(str(self.brush_size_scale.get()))


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
