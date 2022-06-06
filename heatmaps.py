#Script to get heatmaps of a specific video using saved predictions

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from PIL import Image
from skimage import img_as_ubyte
import io
import os

predicciones_root = 'generar_videos/predicciones_guardadas/'
heatmaps_root = 'generar_videos/heatmaps/'

video_list = ['1An41lDIJ6Q25', '6QUCaLvQ_3I60', '8ESEI0bqrJ425', '8feS1rNYEbg30', 'ByBF08H_wDA30', 'dd39herpgXA25', 'ey9J7w98wlI50', 'fryDy9YcbI430', 'idLVnagjl_s30', 'kZB3KMhqqyI30', 'MzcdEI_tSUc25', 'RbgxpagCY_c30']
format_list = ['BCE', 'CC', 'KL', 'NSS', 'Original']

def generate_heatmap(image_path, output_path):
    #print(f'Leyendo {image_path} y guardando en {output_path}')
    image = cv2.imread(image_path, 0) # Read image
    colormap = plt.get_cmap('viridis')
    heatmap = (colormap(image) * 2**16).astype(np.uint16)[:,:,:3]
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR) # Changes color space
    #cv2.imshow('heatmap', heatmap)

    heatmap_ubyte = img_as_ubyte(heatmap)
    cv2.imwrite(output_path, heatmap_ubyte)
    #cv2.imshow('heatmap', heatmap_ubyte)

for form in format_list: # For each format
    print(f'FORMAT: {form}')
    for video in video_list: # For each video
        print(f'   Video: {video}')
        path = os.path.join(f'{predicciones_root}/{form}', video)
        video_names = [vid for vid in os.listdir(path)
                                if vid.endswith(('.jpg', '.jpeg', '.png'))]

        total = len(video_names)
        for idx, v in enumerate(video_names):
            #print(f'Leyendo de {predicciones_root}{video}/{v}, guardando en {heatmaps_root}{video}/{v}')
            generate_heatmap(f'{predicciones_root}/{form}/{video}/{v}', f'{heatmaps_root}/{form}/{video}/{v}')
            if idx % 100 == 0:
                print(f'      {idx} / {total}')