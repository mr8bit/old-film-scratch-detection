import cv2
import skvideo.io

videogen = skvideo.io.vreader(
    "/home/mr9bit/Загрузки/Кавказская пленница, или Новые приключения Шурика (FullHD, комедия, реж. Леонид (1).mp4")
index = 0
for frame in videogen:
    if index % 120 == 0:
        print(frame.shape)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f'./images/frame_{index}.jpg', frame)
    index+=1
