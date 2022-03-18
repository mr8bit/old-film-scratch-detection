from defect_generator import DefectGenerator

if __name__ == '__main__':
    generator = DefectGenerator('./images', './mask', './defect')
    generator.load_video(path='./video/EFECTO MT Super 8 Overlay.mp4')
    generator.run()
