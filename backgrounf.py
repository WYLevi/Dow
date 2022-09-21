# -*- coding: utf-8 -*-
import cv2
from time import *

# TODO �I����t��k���X
ALGORITHMS_TO_EVALUATE = [
    (cv2.bgsegm.createBackgroundSubtractorGMG(20, 0.7), 'GMG'),
    (cv2.bgsegm.createBackgroundSubtractorCNT(), 'CNT'),
    (cv2.createBackgroundSubtractorKNN(), 'KNN'),
    (cv2.bgsegm.createBackgroundSubtractorMOG(), 'MOG'),
    (cv2.createBackgroundSubtractorMOG2(), 'MOG2'),
    (cv2.bgsegm.createBackgroundSubtractorGSOC(), 'GSOC'),
    (cv2.bgsegm.createBackgroundSubtractorLSBP(), 'LSBP'),
]


# TODO �D���
def main():
    # �I�������ѧO���Ǹ�
    algo_index = 0
    subtractor = ALGORITHMS_TO_EVALUATE[algo_index][0]
    videoPath = "./video/vtest.avi"
    show_fgmask = False

    # ��o��������CPU���֤߼�
    nthreads = cv2.getNumberOfCPUs()
    # �]�w�������
    cv2.setNumThreads(nthreads)

    # Ū�����T
    capture = cv2.VideoCapture(videoPath)

    # ��e�V��
    frame_num = 0
    # �`����ɶ�
    sum_Time = 0.0

    while True:
        ret, frame = capture.read()
        if not ret:
            return
        begin_time = time()
        fgmask = subtractor.apply(frame)
        end_time = time()
        run_time = end_time - begin_time
        sum_Time = sum_Time + run_time
        # ��������ɶ�
        average_Time = sum_Time / (frame_num + 1)

        if show_fgmask:
            segm = fgmask
        else:
            segm = (frame * 0.5).astype('uint8')
            cv2.add(frame, (100, 100, 0, 0), segm, fgmask)

        # ��ܷ�e��k
        cv2.putText(segm, ALGORITHMS_TO_EVALUATE[algo_index][1], (10, 30), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 255),
                    2,
                    cv2.LINE_AA)
        # ��ܷ�e�������
        cv2.putText(segm, str(nthreads) + " threads", (10, 60), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 255), 2,
                    cv2.LINE_AA)
        # ��ܷ�e�C�V����ɶ�
        cv2.putText(segm, "averageTime {} s".format(average_Time), (10, 90), cv2.FONT_HERSHEY_PLAIN, 2.0,
                    (255, 0, 255), 2, cv2.LINE_AA);

        cv2.imshow('some', segm)
        key = cv2.waitKey(1) & 0xFF
        frame_num = frame_num + 1

        # ��'q'���h�X�^��
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()