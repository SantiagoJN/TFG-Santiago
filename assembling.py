#Script to reassemble the predictions and the frames together to get a video
# showing the saliency prediction

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from PIL import Image
from skimage import img_as_ubyte
import io
import os

frames_root = 'generar_videos/frames_originales/'
heatmaps_root = 'generar_videos/heatmaps/'
output_root = 'generar_videos/heat+pred/'

video_list = ['1An41lDIJ6Q25', '6QUCaLvQ_3I60', '8ESEI0bqrJ425', '8feS1rNYEbg30', 'ByBF08H_wDA30', 'dd39herpgXA25', 'ey9J7w98wlI50', 'fryDy9YcbI430', 'idLVnagjl_s30', 'kZB3KMhqqyI30', 'MzcdEI_tSUc25', 'RbgxpagCY_c30']
format_list = ['BCE', 'CC', 'KL', 'NSS', 'Original']
format_list = ['Original']

def blend_images(frame_path, heatmap_path, output_path):
    #print(f'Frame_path: {frame_path}, heatmap_path: {heatmap_path}')
    frame = cv2.imread(frame_path, cv2.IMREAD_UNCHANGED)
    #frame = cv2.resize(frame, (640, 480), Image.ANTIALIAS)
    heatmap = cv2.imread(heatmap_path, cv2.IMREAD_UNCHANGED)
    heatmap = cv2.resize(heatmap, (2560, 1440), Image.ANTIALIAS)
    #cv2.imshow('Heatmap', heatmap)
    #cv2.imshow('Frame', frame)
    blended = cv2.addWeighted(frame, 1.0, heatmap, 0.7, 0)
    #cv2.imshow('Blended Image',blended)
    cv2.imwrite(output_path, blended)


for form in format_list: # For each format
    print(f'FORMAT: {form}')
    for video in video_list[6:]: # For each video
        print(f'   Video: {video}')
        video_names = [hm for hm in os.listdir(f'{heatmaps_root}/{form}/{video}')
                                if hm.endswith(('.jpg', '.jpeg', '.png'))]
        for idx, v in enumerate(video_names):
            video_names[idx] = video_names[idx].split(".")[0]

        total = len(video_names)
        for idx, name in enumerate(video_names):
            frame_name = f'{video_names[idx].zfill(3)}.jpeg'
            heatmap_name = f'{video_names[idx]}.jpg'
            frame_path = f'{frames_root}{video}/{frame_name}'
            heatmap_path = f'{heatmaps_root}{form}/{video}/{heatmap_name}'
            output_path = f'{output_root}{form}/{video}/{frame_name}'
            blend_images(frame_path, heatmap_path, output_path)
            if idx % 100 == 0:
                print(f'      {idx} / {total}')
