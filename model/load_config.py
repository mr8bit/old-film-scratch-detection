from mmcv import Config


config = Config.fromfile('../mmsegmentation/configs/swin/upernet_swin_base_patch4_window12_512x512_160k_ade20k_pretrain_384x384_1K.py')

config.dump('./swim.py')
