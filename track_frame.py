from range_function import range_function

from ultralytics import YOLO
import cv2
import numpy as np
import torch


def track_frame(cap, centers, final_cords):

    # Запись видео
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_size = (frame_width, frame_height)
    fps = 20
    # output = cv2.VideoWriter(
    #     "output.mp4", cv2.VideoWriter_fourcc('a', 'v', 'c', '1'), fps, frame_size)

    # Подгрузка модели
    model = YOLO("models/best_60epochs.pt")

    data = {}
    for i in range(1, len(centers)+1):
        data.update([(i, [])])

    n_frame = 1    # номер кадра
    # Обработка каждого кадра
    try:
        while True:
            _, img = cap.read()
            gray = cv2.cvtColor(img[50:250, :], cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 100)
            blur = np.expand_dims(blur, axis=-1)
            blur_temp = blur.copy()
            blur = np.append(blur, blur, axis=-1)
            blur = np.append(blur_temp, blur, axis=-1)

            # Храним корд-ты рамок в nd.array
            results = model.predict(blur, save=False)

            none_flag = False

            for result in results:
                if len(result.boxes.cls.numpy()) == 0:
                    none_flag = True
                    break

                boxes = result.boxes
                boxes = boxes.xyxy.numpy()
                boxes = boxes[np.argsort(boxes[:, 0])][::-1]

            if none_flag == True:
                n_frame += 1
                continue

            # boxes = []
            # for q in range(0, len(box_cords)):
            #     boxes.append([box_cords[q][0] + (box_cords[q][2] - box_cords[q][0]) * 0.15, box_cords[q][1],
            #                   box_cords[q][2] - (box_cords[q][2] - box_cords[q][0]) * 0.15, box_cords[q][3]])

            # Создаём временный словарь temp_data
            temp_data, boxes = range_function(centers, final_cords, boxes)
            print(boxes)
            print(temp_data)

            # # Рисуем центры всех клавиш
            # for i in range(0, len(centers)):
            #     for p in range(0, 1000):
            #         cv2.circle(img, (centers[i], img.shape[0]-p), 1, (255, 255, 255), -1)

            for s in range(0, len(temp_data)):
                for p in range(0, 1000):
                    cv2.circle(img, (centers[temp_data[s]-1], img.shape[0]-p), 1, (0, 0, 255), -1)

            for i in range(0, img.shape[1]):
                cv2.circle(img, (i, img.shape[0] - (img.shape[0] - 250)), 1, (0, 255, 0), -1)
                cv2.circle(img, (i, img.shape[0] - (img.shape[0] - 50)), 1, (0, 255, 0), -1)

            # Рисуем боксы
            for box in boxes:
                cv2.rectangle(img, (int(box[0]), int(box[1])+50), (int(box[2]), int(box[3])+50), (0, 0, 255), 2)

            cv2.imshow('res', img)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

            if len(temp_data) > 0:

                # output.write(img)    # Запись видео

                for i in range(0, len(boxes)):
                    if boxes[i][3] > 100.0 and boxes[i][1] > 100.0:    # 1
                        if len(data[temp_data[i]]) == 0:
                            data[temp_data[i]].append([boxes[i][3]])
                            data[temp_data[i]][-1].append(n_frame)
                            data[temp_data[i]][-1].append(n_frame)

                        else:
                            if len(data[temp_data[i]][-1]) == 2:
                                data[temp_data[i]][-1].append(n_frame)

                            elif boxes[i][3] < data[temp_data[i]][-1][0]:
                                data[temp_data[i]].append([boxes[i][3]])
                                data[temp_data[i]][-1].append(n_frame)
                                data[temp_data[i]][-1].append(n_frame)

                    elif (boxes[i][3] >= 100.0) and (boxes[i][1] < 100.0):    # 2
                        if len(data[temp_data[i]]) == 0:
                            data[temp_data[i]].append([boxes[i][3]])
                            data[temp_data[i]][-1].append(n_frame)

                        elif len(data[temp_data[i]][-1]) == 3:
                            data[temp_data[i]].append([boxes[i][3]])
                            data[temp_data[i]][-1].append(n_frame)

                    elif (boxes[i][3] < 100.0) and (boxes[i][1] < 100.0):    # 3
                        pass

            n_frame += 1

    except TypeError:

        for i in range(1, len(data)+1):
            if not len(data[i]) == 0:
                for note in data[i]:
                    _t = note.pop(0)

        return data

