import os
import numpy as np
import argparse
import pandas as pd
import shutil
import cv2


def feature_NAPSI(data_dir, dir_image):
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            # Read in the YOLO annotation text file
            with open(os.path.join(data_dir, filename), 'r') as f:
                lines = f.readlines()

                # Read in the corresponding image
                img_filename = os.path.join(dir_image, os.path.splitext(filename)[0] + '.jpg')
                img = cv2.imread(img_filename)

                # Determine the center point of the image
                center_x = img.shape[1] / 2
                center_y = img.shape[0] / 2

                # Create an array to hold the scores for each quadrant
                # [0,0,0,0]
                scores = np.zeros((4,))

                # Iterate over each object in the annotation file
                for line in lines:
                    # Parse the object's class, center coordinates, and width and height
                    class_id, x_center, y_center, width, height = map(float, line.strip().split())

                    # Calculate the top-left and bottom-right coordinates of the bounding box
                    x_min = int((x_center - width / 2) * img.shape[1])
                    y_min = int((y_center - height / 2) * img.shape[0])
                    x_max = int((x_center + width / 2) * img.shape[1])
                    y_max = int((y_center + height / 2) * img.shape[0])
                    points = np.array([(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)])
                    # Determine which quadrant the bounding box falls into
                    for i in range(4):
                        if points[i, 0] >= center_x and points[i, 1] <= center_y:
                            # Quadrant 1
                            scores = scores + [1, 0, 0, 0]
                        elif points[i, 0] <= center_x and points[i, 1] <= center_y:
                            # Quadrant 2
                            scores = scores + [0, 1, 0, 0]
                        elif points[i, 0] <= center_x and points[i, 1] >= center_y:
                            # Quadrant 3
                            scores = scores + [0, 0, 1, 0]
                        elif points[i, 0] >= center_x and points[i, 1] >= center_y:
                            # Quadrant 4
                            scores = scores + [0, 0, 0, 1]

                # Print the scores for the current image
                # print('Scores for', filename)
                # print(scores)

                # Write the scores to a new text file
                for i in range(4):
                    if scores[i] > 0:
                        scores[i] = 1

                score_filename = os.path.join(os.path.join(data_dir, "scores"),
                                              os.path.splitext(filename)[0] + '_scores.txt')
                with open(score_filename, 'w') as f:
                    f.write(' '.join(str(score) for score in scores))


def text_filename_extract(dir_image):
    txt_file_list = []
    for filename in os.listdir(dir_image):
        if filename.endswith(".jpg"):
            txt_file_list.append(filename.replace(".jpg", ".txt"))

    return txt_file_list

def sumup_scores(dir_text, dir_path1, dir_path2, dir_path3, dir_path4, dir_dest):
    text_filenames = text_filename_extract(dir_text)
    for text_filename in text_filenames:
        data = [0, 0, 0, 0]
        if text_filename in os.listdir(dir_path1):
            data = np.loadtxt(
                os.path.join(dir_path1, "scores", os.path.splitext(text_filename)[0] + '_scores' + '.txt'))
        if text_filename in os.listdir(dir_path2):
            data = [x + y for x, y in zip(data, np.loadtxt(
                os.path.join(dir_path2, "scores", os.path.splitext(text_filename)[0] + '_scores' + '.txt')))]
        if text_filename in os.listdir(dir_path3):
            data = [x + y for x, y in zip(data, np.loadtxt(
                os.path.join(dir_path3, "scores", os.path.splitext(text_filename)[0] + '_scores' + '.txt')))]
        if text_filename in os.listdir(dir_path4):
            data = [x + y for x, y in zip(data, np.loadtxt(
                os.path.join(dir_path4, "scores", os.path.splitext(text_filename)[0] + '_scores' + '.txt')))]

        data = [1 if x >= 1 else 0 for x in data]
        # result = np.sum(data, axis=0)
        with open(os.path.join(dir_dest, text_filename), 'w') as f:
            f.write(' '.join(str(score) for score in data))

def generate_csv_result(dir_path, dir_dest):
    # Define the directory where the text files are located
    # dir_path = '/home/abcultra/napsi_human/matrix/sum'

    # Create an empty list to store the dataframes
    dfs = []

    # Loop through all the files in the directory
    for filename in os.listdir(dir_path):
        # Check if the file is a text file
        if filename.endswith('.txt'):
            # Load the data from the text file into a numpy array
            data = pd.read_csv(os.path.join(dir_path, filename), sep=' ', header=None)
            # Create a dataframe with the data
            df = pd.DataFrame(data)
            # Add the filename as a column to the dataframe
            df.insert(0, 'filename', filename)
            # Rename the columns to be more descriptive
            df.columns = ['filename', 'component1', 'component2', 'component3', 'component4']
            # Add the dataframe to the list
            dfs.append(df)

    # Concatenate all the dataframes into a single dataframe
    result = pd.concat(dfs)

    # Save the resulting dataframe to a csv file
    result.to_csv(os.path.join(dir_dest), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', type=str, default='runs/detect', help='source directory')
    parser.add_argument('--dir_image', type=str, default='napsi_test_images', help='image directory')
    parser.add_argument('--dir_leukonychia', type=str, default='runs/detect/leukonychia/labels', help='leukonychia label')
    parser.add_argument('--dir_pitting', type=str, default='runs/detect/pitting/labels', help='pitting')
    parser.add_argument('--dir_crumbling', type=str, default='runs/detect/crumbling/labels', help='crumbling')
    parser.add_argument('--dir_redspot', type=str, default='runs/detect/redspot/labels', help='redspot')
    parser.add_argument('--dir_hyperkeratosis', type=str, default='runs/detect/hyperkeratosis/labels', help='hyperkeratosis')
    parser.add_argument('--dir_splinter', type=str, default='runs/detect/splinter/labels', help='splinter')
    parser.add_argument('--dir_onycholysis', type=str, default='runs/detect/onycholysis/labels', help='onycholysis')
    parser.add_argument('--dir_oilspot', type=str, default='runs/detect/oilspot/labels', help='oilspot')

    args = parser.parse_args()

    os.makedirs(os.path.join(args.dir_path, "matrix"), exist_ok=True)
    os.makedirs(os.path.join(args.dir_path, "matrix/sum"), exist_ok=True)
    os.makedirs(os.path.join(args.dir_path, "bed"), exist_ok=True)
    os.makedirs(os.path.join(args.dir_path, "bed/sum"), exist_ok=True)

    dir_list = [os.path.join(args.dir_path,'leukonychia'), os.path.join(args.dir_path,'pitting'),os.path.join(args.dir_path,'crumbling'),os.path.join(args.dir_path,'redspot'),os.path.join(args.dir_path,'hyperkeratosis'),
                os.path.join(args.dir_path,'splinter'),os.path.join(args.dir_path,'onycholysis'),os.path.join(args.dir_path,'oilspot')]

    dir_path0 = os.path.join(args.dir_path, "leukonychia")
    dir_path1 = os.path.join(args.dir_path, "pitting")
    dir_path2 = os.path.join(args.dir_path, "crumbling")
    dir_path3 = os.path.join(args.dir_path, "redspot")

    dir_path4 = os.path.join(args.dir_path, "hyperkeratosis")
    dir_path5 = os.path.join(args.dir_path, "splinter")
    dir_path6 = os.path.join(args.dir_path, "onycholysis")
    dir_path7 = os.path.join(args.dir_path, "oilspot")

    dir_paths = {}
    for index, path in enumerate(dir_list):
        dir_paths[f'dir_path{index}'] = path

    dir_list_label = [args.dir_leukonychia, args.dir_pitting, args.dir_crumbling, args.dir_redspot, args.dir_hyperkeratosis, args.dir_splinter, args.dir_onycholysis, args.dir_oilspot]

    for index, directory in enumerate(dir_list_label):
        for txt_file in os.listdir(directory):
            if txt_file.endswith(".txt"):
                shutil.copy(os.path.join(directory, txt_file), dir_paths[f'dir_path{index}'])

    for directory in dir_list:
        if not os.path.exists(os.path.join(directory, "scores/")):
            os.mkdir(os.path.join(directory, "scores/"))
        feature_NAPSI(directory, args.dir_image)

    dir_matrix = os.path.join(args.dir_path, "matrix")
    dir_bed = os.path.join(args.dir_path, "bed")

    dir_matrix_sum = os.path.join(os.path.join(args.dir_path, "matrix"), "sum")
    dir_bed_sum = os.path.join(os.path.join(args.dir_path, "bed"), "sum")

    sumup_scores(args.dir_image, dir_path0, dir_path1, dir_path2, dir_path3, dir_matrix_sum)
    sumup_scores(args.dir_image, dir_path4, dir_path5, dir_path6, dir_path7, dir_bed_sum)

    generate_csv_result(dir_matrix_sum,os.path.join(dir_matrix, "matrix_result.csv"))
    generate_csv_result(dir_bed_sum,os.path.join(dir_bed, "bed_result.csv"))
