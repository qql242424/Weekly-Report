import cv2
import mediapipe as mp
import numpy as np
import math
import pyautogui
#import applescript
'''
手部姿势检测：首先利用 MediaPipe 的 Hand 模型对摄像头捕获的图像进行手部姿势检测，得到手部关键点的位置信息。
手势识别：通过分析手部关键点的位置，可以根据拇指和食指的相对位置、手部的张开程度等因素来判断用户的手势。
音量控制：根据识别出的手势动作，映射到对应的音量控制操作。
调整系统音量：最后，根据映射得到的音量控制操作，通过相应的系统接口来实现对音量的调整。
操作系统中，可以通过系统 API 或库来控制系统音量的增减和静音操作。
'''
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# 初始化音量大小

volume = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)#读取图像并进行颜色转换：在每次循环迭代中，你使用 cap.read()从摄 像头中读取一帧图像，
    # 并将其颜色空间从 BGR 转换为 RGB。这是因为 Hands 对 象需要 RGB 图像作为输入
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 绘制手部关键点和线条
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2))

            # 计算食指和拇指指尖的位置
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # 控制音量
            distance = math.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
            print(distance)
            max_distance = 0.3  # 定义最大距离
            volume = distance / max_distance  # 根据距离计算音量大小
            print(volume)
            volume = min(1, max(0, volume))  # 将音量限制在 [0, 1] 范围内
            pyautogui.press('volumedown') if volume < 0.5 else pyautogui.press('volumeup')


    cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()


import cv2
import mediapipe as mp
import numpy as np
import math
import pyautogui
#import applescript
'''
手部姿势检测：首先利用 MediaPipe 的 Hand 模型对摄像头捕获的图像进行手部姿势检测，得到手部关键点的位置信息。
手势识别：通过分析手部关键点的位置，可以根据拇指和食指的相对位置、手部的张开程度等因素来判断用户的手势。
音量控制：根据识别出的手势动作，映射到对应的音量控制操作。
调整系统音量：最后，根据映射得到的音量控制操作，通过相应的系统接口来实现对音量的调整。
操作系统中，可以通过系统 API 或库来控制系统音量的增减和静音操作。
'''
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# 初始化音量大小

volume = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)#读取图像并进行颜色转换：在每次循环迭代中，你使用 cap.read()从摄 像头中读取一帧图像，
    # 并将其颜色空间从 BGR 转换为 RGB。这是因为 Hands 对 象需要 RGB 图像作为输入
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 绘制手部关键点和线条
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2))

            # 计算食指和拇指指尖的位置
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # 控制音量
            distance = math.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
            print(distance)
            max_distance = 0.3  # 定义最大距离
            volume = distance / max_distance  # 根据距离计算音量大小
            print(volume)
            volume = min(1, max(0, volume))  # 将音量限制在 [0, 1] 范围内
            pyautogui.press('volumedown') if volume < 0.5 else pyautogui.press('volumeup')


    cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()