from typing import Union, List, Dict
import glob
import os 
from PIL import Image

def feature_list(data, feature_name):
    lists = data[feature_name]
    lists_drop = lists.drop_duplicates(keep='first')
    return lists_drop.values.tolist()

def option_append(data, feature_names):
    options = []
    for feature in feature_names:
        new_list = feature_list(data, feature)
        options = options + new_list
    return options

def create_options(data, feature):
    # Define list of selection options
    options = [ ]
    features = [ ]
    features.append(feature)
    #selection = ['형태', '제작자', '용도 3' ]
    #selection = ['형태', '용도 3' ]
    #print(feature)
    options = option_append(data, features)
    return options

def create_image_paths(image_folder, extension):
    image_paths = []
    format = image_folder + '/*' + extension
    # for filename in glob.glob('C:/Users/SCI/Desktop/self_driving/Midterm/train/*.jpg'): #assuming jpg
    for filename in glob.glob(format): #assuming jpg
        image_paths.append(filename)
    return image_paths

def resize_imgs(new_size, dir, extension):
    file_list = glob.glob(dir + "/*." + extension)
    new_files = []
    dict = {}
    if(not os.path.isdir(dir + '_resize/')):
        os.makedirs(dir + '_resize/')
    for file in file_list:
        title = os.path.split(file)
        #print(title[1])
        resize_file = dir + '_resize/' + title[1]
        dict[title[1].split('_')[0]] = resize_file
        if os.path.isfile(resize_file):
            new_files.append(resize_file)
            continue
        else:
            img = Image.open(file)
            img_resize = img.resize((new_size, new_size))
            title = os.path.split(file)
            print(title[1] + " doesn't exist..",end=' ')
            print("resize & save "+title[1])
            img_resize.save(resize_file)
        new_files.append(resize_file)
    return new_files, dict

def get_feature_label(image_path):
    features = []
    labels = []
    x = Image.open(image_path)
    y = get_class_label(image_path.split('_')[-1])
    return x, y

def get_class_label(image_name):
    # your method here
    return image_name

#def change_name():
    