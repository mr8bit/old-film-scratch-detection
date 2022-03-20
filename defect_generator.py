import glob
import os
import random

import numpy as np
import skvideo.datasets
import skvideo.io
from PIL import Image, ImageFilter


class DefectGenerator(object):
    def __init__(self, image_folder, mask_output_path, image_output_path, videos_with_defect: list):
        self.video = None
        self.mask_output_path = mask_output_path
        self.image_output_path = image_output_path
        self.image_folder = image_folder
        self.image_datasets = glob.glob(os.path.join(image_folder, '*'))
        self.video_length = 0
        self.videos_with_defect = videos_with_defect

    def load_video(self, path: str):
        self.video = skvideo.io.vreader(path)

    def select_alpha(self, mask: Image, color=0, return_numpy=False):
        """
            Конвертируем изображение в битовую маску
        :param mask:
        :return:
        """
        # mask = np.invert(mask)
        data = np.invert(mask)
        rgb = data[:, :, :3]
        color = [235, 235, 235]  # Original value value
        black = [0, 0, 0, 255]
        mask = np.all(rgb <= color, axis=-1)
        data[mask] = black
        defect = data
        #
        # bit_mask = mask
        # bit_mask[bit_mask >= 190] = 255
        # bit_mask[bit_mask < 190] = 0
        # defect = Image.fromarray(mask)
        # r = defect.split()
        # alpha_r = r[0].point(lambda p: 255 - p)
        # defect.putalpha(alpha_r)
        # defect = defect.convert("RGBA")
        if return_numpy:
            return np.invert(defect), np.invert(defect)
        return Image.fromarray(defect), Image.fromarray(np.invert(defect)).convert("L")

    def create_masked(self, image: np.array, original_image: Image, color: int, blur=False) -> (Image, Image):
        mask = Image.fromarray(image).convert("RGBA")
        mask = mask.resize(original_image.size, Image.ANTIALIAS)
        defect, bit_mask = self.select_alpha(mask, color)  # дефект, битовая маска
        if blur:
            defect = defect.filter(ImageFilter.BoxBlur(1))
        defected = Image.alpha_composite(original_image, defect)
        return defected, bit_mask

    def generate_dirty_image(self, defect_count, resize):
        masks = []
        for i in range(defect_count):
            index = random.randint(0, self.video_length)
            frame = self.video[index]
            mask = Image.fromarray(frame).convert("RGBA")
            mask = mask.resize(resize, Image.ANTIALIAS)
            defect, bit_mask = self.select_alpha(mask, 0, return_numpy=True)  # дефект, битовая маска
            masks.append(defect)
        np_merged_mask = masks[0]
        for new_mask in masks[1:]:
            np_merged_mask += new_mask
        return np_merged_mask

    def run(self):
        index_image = 0
        while (index_image < len(self.image_datasets)):
            for video_path in self.videos_with_defect:
                print(f"Load Defects: {video_path}")
                self.load_video(video_path)
                for image_frame in self.video:
                    original_image = Image.open(self.image_datasets[index_image]).convert("RGBA")
                    frame = np.array(image_frame)
                    color = random.choices([100, 50, 0], k=1)
                    defect, bit_mask = self.create_masked(frame, original_image, color[0])
                    defect.save(f"{self.image_output_path}/defect_{index_image}.png")
                    bit_mask.save(f"{self.mask_output_path}/mask_{index_image}.png")
                    index_image += 1
            print("All video defects are ending..")
            break
        # print("Create dirty images...")
        # for image_path in tqdm(self.image_datasets):
        #     original_image = Image.open(image_path).convert("RGBA")
        #     frame = self.generate_dirty_image(5, original_image.size)
        #     color = random.choices([100, 50, 0], k=1)
        #     defect, bit_mask = self.create_masked(frame, original_image, color[0])
        #     defect.save(f"{self.image_output_path}/defect_dirty_{index_image}.png")
        #     bit_mask.save(f"{self.mask_output_path}/mask_dirty_{index_image}.png")
        #     index_image += 1
