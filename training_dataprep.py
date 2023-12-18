# 0 leukonychia
# 1 pitting
# 2 crumbling
# 3 red spot of lunula
# 4 hyperkeratosis
# 5 splinter hemorrhage
# 6 onycholysis
# 7 oil spot

import argparse
import os
import shutil
import random

def microedit(directory, change_list, delete_list):
    txt_filenames = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_filenames.append(filename)

    for txt_filename in txt_filenames:
        txt_filepath = os.path.join(directory, txt_filename)
        with open(txt_filepath, 'r') as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            flag = False
            for delete_number in delete_list:
                if line.startswith(delete_number):
                    flag = True
                    continue

            if flag == True:
                continue

            for change_number in change_list:
                if line.startswith(change_number):
                    line = '0' + line[1:]
            new_lines.append(line)

        with open(os.path.join(directory, txt_filename), 'w') as f:
            f.writelines(new_lines)

def erase_zero(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)

#dir1: images directory
#dir2: text files directory
#dir3: target directory to copy

def move_imagefile(dir1, dir2, dir3):
    txt_files = [f for f in os.listdir(dir2) if f.endswith('.txt')]

    for txt_file in txt_files:
        img_file = txt_file.replace('.txt', '.jpg')
        if os.path.exists(os.path.join(dir1, img_file)):
            shutil.copy(os.path.join(dir1, img_file), os.path.join(dir3, img_file))

def divide_data(dir_path, train_ratio, val_ratio):
    train_dir = os.path.join(dir_path, 'train')
    os.makedirs(train_dir, exist_ok=True)
    #train_ratio = 0.8

    val_dir = os.path.join(dir_path, 'validation')
    os.makedirs(val_dir, exist_ok=True)
    #val_ratio = 0.2

    test_dir = os.path.join(dir_path, 'test')
    os.makedirs(test_dir, exist_ok=True)
    test_ratio = 1-train_ratio-val_ratio

    file_list = os.listdir(dir_path)
    for file in file_list:
        if file.endswith('.jpg'):
            name, ext = os.path.splitext(file)
            text_file = name + '.txt'
            if os.path.exists(os.path.join(dir_path, text_file)):
                rand = random.random()
                if rand < train_ratio:
                    shutil.move(os.path.join(dir_path, file), os.path.join(train_dir, file))
                    shutil.move(os.path.join(dir_path, text_file), os.path.join(train_dir, text_file))
                elif rand < train_ratio + val_ratio:
                    shutil.move(os.path.join(dir_path, file), os.path.join(val_dir, file))
                    shutil.move(os.path.join(dir_path, text_file), os.path.join(val_dir, text_file))
                else:
                    shutil.move(os.path.join(dir_path, file), os.path.join(test_dir, file))
                    shutil.move(os.path.join(dir_path, text_file), os.path.join(test_dir, text_file))

def generate_text_file(dir_path, prefix):
    image_list = [f for f in os.listdir(dir_path) if f.endswith('.jpg')]
    with open (os.path.join(dir_path, 'image_list.txt'), 'w') as f:
        for image in image_list:
            f.write(os.path.join(prefix, image) + '\n')

def change_move_file (current_file_path, new_file_name, destination_directory):
    new_file_path = os.path.join(destination_directory, new_file_name)
    os.rename(current_file_path, new_file_path)

def move_files(file_list, src_dir, dest_img_dir, dest_label_dir):
    for file in file_list:
        if file.endswith('.jpg'):
            name, ext = os.path.splitext(file)
            text_file = name + '.txt'
            if os.path.exists(os.path.join(src_dir, text_file)):
                shutil.move(os.path.join(src_dir, file), os.path.join(dest_img_dir, file))
                shutil.move(os.path.join(src_dir, text_file), os.path.join(dest_label_dir, text_file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', type=str, default='', help='source directory')
    parser.add_argument('--txt_source', type=str, default='labels/training', help='text label source')
    parser.add_argument('--img_source', type=str, default='images/training', help='image source')
    args = parser.parse_args()

    leukonychia_dir = os.path.join(args.dir_path, 'leukonychia')
    os.makedirs(leukonychia_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, leukonychia_dir)

    pitting_dir = os.path.join(args.dir_path, 'pitting')
    os.makedirs(pitting_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, pitting_dir)

    crumbling_dir = os.path.join(args.dir_path, 'crumbling')
    os.makedirs(crumbling_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, crumbling_dir)

    redspot_dir = os.path.join(args.dir_path, 'redspot')
    os.makedirs(redspot_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, redspot_dir)

    hyperkeratosis_dir = os.path.join(args.dir_path, 'hyperkeratosis')
    os.makedirs(hyperkeratosis_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, hyperkeratosis_dir)

    splinter_dir = os.path.join(args.dir_path, 'splinter')
    os.makedirs(splinter_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, splinter_dir)

    onycholysis_dir = os.path.join(args.dir_path, 'onycholysis')
    os.makedirs(onycholysis_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, onycholysis_dir)

    oilspot_dir = os.path.join(args.dir_path, 'oilspot')
    os.makedirs(oilspot_dir, exist_ok=True)
    for filename in os.listdir(args.txt_source):
        filepath = os.path.join(args.txt_source, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, oilspot_dir)

    microedit(leukonychia_dir, ['0'], ['1', '2', '3', '4', '5', '6', '7'])
    microedit(pitting_dir, ['1'], ['0', '2', '3', '4', '5', '6', '7'])
    microedit(crumbling_dir, ['2'], ['0', '1', '3', '4', '5', '6', '7'])
    microedit(redspot_dir, ['3'], ['0', '1', '2', '4', '5', '6', '7'])
    microedit(hyperkeratosis_dir, ['4'], ['0', '1', '2', '3', '5', '6', '7'])
    microedit(splinter_dir, ['5'], ['0', '1', '2', '3', '4', '6', '7'])
    microedit(onycholysis_dir, ['6'], ['0', '1', '2', '3', '4', '5', '7'])
    microedit(oilspot_dir, ['7'], ['0', '1', '2', '3', '4', '5', '6'])

    erase_zero(leukonychia_dir)
    erase_zero(pitting_dir)
    erase_zero(crumbling_dir)
    erase_zero(redspot_dir)
    erase_zero(hyperkeratosis_dir)
    erase_zero(splinter_dir)
    erase_zero(onycholysis_dir)
    erase_zero(oilspot_dir)

    move_imagefile(args.img_source, leukonychia_dir, leukonychia_dir)
    move_imagefile(args.img_source, pitting_dir, pitting_dir)
    move_imagefile(args.img_source, crumbling_dir, crumbling_dir)
    move_imagefile(args.img_source, redspot_dir, redspot_dir)
    move_imagefile(args.img_source, hyperkeratosis_dir, hyperkeratosis_dir)
    move_imagefile(args.img_source, splinter_dir, splinter_dir)
    move_imagefile(args.img_source, onycholysis_dir, onycholysis_dir)
    move_imagefile(args.img_source, oilspot_dir, oilspot_dir)

    dir_list = [leukonychia_dir, pitting_dir, crumbling_dir, redspot_dir, hyperkeratosis_dir, splinter_dir, onycholysis_dir, oilspot_dir]
    for dir_path in dir_list:
        divide_data(dir_path, 0.8, 0.2)

        os.makedirs("images", exist_ok=True)
        os.makedirs("labels", exist_ok=True)

        os.makedirs("images/train2017", exist_ok=True)
        os.makedirs("images/val2017", exist_ok=True)
        os.makedirs("images/test2017", exist_ok=True)

        os.makedirs("labels/train2017", exist_ok=True)
        os.makedirs("labels/val2017", exist_ok=True)
        os.makedirs("labels/test2017", exist_ok=True)

        train_dir = os.path.join(dir_path, 'train')
        val_dir = os.path.join(dir_path, 'validation')
        test_dir = os.path.join(dir_path, 'test')

       #leukonychia_dir 안에 image directory 만들기

        generate_text_file(train_dir, './images/train2017/')
        generate_text_file(val_dir, './images/train2017/')
        generate_text_file(test_dir, './images/train2017/')

        change_move_file(os.path.join(train_dir, 'image_list.txt'), 'train2017.txt', dir_path)
        change_move_file(os.path.join(val_dir, 'image_list.txt'), 'val2017.txt', dir_path)
        change_move_file(os.path.join(test_dir, 'image_list.txt'), 'test2017.txt', dir_path)

        train_images_dir = os.path.join(dir_path, 'images/train2017')
        os.mkdir(os.path.join(dir_path, 'images/'))
        os.mkdir(os.path.join(dir_path, 'labels/'))
        os.mkdir(train_images_dir)
        val_images_dir = os.path.join(dir_path, 'images/val2017')
        os.mkdir(val_images_dir)
        test_images_dir = os.path.join(dir_path, 'images/test2017')
        os.mkdir(test_images_dir)
        train_labels_dir = os.path.join(dir_path, 'labels/train2017')
        os.mkdir(train_labels_dir)
        val_labels_dir = os.path.join(dir_path, 'labels/val2017')
        os.mkdir(val_labels_dir)
        test_labels_dir = os.path.join(dir_path, 'labels/test2017')
        os.mkdir(test_labels_dir)

        move_files(os.listdir(train_dir), train_dir, train_images_dir, train_labels_dir)
        move_files(os.listdir(val_dir), val_dir, val_images_dir, val_labels_dir)
        move_files(os.listdir(test_dir), test_dir, test_images_dir, test_labels_dir)








