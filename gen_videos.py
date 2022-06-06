import os

video_list = ['1An41lDIJ6Q25', '6QUCaLvQ_3I60', '8ESEI0bqrJ425', '8feS1rNYEbg30', 'ByBF08H_wDA30', 'dd39herpgXA25', 'ey9J7w98wlI50', 'fryDy9YcbI430', 'idLVnagjl_s30', 'kZB3KMhqqyI30', 'MzcdEI_tSUc25', 'RbgxpagCY_c30']
format_list = ['BCE', 'CC', 'KL', 'NSS']
format_list = ['Original']

for form in format_list: # For each format
    print(f'FORMAT: {form}')
    for video in video_list: # For each video
        print(f'   Video: {video}')
        fps = video[-2:]
        path_entrada = f'generar_videos/heat+pred/{form}/{video}'
        path_salida = f'generar_videos/videos_sin_audio/{form}'
        os.system(f'ffmpeg -framerate {fps} -i {path_entrada}/%03d.jpeg {path_salida}/{video}.mp4')