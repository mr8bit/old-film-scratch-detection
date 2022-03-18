import glob
import os
import random

import numpy as np
import skvideo.datasets
import skvideo.io
from PIL import Image, ImageFilter
from tqdm import tqdm


class DefectGenerator(object):
    def __init__(self, image_folder, mask_output_path, image_output_path):
        self.video = None
        self.mask_output_path = mask_output_path
        self.image_output_path = image_output_path
        self.image_folder = image_folder
        self.image_datasets = glob.glob(os.path.join(image_folder, '*'))
        self.video_length = 0

    def load_video(self, path:str):
        self.video = skvideo.io.vread(path)
        self.video_length = len(self.video)

    def select_alpha(self, mask: np.array, color=0, return_numpy=False):
        """
            Конвертируем изображение в битовую маску
        :param mask:
        :return:
        """
        mask = np.invert(mask)
        bit_mask = mask
        bit_mask[bit_mask >= 190] = 255
        bit_mask[bit_mask < 190] = 0
        defect = Image.fromarray(mask)
        r = defect.split()
        alpha_r = r[0].point(lambda p: 255 - p)
        defect.putalpha(alpha_r)
        defect = defect.convert("RGBA")
        if return_numpy:
            return np.invert(defect), np.invert(bit_mask)
        return defect, Image.fromarray(np.invert(bit_mask))

    def create_masked(self, image: np.array, original_image: Image, color: int, blur=False) -> (Image, Image):
        mask = Image.fromarray(image).convert("L")
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
            mask = Image.fromarray(frame).convert("L")
            mask = mask.resize(resize, Image.ANTIALIAS)
            defect, bit_mask = self.select_alpha(mask, 0, return_numpy=True)  # дефект, битовая маска
            masks.append(defect)
        np_merged_mask = masks[0]
        for new_mask in masks[1:]:
            np_merged_mask += new_mask
        return np_merged_mask

    def run(self):
        self.video_length = len(self.video)

        index_image = 0
        for image_path in tqdm(self.image_datasets):
            index = random.randint(0, self.video_length)
            original_image = Image.open(image_path).convert("RGBA")
            frame = self.video[index]
            color = random.choices([100, 50, 0], k=1)
            defect, bit_mask = self.create_masked(frame, original_image, color[0])
            defect.save(f"{self.image_output_path}/defect_{index_image}.png")
            bit_mask.save(f"{self.mask_output_path}/mask_{index_image}.png")
            index_image += 1

        print("Create dirty images...")

        for image_path in tqdm(self.image_datasets):
            original_image = Image.open(image_path).convert("RGBA")
            frame = self.generate_dirty_image(5, original_image.size)
            color = random.choices([100, 50, 0], k=1)
            defect, bit_mask = self.create_masked(frame, original_image, color[0])
            defect.save(f"{self.image_output_path}/defect_dirty_{index_image}.png")
            bit_mask.save(f"{self.mask_output_path}/mask_dirty_{index_image}.png")
            index_image += 1
