""" --------------------------- ТУТ БУДУТ ПОЛЕЗНЫЕ КУСКИ КОДА------------------------------ """

# import json
# from json import JSONEncoder
# from ultralytics import YOLO
# import cv2 as cv
# import numpy as np
# import torch
#
#
# class NumpyArrayEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return JSONEncoder.default(self, obj)
#
#
# model = YOLO("best_60epochs.pt")
#
# cap = cv.VideoCapture("vid_test.mp4")
#
# while True:
#     _, img = cap.read()
#     gray = cv.cvtColor(img[50:250, :], cv.COLOR_RGB2GRAY)
#     blur = cv.GaussianBlur(gray, (3, 3), 100)
#     blur = np.expand_dims(blur, axis=-1)
#     blur_temp = blur.copy()
#     blur = np.append(blur, blur, axis=-1)
#     blur = np.append(blur_temp, blur, axis=-1)
#     print(blur.shape)
#
#     results = model.predict(blur, save=False)
#     for result in results:
#         boxes = result.boxes
#
#         data_boxes = json.dumps({"array": boxes.xyxy.numpy()}, cls=NumpyArrayEncoder)
#
#         print(boxes.xyxy.numpy())
#         for box in range(0, len(boxes.xyxy.numpy())):
#             cv.rectangle(blur, (int(boxes.xyxy.numpy()[box][0]), int(boxes.xyxy.numpy()[box][1])),
#                          (int(boxes.xyxy.numpy()[box][2]), int(boxes.xyxy.numpy()[box][3])), (0, 255, 0), 2)
#     cv.imshow('res', blur)
#
#     if cv.waitKey(50) & 0xFF == ord('q'):
#         break
#
#     with open('data_boxes.json', 'w') as file:
#         json.dump(data_boxes, file)

# import cv2
# import numpy as np
#
#
# def kmeans_color(image, label):
#     # Загрузка цветного изображения
#
#     # Преобразование изображения в одномерный массив
#     data = image.reshape((-1, 3))
#
#     # Преобразование в тип данных с плавающей запятой
#     data = np.float32(data)
#
#     # Определение критериев останова для алгоритма к-средних
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#
#     # Применение алгоритма к-средних для четырех регионов
#     _, labels4, centers4 = cv2.kmeans(data, 7, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
#
#     # Конвертация центров кластеров обратно в тип данных с плавающей запятой
#     centers4 = np.uint8(centers4)
#
#     # Преобразование меток обратно в изображение
#
#     segmented_image4 = centers4[labels4.flatten()]
#     segmented_image4 = segmented_image4.reshape(image.shape)
#
#     # cv2.imwrite(f"dataset/image{label}.png", segmented_image4)
#     return segmented_image4
#
#
# cap = cv2.VideoCapture("videos/v10.mp4")
# label = 2632
#
# while True:
#
#     _, img = cap.read()
#     gray = cv2.cvtColor(img[32:, :], cv2.COLOR_RGB2GRAY)
#     blur = cv2.GaussianBlur(gray, (3, 3), 100)
#
#     print(kmeans_color(blur, label).shape)
#     cv2.imshow('res', kmeans_color(blur, label))
#     label += 1
#
#     if cv2.waitKey(50) & 0xFF == ord('q'):
#         break


# print(piano.final_cords)
# cap = cv2.VideoCapture("vid_test.mp4")
#
# while True:
#
#     _, img = cap.read()
#     gray = cv2.cvtColor(img[:][:600], cv2.COLOR_RGB2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 100)
#
#     alpha = 1.5  # Contrast control (1.0-3.0)
#     beta = 0  # Brightness control (0-100)
#
#     contrast = cv2.convertScaleAbs(blur, alpha=alpha, beta=beta)
#
#     canny = cv2.Canny(contrast, 230, 255)
#     kernel = np.ones((7, 7), np.uint8)
#     erode = cv2.erode(canny, kernel, iterations=1)

# for i in range(0, len(piano.centers)):
#     area_1 = canny[100][piano.centers[i]] > 0 or canny[99][piano.centers[i]] >0 or canny[98][piano.centers[i]] > 0
#     area_2 = canny[97][piano.centers[i]] > 0 or canny[96][piano.centers[i]] > 0 or canny[95][piano.centers[i]] > 0
#     area_3 = canny[94][piano.centers[i]] > 0 or canny[93][piano.centers[i]] > 0 or canny[92][piano.centers[i]] > 0
#     if area_1 or area_2 or area_3:
#         cv2.circle(img, (piano.centers[i], 100), 20, (255, 0, 0), -1)
#
# for i in range(0, len(piano.centers)):
#     cv2.circle(img, (piano.centers[i], 100), 1, (255, 0, 0), -1)

# # Рисуем центры всех клавиш
# for i in range(0, len(piano.centers)):
#     for p in range(0, 1000):
#         cv2.circle(img, (piano.centers[i], img.shape[0]-90-p), 1, (255, 255, 255), -1)
#
# cv2.imshow('res', img)

# if cv2.waitKey(50) & 0xFF == ord('q'):
#     break

# # Рисуем прорези для белых клавиш
# i = 1
# j = 0
# while i <= len(piano.cords_white_buttons):
#     while j < 2:
#         for k in range(int(image.shape[0]/1.5), image.shape[0]):
#             cv2.circle(image, (piano.cords_white_buttons[i][1], k), 1, (255, 0, 0), -1)
#
#         j += 1
#     i += 1
#     j = 0
#
# # Рисуем чёрные клавиши
# i = 1
# while i <= len(piano.black_cords):
#     while j < 2:
#         for k in range(piano.low_high_cords[i][1], piano.low_high_cords[i][0]):
#             cv2.circle(image, (piano.black_cords[i][0], k), 0, (0, 0, 255), -1)
#             cv2.circle(image, (piano.black_cords[i][1], k), 0, (0, 0, 255), -1)
#
#         j += 1
#     i += 1
#     j = 0
#
# a = 1
# while a <= len(piano.black_cords):
#     i = piano.black_cords[a][0]
#     while i <= piano.black_cords[a][1]:
#         cv2.circle(image, (i, piano.low_high_cords[a][0]), 0, (0, 0, 255), -1)
#         cv2.circle(image, (i, piano.low_high_cords[a][1]), 0, (0, 0, 255), -1)
#         i += 1
#     a += 1
#
# # Рисуем центры всех клавиш
# for i in range(0, len(piano.centers)):
#     for p in range(0, 1000):
#         cv2.circle(image, (piano.centers[i], image.shape[0]-90-p), 1, (0, 255, 0), -1)

# # Рисуем финальные координаты
# for i in range(1, len(piano.final_cords)+1):
#     cv2.line(image, [piano.final_cords[i][0], image.shape[0]-10-i],
#              [piano.final_cords[i][1], image.shape[0]-10-i], (0, 0, 200))

# print(len(piano.canny[0]))
# print(piano.cords)
# print(piano.cords_white_buttons)
# print(piano.black_cords)
# print(piano.low_high_cords)
# print(piano.final_cords)
# print(piano.cords)
# print(piano.cords_white_buttons)
# cv2.imshow('res', image)
# cv2.waitKey(0)

# cap = cv2.VideoCapture("vid_1.mp4")
#
# while True:
#     _, img = cap.read()
#     for i in range(0, len(piano.centers)):
#         for p in range(0, 1000):
#             cv2.circle(img, (piano.centers[i], img.shape[0] - 323 - p), 1, (0, 255, 0), -1)
#
#     cv2.imshow('res', img)
#
#     if cv2.waitKey(50) & 0xFF == ord('q'):
#         break