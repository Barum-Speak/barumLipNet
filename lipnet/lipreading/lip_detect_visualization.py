import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import cv2 as cv
import dlib
import numpy as np

def show_video_subtitle(frames, subtitle):

    # 얼굴 검출을 위해 디폴트 얼굴 검출기 사용
    detector = dlib.get_frontal_face_detector()
    # 검출된 얼굴에서 눈, 코, 입같은 랜드마크를 찾기 위해 사용할 학습모델을 로드합니다.
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    MOUTH = list(range(48, 68))
    index = MOUTH

    fig, ax = plt.subplots()
    fig.show()

    text = plt.text(0.5, 0.1, "",
        ha='center', va='center', transform=ax.transAxes,
        fontdict={'fontsize': 15, 'color':'white', 'fontweight': 500})
    text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),
        path_effects.Normal()])

    subs = subtitle.split()
    inc = max(len(frames)/(len(subs)+1), 0.01)

    i = 0
    img = None
    for frame in frames:
        # 웹캠으로부터 이미지를 가져와서 그레이스케일로 변환한다.
        img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # 주어진 이미지에서 얼굴을 검출. 두번째 아규먼트는 업샘플링 횟수.
        dets = detector(img_gray, 1)

        for face in dets:

            # 주어진 이미지 img_frame의 검출된 얼굴 영역 face에서 랜드마크를 검출.
            shape = predictor(frame, face)  # 얼굴에서 68개 점 찾기

            list_points = []
            for p in shape.parts():
                list_points.append([p.x, p.y])

            list_points = np.array(list_points)

            # 검출된 랜드마크 중 index 변수에 지정된 부위만 이미지에 원으로 그려줌.
            for i, pt in enumerate(list_points[index]):
                pt_pos = (pt[0], pt[1])

                cv.circle(frame, pt_pos, 2, (0, 255, 0), -1)

        # 결과 이미지를 화면에 보여주고 키보드 입력을 받음
        cv.imshow('result', frame)

        sub = " ".join(subs[:int(i/inc)])

        text.set_text(sub)

        if img is None:
            img = plt.imshow(frame)
        else:
            img.set_data(frame)
        fig.canvas.draw()
        i += 1


