import csv
import numpy as np
import os
import cv2
import shutil
from scipy import ndimage as ndi
from scipy.io import savemat

# Hardcoded data to access with ease later
video_names = ['1An41lDIJ6Q25', '6QUCaLvQ_3I60', '8ESEI0bqrJ425', '8feS1rNYEbg30', 'ByBF08H-wDA30', 'dd39herpgXA25',
                'ey9J7w98wlI50', 'fryDy9YcbI430', 'idLVnagjl_s30', 'kZB3KMhqqyI30', 'MzcdEI-tSUc25', 'RbgxpagCY_c_230']
video_fps = [25, 60, 25, 30, 30, 25, 50, 30, 30, 30, 25, 30]
video_durations = [25, 25, 25, 25, 25, 25, 25, 26, 25, 25, 25, 23]

save_images = False # If we want to save the ground truth saliency images
update_mat = True # If we want to update the .mat files
sigma = 20

video = 7
num_fps = video_fps[video]
vid_duration = video_durations[video]
vid_name = video_names[video]

total_frames = num_fps * vid_duration
loop_iterations = total_frames # Value to debug faster. It varies between 10 and total_frames

print(f'Loading video {vid_name} with {vid_duration} seconds at {num_fps} fps (total: {total_frames} frames)')

frame_duration = 1/num_fps # Duration of each frame in seconds
width = 645 # A bit oversized for numerical imprecissions ~~
height = 485

# ======================= GET FIXATION MATRICES =======================
print('++Getting fixation matrices...')

fix_matrix = np.zeros((total_frames+5,height,width)) # Initialize video matrix
for participant in os.listdir(f'ambix_data/{vid_name}'): # For each participant
    #print(f'========PARTICIPANT: {participant}========')
    with open(f'ambix_data/{vid_name}/{participant}', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        current_frame = 0 # Counter to access the fix_matrix later
        num_samples = 0 # Samples read at the current frame
        pos_acum = (0,0)
        for row in csvreader:
            # Read the values in the row
            read_pos = (float(row[3]), float(row[2]))           
            real_pos = (int(read_pos[0] * 480), int(read_pos[1] * 640))
            timestamp = float(row[1])
            
            if timestamp >= (current_frame+1) * frame_duration: # Sample in the next frame
                # Save the previous frame data
                pos_acum = (int(pos_acum[0] / max(num_samples,1)), int(pos_acum[1] / max(num_samples,1))) # Normalize the samples
                #print(f'==>He guardado en el frame {current_frame} un {pos_acum}.')
                fix_matrix[current_frame-1][pos_acum] = 1 # Set the fixation to 1

                current_frame = current_frame + 1 # Update frame counter
                num_samples = 1 # Reset the number of samples for the new frame
                pos_acum = real_pos # Count the new fixation
            
            else: # Sample in the current frame -> Keep counting
                pos_acum = (pos_acum[0] + real_pos[0], pos_acum[1] + real_pos[1]) # Acum the fixation point
                num_samples = num_samples + 1 # Acum the number of samples in frame
                #print(f'Estoy en el frame {current_frame} - ts: {timestamp}, posición leída: {real_pos} (sample {num_samples})')
            
        pos_acum = (int(pos_acum[0] / num_samples), int(pos_acum[1] / num_samples)) # Normalize the samples
        fix_matrix[current_frame-1][pos_acum] = 1 # Set the fixation to 1
        #print(f'==>He guardado en el (ultimo) frame {current_frame} un {pos_acum}.')


# ====================== GET SALIENCY MATRICES (AND SAVE?) ======================
print('++Getting saliency matrices...')

sal_matrix = np.zeros((total_frames+5,height,width)) # Initialize saliency matrix
for frame in range(0,loop_iterations): # Compute gaussian blur for each frame
    sal_matrix[frame] = ndi.gaussian_filter(fix_matrix[frame]*255, sigma=sigma)
    #cv2.imshow("Saliency map", sal_matrix[frame])
    #cv2.waitKey()

if save_images: # Do we want to save the saliency images?
    print('++Saving saliency images...')
    shutil.rmtree(f'./output/{vid_name}', ignore_errors=True)
    os.mkdir(f'./output/{vid_name}')
    for frame in range(0,loop_iterations): # Save every frame of a video
        cv2.imwrite(f'./output/{vid_name}/{str(frame+1).zfill(3)}.jpg', (sal_matrix[frame]*255).astype(np.uint16))
else:
    print('--NOT saving saliency images')
# ====================== SAVE .mat FILES FOR MATLAB ======================

if update_mat:
    print('++Saving .mat files...')
    shutil.rmtree(f'./matlab_files/fixmaps/{vid_name}', ignore_errors=True)
    os.mkdir(f'./matlab_files/fixmaps/{vid_name}')
    shutil.rmtree(f'./matlab_files/salmaps/{vid_name}', ignore_errors=True)
    os.mkdir(f'./matlab_files/salmaps/{vid_name}')

    for frame in range(0,loop_iterations):
        savemat(f'./matlab_files/fixmaps/{vid_name}/{str(frame+1).zfill(3)}.mat', {'data': fix_matrix[frame]})
        savemat(f'./matlab_files/salmaps/{vid_name}/{str(frame+1).zfill(3)}.mat', {'data': sal_matrix[frame]/255})
else:
    print('--NOT updating mat files')

#total_puntitos = fix_matrix.sum()
#print(f'En total hay {total_puntitos} fix points :>')

# img1 = fix_matrix[0]
# print(f'En la primera imagen hay {img1.sum()} fix points')

# cv2.imshow("Fixation map", img1*255)
# cv2.waitKey()
# blurred = ndi.gaussian_filter(img1*255, sigma=sigma)
# cv2.imshow("Saliency map", blurred)
# cv2.waitKey()
# print(f'En total hay {blurred.sum()} valores :>')

# image = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
# blurred.show()
