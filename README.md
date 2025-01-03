# Построение нотной грамоты на основе видеоряда игры на пианино
## Цель:

Разработать алгоритм, который будет строить нотную грамоту (табулатуру) используя только видеоряд игры на пианино.
## Краткий обзор проекта:
### Входные данные (Inputs):
- видеоряд игры на пианино
### Выходные данные (Outputs):
- нотная грамота (табулатура), но на данный момент реализован только выходной набор данных
с информацией о времени нажатия и отпускания для каждой клавиши.
### работа алгоритма основана на нескольких этапах:
- на первом этапе создаем карту разметки центров каждой реальной клавиши (черной или белой) - файл marking_buttons.py
- далее каждый кадр видеоряда проходит предобработку различными фильтрами, после чего производится
определение границ каждого визуального эффекта для клавиш (светящиеся клавиши) - файл track_frame.py
- после определения границ заполняется набор данных data_frame (словарь, ключи - номера клавиш,
значения - номер кадра нажатия и номер кадра отпускания данной клавиши)
## Что использовал?
Помимо основного алгоритма была обучена нейронная сеть на основе архитектуры YOLOv8m, пройдено 60 эпох, обучена
на датасете из >5000 размеченных кадров различных видеорядов.
## Результаты:
разработан алгоритм, способный отслеживать нажатие каждой клавиши на пианино и заполнять время нажатия
и отпускания в результирующий набор данных. (Результаты представлены в папке results).

![clavishi_2](https://github.com/user-attachments/assets/e917e22b-87ce-4866-847d-d5e460261ecd)
![clavishi](https://github.com/user-attachments/assets/841216d5-ab1d-4a4d-8913-af21931b0a5f)
![dataa_of_puts_2](https://github.com/user-attachments/assets/61b1a03b-997a-424d-b8a1-be784896531b)
![dataa_of_puts_1](https://github.com/user-attachments/assets/124b2af0-1cda-4e59-a56b-9e972bddc5c0)
