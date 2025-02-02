"""
Программа для создания изображений на основе TKinter.
"""
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    """
    Приложение для создания изображений с графическим интерфейсом TKinter.
    """
    def __init__(self, root, w: int = 600, h: int = 400, bg: str = "white"):
        """
        Конструктор приложения с графическим интерфейсом.
        :param root: Окно приложения.
        :param w: Ширина холста.
        :param h: Высота холста.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")  # Установка заголовка окна приложения.

        # Создание объекта изображения (виртуального холста).
        self.image = Image.new("RGB", (w, h), bg)

        # Инициализация объекта, позволяющего рисовать на объекте изображения (виртуальном холсте).
        self.draw = ImageDraw.Draw(self.image)

        # Создание виджета Canvas Tkinter, который отображает графический интерфейс для рисования.
        self.canvas = tk.Canvas(root, width=w, height=h, bg=bg)
        self.canvas.pack()

        # Размеры холста.
        self.sizes = (w, h)

        # Начальные значения
        self.last_x, self.last_y = None, None  # координат положения,
        self.brush_color = 'black'  # цвета кисти
        self.eraser_color = 'white'  # и цвета ластика.

        # Привязка обработчиков событий к холсту для отслеживания движений мыши при рисовании (<B1-Motion>)
        # и сброса состояния кисти при отпускании кнопки мыши (<ButtonRelease-1>).
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # Пипетка для выбора цвета с холста.
        self.canvas.bind('<Button-3>', self.pick_color)

        # Горячие клавиши для быстрых действий.
        self.root.bind('<Control-s>', self.save_image)  # Сохранить.
        self.root.bind('<Control-c>', self.choose_color)  # Выбрать цвет.

        # Настройка элементов управления интерфейса.
        self.setup_ui()

    def setup_ui(self):
        """
        Настройка элементов управления интерфейса.
        """
        # Создание панели управления.
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        # Создание кнопки «Сохранить».
        save_button = tk.Button(self.control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Создание кнопки «Очистить».
        clear_button = tk.Button(self.control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Создание кнопки «Выбрать цвет».
        color_button = tk.Button(self.control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Создание метки-образца текущего цвета кисти.
        self.brush_color_label = tk.Label(self.control_frame, bg=self.brush_color, height=1, width=3)
        self.brush_color_label.pack(side=tk.LEFT)

        # Объект StringVar, хранящий текущее значение размера кисти.
        self.brush_size = tk.StringVar(value='1')

        # Создание выпадающего списка для выбора размера кисти. Интервал выбора: [1, 10].
        # При изменении текущего значения, меняется и текущее значение слайдера.
        self.brush_size_option = tk.OptionMenu(self.control_frame, self.brush_size,
                                               *[str(i) for i in range(1, 11)], command=self.set_brush_size_scale)
        self.brush_size_option.pack(side=tk.LEFT)

        # Создание слайдера для изменения размера кисти в интервале [1, 10].
        # При изменении текущего значения, меняется и текущее значение выпадающего списка.
        self.brush_size_scale = tk.Scale(self.control_frame, from_=1, to=10, command=self.set_brush_size_option,
                                         orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        # Создание кнопки «Ластик».
        self.eraser_button = tk.Button(self.control_frame, text='Ластик', command=self.press_eraser, relief='raised')
        self.eraser_button.pack(side=tk.LEFT)

        # Создание метки-образца текущего цвета второй кисти (ластика).
        self.eraser_color_label = tk.Label(self.control_frame, bg=self.eraser_color, height=1, width=3)
        self.eraser_color_label.pack(side=tk.LEFT)

        # Создание кнопки «Текст».
        self.text_button = tk.Button(self.control_frame, text='Текст', command=self.ask_text)
        self.text_button.pack(side=tk.LEFT)

        # Создание кнопки «Размер холста».
        holst_size_button = tk.Button(self.control_frame, text='Размер холста', command=self.choose_holst_size)
        holst_size_button.pack(side=tk.RIGHT)

        # Создание кнопки «Изменить фон».
        change_background_button = tk.Button(self.control_frame, text='Изменить фон', command=self.change_background)
        change_background_button.pack(side=tk.RIGHT)

    def paint(self, event):
        """
        Рисование линии на холсте Tkinter и параллельно на объекте Image из Pillow.
        :param event: Событие <B1-Motion> содержит координаты мыши, которые используются для рисования.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, capstyle=tk.ROUND,
                                    fill=self.brush_color, smooth=tk.TRUE, width=int(self.brush_size.get()))
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

    def change_color(self):
        if self.eraser_button.config('relief')[-1] == 'raised':
            self.brush_color_label['bg'] = self.brush_color
        else:
            self.eraser_color_label['bg'] = self.brush_color

    def pick_color(self, event):
        """
        Пипетка для выбора цвета с холста.
        :param event: Событие <Button-3> означает взятие цвета с холста.
        """
        rgb = self.image.getpixel((event.x, event.y))
        self.brush_color = '#' + ''.join([f'{c:02X}' for c in rgb])
        self.change_color()

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

    def clear_canvas(self, bg: str = "white"):
        """
        Очистка холста (и объекта рисования).
        :param bg: Цвет фона.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", self.sizes, bg)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=self.sizes[0], height=self.sizes[1], bg=bg)

    def choose_color(self):
        """
        Изменение цвета кисти, используя стандартное диалоговое окно выбора цвета.
        """
        self.brush_color = colorchooser.askcolor(color=self.brush_color)[1]
        self.change_color()

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

    def press_eraser(self):
        """
        Нажатие на кнопку «Ластик».
        """
        if self.eraser_button.config('relief')[-1] == 'raised':
            # Включение ластика.
            self.eraser_button.config(relief='sunken')
        else:  # Выключение ластика.
            self.eraser_button.config(relief='raised')
        # Обмен цветами кисти и ластика.
        self.eraser_color, self.brush_color = self.brush_color, self.eraser_color

    def text_raised(self):
        """
        Возврат кнопки «Текст» в исходное состояние.
        """
        self.text_button.config(relief='raised')
        self.__delattr__('text')

    def add_text(self, event):
        """
        Добавление текста на изображение.
        :param event: Событие <B1-Motion> содержит координаты мыши, которые используются для вставки текста.
        """
        self.canvas.unbind('<Button-1>')
        self.draw.text((event.x, event.y), self.text, fill=self.brush_color)
        self.canvas.create_text(event.x, event.y, fill=self.brush_color, text=self.text)
        self.text_raised()

    def ask_text(self):
        """
        Запрос текста от пользователя.
        """
        self.text_button.config(relief='sunken')
        self.text = simpledialog.askstring('Ввод текста', 'Добавляемый текст:')
        if self.text:
            self.canvas.bind('<Button-1>', self.add_text)
        else:
            self.text_raised()

    def choose_holst_size(self):
        """
        Выбор размера холста.
        """
        title = 'Выбор размера холста'
        a = messagebox.askyesno(title, 'Рекомендуется сохранить текущее изображение перед сменой холста.\n'
                                       'Удалить текущее изображение?')
        if a:
            w = simpledialog.askinteger(title, 'Ширина нового холста:')
            if not w:  # Второй шанс возврата к холсту.
                return
            h = simpledialog.askinteger(title, 'Высота нового холста:')
            if not h:  # Третий шанс возврата к холсту.
                return

            self.sizes = (w, h)
            self.clear_canvas(self.canvas['bg'])

            # # Сохранение параметров.
            # bc = self.brush_color
            # ec = self.eraser_color
            # bs = self.brush_size
            #
            # self.control_frame.destroy()  # Уничтожение панели управления.
            # self.canvas.destroy()  # Уничтожение рабочей области.
            # self.__init__(self.root, w, h)  # Новая инициация.
            #
            # # Восстановление параметров.
            # self.brush_color_label['bg'] = self.brush_color = bc
            # self.eraser_color_label['bg'] = self.eraser_color = ec
            # self.brush_size_scale.set(int(bs.get()))
            # self.brush_size.set(str(self.brush_size_scale.get()))

    def change_background(self):
        """
        Изменение цвета фона.
        """
        title = 'Изменение цвета фона'
        a = messagebox.askyesnocancel(
            title,
            'Для сохранения нового фона в изображении нажмите «Да».\n'
            'Для смены фона холста без сохранения нового фона в изображении нажмите «Нет».\n'
            'Для отмены — «Отмена».'
        )
        if a:
            a = messagebox.askyesno(
                title,
                'Рекомендуется сохранить текущее изображение перед изменением цвета фона, т.к. произойдёт заливка.\n'
                'Удалить текущее изображение?'
            )
            if a:
                self.clear_canvas(colorchooser.askcolor()[1])
        elif a is False:
            self.canvas.config(bg=colorchooser.askcolor()[1])


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
