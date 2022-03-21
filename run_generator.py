import argparse
import glob
import os

from defect_generator import DefectGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Создание набора данных')
    parser.add_argument('--original_folder', type=str, help='Папка где лежат оригинальные изображения')
    parser.add_argument('--masks_folder', type=str, help='Папка куда сохранять маски')
    parser.add_argument('--defects_folder', type=str,
                        help='Папка куда сохранять изображения original_folder video_defects с дефектам')
    parser.add_argument('--video_defects_folder', type=str, help='Папка где лежат видео с дефектами')
    args = parser.parse_args()

    video_defects = glob.glob(os.path.join(args.video_defects_folder, '*'))
    print("#" * 30)
    print(f"Папка где лежат оригинальные изображения: {args.original_folder}")
    print(f"Папка куда сохранять маски: {args.masks_folder}")
    print(f"Папка куда сохранять дефекты: {args.defects_folder}")
    print(f"Папка где лежат видео с дефекты: {args.video_defects_folder}")
    print(f"Количество видео в дефектами: {len(video_defects)}")
    print("#" * 30)

    generator = DefectGenerator(args.original_folder, args.masks_folder, args.defects_folder, video_defects)
    generator.run()
