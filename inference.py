from keras.models import load_model
import cv2
import os
import numpy as np
from utils.utils import get_yolo_boxes, makedirs
from utils.bbox import draw_boxes


def load_the_model():
    os.environ['CUDA_VISIBLE_DEVICES'] = "0"
    loaded_model = load_model('raccoon.h5')
    return loaded_model


class Model(object):
    def __init__(self):
        self.model = load_the_model()

    def predict(self):
        net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
        obj_thresh, nms_thresh = 0.5, 0.45
        # For testing
        input_path = 'raccoon-188.jpg'
        output_path = 'C:\\Users\\colsson\\uploads\\predictions\\'

        anchors = [55, 69, 75, 234, 133, 240, 136, 129, 142, 363, 203, 290, 228, 184, 285, 359, 341, 260]
        # Required because of a bug in Keras when using tensorflow graph cross threads
        image_paths = []

        if os.path.isdir(input_path):
            for inp_file in os.listdir(input_path):
                image_paths += [input_path + inp_file]
        else:
            image_paths += [input_path]

        image_paths = [inp_file for inp_file in image_paths if (inp_file[-4:] in ['.jpg', '.png', 'JPEG'])]

        for image_path in image_paths:
            image = cv2.imread(image_path)

            # predict the bounding boxes
            boxes = \
                get_yolo_boxes(self.model, [image], net_h, net_w, anchors, obj_thresh, nms_thresh)[0]

            # draw bounding boxes on the image using labels
            draw_boxes(image, boxes, ['raccoon'], obj_thresh, quiet=True)

            # write the image with bounding boxes to file
            cv2.imwrite(output_path + image_path.split('/')[-1], np.uint8(image))

            prediction = {'result': "hej"}

        return prediction

    def predict_file(self, filepath):
        net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
        obj_thresh, nms_thresh = 0.5, 0.45
        # For testing
        input_path = filepath
        print("The filepath is: " + str(filepath))
        # output_path = 'C:\\Users\\colsson\\uploads\\predictions\\'
        output_path = 'C:\\Users\\colsson\\PycharmProjects\\keras_flask\\app\\static\\'
        anchors = [55, 69, 75, 234, 133, 240, 136, 129, 142, 363, 203, 290, 228, 184, 285, 359, 341, 260]
        # Required because of a bug in Keras when using tensorflow graph cross threads
        image_paths = []

        if os.path.isdir(input_path):
            for inp_file in os.listdir(input_path):
                image_paths += [input_path + inp_file]
        else:
            image_paths += [input_path]

        image_paths = [inp_file for inp_file in image_paths if (inp_file[-4:] in ['.jpg', '.png', 'JPEG'])]

        for image_path in image_paths:
            image = cv2.imread(image_path)

            # predict the bounding boxes
            boxes = \
                get_yolo_boxes(self.model, [image], net_h, net_w, anchors, obj_thresh, nms_thresh)[0]

            # draw bounding boxes on the image using labels
            draw_boxes(image, boxes, ['raccoon'], obj_thresh, quiet=False)

            # write the image with bounding boxes to file
            #cv2.imwrite(output_path + image_path.split('/')[-1], np.uint8(image))
            # result_filepath = output_path + image_path.split('\\')[-1]
            result_filepath = image_path.split('\\')[-1]
            cv2.imwrite(output_path + image_path.split('\\')[-1], np.uint8(image))
            #print(str(output_path + image_path.split('\\')[-1]))
            prediction = {'result': "hej filepath!"}

        return result_filepath



if __name__ == '__main__':
    pass
    model = Model()
    #print(model.predict())
