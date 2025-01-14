# Приложение для создания изображений с графическим интерфейсом.

## ⚙ Зависимости

Разработка и тестирование производились на стеке:

![Static Badge](https://img.shields.io/badge/Python-3.12.7-3776AB)
![Static Badge](https://img.shields.io/badge/Pillow-11.0.0-black)

Установка библиотки:
```bash
pip install pillow
```

## 🖥 Использование

Запуск приложения производится командой
```bash
python main.py
```

### Панель управления

#### Очистить
Очистка холста.

#### Выбрать цвет
Изменение цвета кисти, используя стандартное диалоговое окно выбора цвета. По умолчанию цвет кисти чёрный.

#### Сохранить
Сохранение изображения, используя стандартное диалоговое окно сохранения файла.
Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.

#### Размер кисти
  * Выпадающий список<br>
    Установка текущего значения слайдера размера кисти, равного текущему значению выпадающего списка.
  * Слайдер<br>
    Установка текущего значения выпадающего списка размера кисти, равного текущему значению слайдера.
  
Оба элемента связаны между собой и работают синхронно.

#### Ластик
Активация/деактивация инструмента «Ластик».

По умолчанию при активации Ластика кисть меняет свой цвет на белый (цвет холста) и закрашивает (стирает) белым цветом.
Если изменить цвет кисти при активированном Ластике, то Ластик будет закрашивать выбранным цветом.
А при повторной активации выбранный цвет не сбросится. Это позволяет переключаться между двумя цветами.

### Пипетка
Для активации Пипетки достаточно навести курсор на пиксель холста, цвет которого требуется взять,
и нажать правую кнопку мыши. Цвет кисти заменится на цвет пикселя под курсором.

### Горячие клавиши для быстрых действий
`Ctrl+S` — сохранить,<br>
`Ctrl+C` — выбрать цвет.

<div align="center">

## Скриншоты
![20250114192705274.jpg](README_images/20250114192705274.jpg)<br>
Окно приложения с чистым холстом.

![20241228185332115.jpg](README_images/20241228185332115.jpg)<br>
Выпадающий список выбора размера кисти.

![20250104170531696.jpg](README_images/20250104170531696.jpg)<br>
Кнопка «Ластик» в активированном состоянии.
</div>
