from numpy import *


def range_function(centers, final_cords, boxes):
    """
    ranges - словарь диапазонов клавиш, формат: {key(номер клавиши) : [левая граница, правая граница]}
    notes - список нот в кадре, формат: {[[x1,y1, x2,y2]...]}

    Работает на основе наблюдения, что границы клавиш всегда лежат внутри границ падающих нот
    работает примерно, со скростью nlog(n)

    Возвращает словарь формата: {key(номер клавиши):[[x1,y1, x2,y2]...]] - списки параметров нот соотвествующие клавише}
    """

    filter_flag = True

    while filter_flag == True:
        result = {}
        b = 0

        for box in boxes:
            n = 1
            s = 0
            for center in centers:
                if (box[0] < center) and (box[2] > center):

                    if final_cords[n][2] == 1:
                        result.update([(b, n)])
                        filter_flag = False
                        break
                    else:
                        result.update([(b, n)])
                        filter_flag = False
                        s += 1

                else:

                    if (s > 0) and (s < 2):
                        s += 1
                        filter_flag = False

                    elif s == 2:
                        filter_flag = False
                        break
                    else:
                        filter_flag = True

                n += 1

            if filter_flag == True:
                boxes = delete(boxes, [b], 0)
                break

            b += 1

        if filter_flag == False:
            return result, boxes

