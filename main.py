import numpy as np
import cv2
import marking_buttons as mb
from track_frame import track_frame

if __name__ == "__main__":

    cap = cv2.VideoCapture("videos/v1.mp4")
    image = cv2.imread("images/3_sept.png")
    print(image.shape)
    piano = mb.Piano(image)
    piano.complete()

    data_frame = track_frame(cap, piano.centers, piano.final_cords)
    print(f'DATA: {data_frame}')

    # Рисуем центры всех клавиш
    for i in range(0, len(piano.centers)):
        for p in range(0, 1000):
            cv2.circle(image, (piano.centers[i], image.shape[0]-90-p), 1, (255, 255, 255), -1)

    cv2.imshow('res', image)
    cv2.waitKey(0)

