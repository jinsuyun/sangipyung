from lxml import etree
import json
import os
import glob
import cv2
import shutil


# ###################################################################################### #
# train:70,000 val:10,000 test:20,000(No annotations) total:100,000 images               #
# bus, traffic light, traffic sign, person, bike, truck, motor, car, train, and rider    #
# ###################################################################################### #
def size_check():
    label_path = '/mnt/hdd2/darknet/sanjabu/bdd100k_image'
    label_folder = glob.glob(os.path.join(label_path, '*.txt'))
    for file in label_folder:
        size = os.path.getsize(file)
        if size < 50:
            print(size, file)


def bdd():
    classes = {"person": 0, "bike": 1, "motor": 2, "bus": 3, "truck": 4, "traffic light": 5, "traffic sign": 6, "car": 7}
    new_classes = {"person": 0, "bike": 1, "motor": 2, "bus": 3, "truck": 4, "traffic light": 5, "traffic sign": 6, "center car": 7, "left car": 8, "right car": 9}

    label_path = '/mnt/hdd2/bdd100k/bdd100k/labels/100k/train'
    # label_path = '/mnt/hdd1/darknet/0830/test/label/'
    # img_path = '/mnt/hdd1/darknet/0830/test/image/'
    img_path = '/mnt/hdd2/bdd100k/bdd100k/images/100k/train/'

    # dst_label = '/mnt/hdd1/darknet/0830/test/label/'
    # dst_img = '/mnt/hdd1/darknet/0830/test/point_img/'
    dst_img_path = '/mnt/hdd2/darknet/sanjabu/1002/image/'
    dst_path = '/mnt/hdd2/darknet/sanjabu/1002/label/'
    label_folder = glob.glob(os.path.join(label_path, '*.json'))

    for json_file in sorted(label_folder):
        print(json_file)
        file_name = json_file.split('.')[0].split('.')[0]
        try:
            with open(json_file) as data_file:
                data = json.load(data_file)
        except ValueError as e:
            raise KeyError from e
        else:
            objects = data["frames"][0]['objects']
            # target_img = img_path + file_name.split('/')[-1] + '.jpg'
            # save_img = dst_img + file_name.split('/')[-1] + '.jpg'

            # line_color = (0, 255, 255)
            # target_img = cv2.imread(target_img)
            # target_img = cv2.line(target_img, (333, 720), (580, 300), line_color, 3)
            # target_img = cv2.line(target_img, (947, 720), (700, 300), line_color, 3)
            # cv2.imwrite(save_img, target_img)

            # points_l_x = []
            # points_l_y = []
            # points_c_x = []
            # points_c_y = []
            for object in objects:

                category = object["category"]
                if category in classes:
                    if category != 'car':
                        # shutil.copy(img_path + file_name.split('/')[-1] + '.jpg', dst_img_path)  # TODO: cnt
                        category = classes[category]
                        center_x, center_y, bbox_width, bbox_height, bbox_area = get_bbox(object)
                        make_text(category, center_x, center_y, bbox_width, bbox_height, file_name, dst_path)

                    else:
                        # shutil.copy(img_path + file_name.split('/')[-1] + '.jpg', dst_img_path)
                        center_x, center_y, bbox_width, bbox_height, bbox_area = get_bbox(object)

                        if bbox_area <= 2000:
                            continue
                        if center_y < 200:
                            continue
                        if bbox_width > bbox_height * 2:
                            continue

                        if center_y < (-420 / 247) * (center_x - 333) + 720:
                            category = 8  # 'left_car'
                            # target_img = cv2.line(target_img, (int(center_x), int(center_y)), (int(center_x), int(center_y)), (0, 255, 0), 5)
                        elif center_y < (420 / 247) * (center_x - 947) + 720:
                            category = 9  # 'right_car'
                            # target_img = cv2.line(target_img, (int(center_x), int(center_y)), (int(center_x), int(center_y)), (250, 0, 255), 5)
                        else:
                            category = 7  # 'center_car'
                            # target_img = cv2.line(target_img, (int(center_x), int(center_y)), (int(center_x), int(center_y)), (0, 255, 255), 5)

                        make_text(category, center_x, center_y, bbox_width, bbox_height, file_name, dst_path)
                        # cv2.imwrite(save_img, target_img)

                # exit()
                # if category == 'area/drivable':
                #     cnt += 1
                # if cnt == 1:
                #     shutil.copy(img_path + file_name.split('/')[-1] + '.jpg', dst_img)
                # lane_x = object["poly2d"]
                # for point in lane_x:
                #     # print(point)
                #     if point[2] == 'L':
                #         point_color = (0, 0, 255)  # Red
                #         points_l_x.append(point[0])
                #         points_l_y.append(point[1])
                #     else:
                #         point_color = (255, 0, 0)  # Blue
                #         points_c_x.append(point[0])
                #         points_c_y.append(point[1])
                #     target_img = cv2.line(target_img, (int(point[0]), int(point[1])), (int(point[0]), int(point[1])), point_color, 5)
                # selected_color = (0, 255, 0)
                # print(points_l_x)
                # print(points_l_y)
                # y_min = min(points_l_y)
                # # print('y_min: ', y_min)
                # thresh1 = y_min - 40
                # thresh2 = y_min + 40
                # points_th_y = []
                # points_th_x = []
                #
                # for i, y in enumerate(points_l_y):
                #     if thresh1 <= y <= thresh2:
                #         if 400 <= points_l_x[i] <= 800:
                #             points_th_y.append(y)
                #             points_th_x.append(points_l_x[i])
                #
                # point_x_min = min(points_th_x)
                # point_x_min_i = points_th_x.index(min(points_th_x))
                #
                # point_x_max = max(points_th_x)
                #
                # point_x_max_i = points_th_x.index(max(points_th_x))

                # target_img = cv2.line(target_img, (int(point_x_min), int(points_th_y[point_x_min_i])), (0, 640), selected_color, 5)
                # target_img = cv2.line(target_img, (int(point_x_max), int(points_th_y[point_x_max_i])), (1280, 640), selected_color, 5)
                # target_img = cv2.line(target_img, (int(point_x_min), int(points_th_y[point_x_min_i])), (256, 720), selected_color, 5)
                # target_img = cv2.line(target_img, (int(point_x_max), int(points_th_y[point_x_max_i])), (1024, 720), selected_color, 5)

                # print(points_c)

                # cv2.imwrite(save_img, target_img)

                # print(lane_x)
                # if category in classes:
                #     category = classes[category]
                #
                #     cnt += 1
                #     if cnt == 1:
                #         shutil.copy(img_path + file_name.split('/')[-1] + '.jpg', dst_img)
                #
                #     xmin = round(object["box2d"]["x1"])
                #     xmax = round(object["box2d"]["x2"])
                #     ymin = round(object["box2d"]["y1"])
                #     ymax = round(object["box2d"]["y2"])
                #
                #     center_x = (xmin + xmax) / 2
                #     center_x /= 1280
                #     center_y = (ymin + ymax) / 2
                #     center_y /= 720
                #     width_ratio = (xmax - xmin) / 1280
                #     height_ratio = (ymax - ymin) / 720
                #
                #     txt_name = dst_path + file_name.split('/')[-1].split('.')[0] + '.txt'
                #     fw = open(txt_name, 'a+')
                #     txt_content = "{} {} {} {} {}".format(category, center_x, center_y, width_ratio, height_ratio)
                #     fw.write(str(txt_content) + '\n')
                #     fw.close()

                # except KeyError:
                #     break


def get_bbox(object):
    xmin = round(object["box2d"]["x1"])
    xmax = round(object["box2d"]["x2"])
    ymin = round(object["box2d"]["y1"])
    ymax = round(object["box2d"]["y2"])
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2

    bbox_width = (xmax - xmin)
    bbox_height = (ymax - ymin)
    bbox_area = bbox_width * bbox_height
    return center_x, center_y, bbox_width, bbox_height, bbox_area


def make_text(category, center_x, center_y, bbox_width, bbox_height, file_name, dst_path):
    txt_name = dst_path + file_name.split('/')[-1].split('.')[0] + '.txt'
    fw = open(txt_name, 'a+')
    txt_content = "{} {} {} {} {}".format(category, center_x / 1280, center_y / 720, bbox_width / 1280, bbox_height / 720)
    fw.write(str(txt_content) + '\n')
    fw.close()


def coco():
    # COCO 2017
    classes = {"bench(15)": 8, "parking-meter(14)": 9, "cat(17)": 10, "dog(18)": 11}
    classes = [15, 14, 17, 18]
    path = '/mnt/hdd1/darknet/0713/annotations/instances_train2017.json'
    img_path = '/mnt/hdd1/darknet/0713/train2017/'
    dst_path = '/mnt/hdd1/darknet/0713/COCO_4class/label/'
    dst_img = '/mnt/hdd1/darknet/0713/BDD_8class/coco/image/'

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    try:
        print("Data loading . . . ")
        with open(path) as data_file:
            data = json.load(data_file)
    except ValueError as e:
        raise KeyError from e
    else:
        print("Converting json to darknet text file !!!")
        for list in data["images"]:
            image_id = list["id"]
            image_name = list["file_name"].split('.')[0]
            # print(image_id, image_name)
            imgWidth = list["width"]
            imgHeight = list["height"]
            cnt = 0
            for index in data["annotations"]:
                if index["image_id"] == image_id:
                    # print(image_id)
                    category_id = index["category_id"]
                    if category_id in classes:
                        if category_id == 15:
                            category_id = 8
                        if category_id == 14:
                            category_id = 9
                        if category_id == 17:
                            category_id = 10
                        if category_id == 18:
                            category_id = 11

                        x = int(index["bbox"][0])
                        y = int(index["bbox"][1])
                        w = int(index["bbox"][2])
                        h = int(index["bbox"][3])
                        center_x = (x + w / 2) / imgWidth
                        center_y = (y + h / 2) / imgHeight
                        width_ratio = w / imgWidth
                        height_ratio = h / imgHeight
                        # print(category_id, img_path + image_name + '.jpg')
                        # print(center_x, center_y, width_ratio, height_ratio)
                        # cnt += 1
                        # if cnt == 1:
                        #     shutil.copy(img_path + image_name + '.jpg', dst_img)
                        txt_name = dst_path + image_name + '.txt'
                        # print(txt_name)
                        fw = open(txt_name, 'a+')
                        txt_content = "{} {} {} {} {}".format(category_id, center_x, center_y, width_ratio, height_ratio)
                        fw.write(str(txt_content) + '\n')
                        fw.close()
        print("Bye~")


def list_up():
    img_path = '/mnt/hdd2/darknet/sanjabu/1002/image'
    folder = glob.glob(os.path.join(img_path, '*.jpg'))
    file = '/mnt/hdd2/darknet/sanjabu/1002/train_list.txt'
    for content in sorted(folder):
        fw = open(file, 'a+')
        fw.write(str(content) + '\n')
        fw.close()


def list_up_from_txt():
    img_path = '/mnt/hdd2/darknet/sanjabu/1002/label'
    folder = glob.glob(os.path.join(img_path, '*.txt'))
    file = '/mnt/hdd2/darknet/sanjabu/1002/train_list.txt'
    for content in sorted(folder):
        content = '/mnt/hdd2/bdd100k/bdd100k/images/100k/train/' + content.split('.')[0].split('/')[-1] + '.jpg'
        fw = open(file, 'a+')
        fw.write(str(content) + '\n')
        fw.close()


def matching():
    img_path = '/mnt/hdd2/darknet/sanjabu/1002/image'

    folder = glob.glob(os.path.join(img_path, '*.jpg'))
    img_list = []
    label_list = []

    for img in folder:
        img_list.append(img.split('.')[0].split('/')[-1])
    label_path = '/mnt/hdd2/darknet/sanjabu/1002/label'

    folder = glob.glob(os.path.join(label_path, '*.txt'))
    for label in folder:
        label_list.append(label.split('.')[0].split('/')[-1])
    cnt = 0
    for x in img_list:
        if x not in label_list:
            cnt += 1
            target = img_path + '/' + x + '.jpg'
            print(target)
            os.remove(target)
    print(cnt)


def change_name():
    img_path = '/mnt/hdd2/darknet/sanjabu/1002/image/'
    label_path = '/mnt/hdd2/darknet/sanjabu/1002/label/'

    folder = glob.glob(os.path.join(img_path, '*'))
    i = 1
    for file in sorted(folder):
        new = img_path + str(i) + '.jpg'
        print(file + '->' + new)
        os.rename(file, new)
        i += 1


def img2videoConvert():
    image_folder = '/mnt/hdd2/darknet/sanjabu/1110/CAM_FR_OUT/'
    image_paths = glob.glob(os.path.join(image_folder, '*.jpg'))
    width = 1280
    height = 960
    size = (width, height)
    thick = int((height + width) // 300)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("/mnt/hdd2/darknet/sanjabu/1110/CAM_FR_OUT.avi", fourcc, 25, size)

    for file in sorted(image_paths):
        img = cv2.imread(file)
        out.write(img)
    out.release()
    print("COMPLETED !!!!")


img2videoConvert()
# bdd()
# matching()
# list_up_from_txt()
# list_up()
# size_check()
# change_name()
