from defect_generator import DefectGenerator

if __name__ == '__main__':
    generator = DefectGenerator('./images', './mask', './defect', ['./video/Damaged Old Film OVERLAY - 4K FREE high quality effects.mp4'])
    generator.run()
