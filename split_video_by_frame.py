import argparse

import cv2
import skvideo.io
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Разделение видео на файлы')
    parser.add_argument('--video', type=str, help='Видео для разделения на кадры')
    parser.add_argument('--frame', type=int, help='Какой кадр сохранять')
    args = parser.parse_args()

    print("#" * 30)
    print("Видео:", args.video)
    print(f"Сохраняем каждый {args.frame} кадр")
    print("#" * 30)

    videogen = skvideo.io.vreader(args.video)
    index = 0
    for frame in tqdm(videogen):
        if index % args.frame == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f'./data/images/frame_{index}.jpg', frame)
        index += 1
