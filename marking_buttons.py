import numpy as np
import cv2


"""-------------------------------Пишем свой класс--------------------------------"""
class Piano:
    def __init__(self, image):  # Инициализация атрибутов
        self.canny = None
        self.cords = []
        self.cords_white_buttons = {}
        self.black_cords = {}
        self.low_high_cords = {}
        self.centers = []
        self.final_cords = {}
        self.image = image
        self.level = 40  # 323
        self.alpha = 10
        self.beta = 2.5
        self.num = 1

    def prep(self):  # Подготовка изображения

        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        # gray = np.transpose(gray)
        print(gray.shape)
        # gray = cv2.GaussianBlur(gray, (3, 3), 10)
        self.alpha = 2.5  # Contrast control (1.0-3.0)
        self.beta = 10  # Brightness control (0-100)

        _contrast = cv2.convertScaleAbs(gray, alpha=self.alpha, beta=self.beta)
        self.canny = cv2.Canny(_contrast, 0, _contrast.max() - 150)

        _kernel = np.ones((5, 5), np.uint8)
        _dil = cv2.dilate(self.canny, _kernel, iterations=1)
        self.canny = _dil

    def holes(self):  # Заполнение дыр

        _Y, _X = self.canny.shape
        _nearest_neigbours = [[
            np.argmax(
                np.bincount(self.canny[max(_i - self.num, 0):min(_i + self.num, _Y),
                            max(_j - self.num, 0):min(_j + self.num, _X)].ravel()))
            for _j in range(_X)] for _i in range(_Y)]
        self.canny = np.array(_nearest_neigbours, dtype=np.uint8)

    def first_level(self):

        _j = 0
        while _j < self.image.shape[1]:
            if self.canny[self.image.shape[0] - self.level][_j] > 0:
                _j_val = _j
                while self.canny[self.image.shape[0] - self.level][_j] > 0 and _j < self.image.shape[1]:
                    _j += 1
                _j_val = _j_val + int((_j - _j_val) / 2)
                self.cords.append(_j_val - 1)
            _j += 1

    def second_level(self):

        _l1 = self.cords[1] - self.cords[0]
        _l2 = self.cords[2] - self.cords[1]

        _area_1 = ((self.cords[0] / (self.cords[1] - self.cords[0]) > 1.2)
                   and (self.cords[0] / (self.cords[1] - self.cords[0]) < 2.2))
        _area_2 = ((self.cords[0] / (self.cords[1] - self.cords[0]) >= 2.2)
                   and (self.cords[0] / (self.cords[1] - self.cords[0]) < 3.1))

        if _area_1:
            self.cords.append(self.cords[0] - int(self.cords[1] - self.cords[0]))
            self.cords.sort()
        if _area_2:
            self.cords.append(self.cords[0] - int(self.cords[1] - self.cords[0]))
            self.cords.sort()
            self.cords.append(self.cords[0] - int(self.cords[1] - self.cords[0]))
            self.cords.sort()

        _l_etal = _l1
        for _i in range(1, len(self.cords)):
            if (((self.cords[_i] - self.cords[_i - 1]) / _l_etal > 1.5)
                    and ((self.cords[_i] - self.cords[_i - 1]) / _l_etal < 2.7)):
                self.cords.append(self.cords[_i] - int((self.cords[_i] - self.cords[_i - 1]) / 2))
                self.cords.sort()
            elif (self.cords[_i] - self.cords[_i - 1]) / _l_etal >= 2.7:
                self.cords.append(self.cords[_i] - int((self.cords[_i] - self.cords[_i - 1]) / 2))
                self.cords.sort()
                self.cords.append(self.cords[_i] - int((self.cords[_i] - self.cords[_i - 1]) / 2))
                self.cords.sort()

        _score = 2
        self.cords_white_buttons.update([(1, [0, self.cords[0]])])
        for _i in range(1, len(self.cords)):
            self.cords_white_buttons.update([(_score, [self.cords[_i - 1], self.cords[_i]])])
            _score += 1

        self.cords_white_buttons.update([(_score, [self.cords[-1], self.cords[-1] + (self.cords[-1]-self.cords[-2])])])
        self.cords.append(self.cords[-1] + (self.cords[-1]-self.cords[-2]))

    def black_marking(self):

        _score = 0

        for _i in range(1, len(self.cords_white_buttons)):
            if _i in [2, 5, 9, 12, 16, 19, 23, 26, 30, 33, 37, 40, 44, 47, 51]:
                pass

            elif _i in [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50]:
                _score += 1

                if _i == 1:
                    _l_black = self.cords_white_buttons[_i][1] - int(
                        (self.cords_white_buttons[_i + 1][1] - self.cords_white_buttons[_i + 1][0]) * 3 / 15)
                    _r_black = self.cords_white_buttons[_i][1] + int(
                        (self.cords_white_buttons[_i + 1][1] - self.cords_white_buttons[_i + 1][0]) * 6 / 15)
                    self.black_cords.update([(_score, [_l_black, _r_black])])

                else:
                    _l_black = self.cords_white_buttons[_i][1] - int(
                        (self.cords_white_buttons[_i][1] - self.cords_white_buttons[_i][0]) * 3 / 15)
                    _r_black = self.cords_white_buttons[_i][1] + int(
                        (self.cords_white_buttons[_i + 1][1] - self.cords_white_buttons[_i + 1][0]) * 6 / 15)
                    self.black_cords.update([(_score, [_l_black, _r_black])])

            elif _i in [3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48]:
                _score += 1

                _l_black = self.cords_white_buttons[_i][1] - int(
                    (self.cords_white_buttons[_i][1] - self.cords_white_buttons[_i][0]) * 6 / 15)
                _r_black = self.cords_white_buttons[_i][1] + int(
                    (self.cords_white_buttons[_i + 1][1] - self.cords_white_buttons[_i + 1][0]) * 3 / 15)
                self.black_cords.update([(_score, [_l_black, _r_black])])

            elif _i in [7, 14, 21, 28, 35, 42, 49]:
                _score += 1

                _l_black = self.cords_white_buttons[_i][1] - int(
                    (self.cords_white_buttons[_i][1] - self.cords_white_buttons[_i][0]) * 9 / 30)
                _r_black = self.cords_white_buttons[_i][1] + int(
                    (self.cords_white_buttons[_i + 1][1] - self.cords_white_buttons[_i + 1][0]) * 9 / 30)
                self.black_cords.update([(_score, [_l_black, _r_black])])

    def marking_low_high(self):

        _low_black_button = 0
        _n_button = 1
        _j = 0

        # разметка нижней границы чёрных клавиш
        for _n in range(1, len(self.cords_white_buttons) + 1):
            if _n in [1, 4, 7, 11, 14, 18, 21, 25, 28, 32, 35, 39, 42, 46, 49, 52]:
                pass

            else:

                if _n in [2, 5, 8, 9, 12, 15, 16, 19, 22, 23, 26, 29, 30, 33, 36, 37, 40, 43, 44, 47, 50, 51]:
                    _j = (self.cords_white_buttons[_n][0]
                          + int((self.cords_white_buttons[_n][1] - self.cords_white_buttons[_n][0]) / 3))

                if _n in [3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48]:
                    _j = (self.cords_white_buttons[_n][0]
                          + int((self.cords_white_buttons[_n][1] - self.cords_white_buttons[_n][0]) / 1.5))

                _i = 0
                while self.canny[self.image.shape[0] - self.level + _i][_j] < 1:
                    _i = _i - 1
                    if _i < -self.image.shape[0]:
                        _i = _low_black_button
                        break
                _low_black_button = _i + self.image.shape[0] - self.level

                # разметка верхней границы чёрных клавиш
                _a1 = self.cords_white_buttons[2][1] - self.cords_white_buttons[2][0]
                _high_black_button = _low_black_button - _a1 * 4 - 10

                self.low_high_cords.update([(_n_button, [_low_black_button, _high_black_button])])
                _n_button += 1

    def center_marking(self):

        # Разметка клавиш по центральной координате
        self.centers.append(int(self.cords_white_buttons[1][0]
                                + (self.black_cords[1][0] - self.cords_white_buttons[1][0])*0.5))

        for _q in range(2, len(self.black_cords) + 1):

            _temp = self.black_cords[_q-1][1] - self.black_cords[_q-1][0]

            if (self.black_cords[_q][0]-self.black_cords[_q-1][1])/_temp > 1.3:

                self.centers.append(int(self.black_cords[_q-1][1]
                                        + (self.black_cords[_q][0]-self.black_cords[_q-1][1])*0.25))
                self.centers.append(int(self.black_cords[_q-1][1]
                                        + (self.black_cords[_q][0]-self.black_cords[_q-1][1])*0.75))
            else:

                self.centers.append(int(self.black_cords[_q-1][1]
                                        + (self.black_cords[_q][0]-self.black_cords[_q-1][1])*0.5))

        self.centers.append(int(self.black_cords[36][1]
                                + (self.cords_white_buttons[51][1] - self.black_cords[36][1])*0.5))
        self.centers.append(int(self.black_cords[36][1]
                                + (self.cords_white_buttons[51][1] - self.black_cords[36][1])*1.75))

        for _q in range(1, len(self.black_cords) + 1):

            self.centers.append(int(self.black_cords[_q][0]
                                    + (self.black_cords[_q][1] - self.black_cords[_q][0]) / 2))

        self.centers.sort()




    def final_marking(self):

        _data = []
        _s = 1
        _k = 1

        for _i in range(1, len(self.cords_white_buttons)):
            if _i == 1:    # Первая клавиша
                _data.append(0)
                _data.append(self.black_cords[1][0])
            elif _i in [2, 5, 9, 12, 16, 19, 23, 26, 30, 33, 37, 40, 44, 47, 51]:    # Правые белые
                _data.append(self.black_cords[_i-_s][1])
                _data.append(self.cords_white_buttons[_i][1])
                _s += 1
            elif _i in [3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48]:    # Левые белые
                _data.append(self.cords_white_buttons[_i][0])
                _data.append(self.black_cords[_i-_k][0])
                _k += 1

        # Последняя белая
        _data.append(self.cords_white_buttons[52][0])
        _data.append(self.cords_white_buttons[52][1])

        for _i in range(2, len(self.black_cords)+1):    # Центральные белые
            if not ((self.black_cords[_i][0]-self.black_cords[_i-1][1])
                    / (self.black_cords[_i][1]-self.black_cords[_i][0]) > 1.3):
                _data.append(self.black_cords[_i-1][1])
                _data.append(self.black_cords[_i][0])

        for _i in range(1, len(self.black_cords)+1):    # Все чёрные
            _data.append(self.black_cords[_i][0])
            _data.append(self.black_cords[_i][1])

        _data.sort()

        _b = 1
        for _i in range(0, len(_data), 2):
            if _b in [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46, 48, 50, 53,
                      55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]:
                self.final_cords.update([(_b, [_data[_i], _data[_i+1], 0])])
            else:
                self.final_cords.update([(_b, [_data[_i], _data[_i+1], 1])])

            _b += 1


    def complete(self):

        self.prep()
        self.holes()
        self.first_level()
        self.second_level()
        self.black_marking()
        self.marking_low_high()
        self.center_marking()
        self.final_marking()
