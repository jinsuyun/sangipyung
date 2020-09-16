import os
import glob

img_width = 960
img_height = 540


# 0: vehicle
# 1: person

def convert_annotation(center_x, center_y, box_width, box_height):
    left = (center_x - box_width / 2) * img_width
    right = (center_x + box_width / 2) * img_width
    top = (center_y - box_height / 2) * img_height
    bottom = (center_y + box_height / 2) * img_height
    return int(left), int(top), int(right), int(bottom)


carla_gt_path = '/home/say2dbs/kookmin_data/data/'
with open(carla_gt_path + 'class.names') as f:
    class_names = f.readlines()
    class_names = [x.strip() for x in class_names]

carla_gt_folder = glob.glob(os.path.join(carla_gt_path + 'gt', '*.txt'))
cp_dest = '/mnt/hdd1/YOLOv2/mAP/ground-truth/'
for gt_files in sorted(carla_gt_folder):
    image_name = gt_files.split(".txt", 1)[0].split("/")[-1]
    print(image_name)
    with open(gt_files) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    for line in lines:
        class_name, center_x, center_y, box_width, box_height = line.split()
        class_name = class_names[int(class_name)]
        left, top, right, bottom = convert_annotation(float(center_x), float(center_y), float(box_width), float(box_height))
        new_txt = cp_dest + image_name + '.txt'
        fw = open(new_txt, 'a+')
        txt_content = "{} {} {} {} {}".format(class_name, left, top, right, bottom)
        fw.write(str(txt_content) + '\n')
        fw.close()

print("Conversion completed!")
