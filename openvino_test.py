import sys, os, cv2, time
import numpy as np, math
from argparse import ArgumentParser
from sys import platform
if platform == "win32":
    sys.path.insert(0,'C:\Intel\computer_vision_sdk\python\python3.6')
from openvino.inference_engine import IENetwork, IEPlugin

yolo_scale_13 = 13
yolo_scale_26 = 26
yolo_scale_52 = 52

classes = 80
coords = 4
num = 3
anchors = [10,14, 23,27, 37,58, 81,82, 135,169, 344,319]

LABELS = ("person", "bicycle", "car", "motorbike", "aeroplane",
          "bus", "train", "truck", "boat", "traffic light",
          "fire hydrant", "stop sign", "parking meter", "bench", "bird",
          "cat", "dog", "horse", "sheep", "cow",
          "elephant", "bear", "zebra", "giraffe", "backpack",
          "umbrella", "handbag", "tie", "suitcase", "frisbee",
          "skis", "snowboard", "sports ball", "kite", "baseball bat",
          "baseball glove", "skateboard", "surfboard","tennis racket", "bottle",
          "wine glass", "cup", "fork", "knife", "spoon",
          "bowl", "banana", "apple", "sandwich", "orange",
          "broccoli", "carrot", "hot dog", "pizza", "donut",
          "cake", "chair", "sofa", "pottedplant", "bed",
          "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
          "remote", "keyboard", "cell phone", "microwave", "oven",
          "toaster", "sink", "refrigerator", "book", "clock",
          "vase", "scissors", "teddy bear", "hair drier", "toothbrush")

label_text_color = (255, 255, 255)
label_background_color = (125, 175, 75)
box_color = (255, 128, 0)
box_thickness = 1

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-d", "--device", help="Specify the target device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. \
                                    Sample will look for a suitable plugin for device specified (CPU by default)", default="CPU", type=str)
    parser.add_argument("-s", "--size", help="Specify the CNN input size", default=416, type=int)
    parser.add_argument("-v", "--video", help="Specify the name of the input video (CAMERA by default)", default=0, type=str)
    parser.add_argument("--tiny", help="Use tiny-YoloV3", action="store_true")
    return parser


def EntryIndex(side, lcoords, lclasses, location, entry):
    n = int(location / (side * side))
    loc = location % (side * side)
    return int(n * side * side * (lcoords + lclasses + 1) + entry * side * side + loc)


class DetectionObject():
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0
    class_id = 0
    confidence = 0.0

    def __init__(self, x, y, h, w, class_id, confidence, h_scale, w_scale):
        self.xmin = int((x - w / 2) * w_scale)
        self.ymin = int((y - h / 2) * h_scale)
        self.xmax = int(self.xmin + w * w_scale)
        self.ymax = int(self.ymin + h * h_scale)
        self.class_id = class_id
        self.confidence = confidence


def IntersectionOverUnion(box_1, box_2):
    width_of_overlap_area = min(box_1.xmax, box_2.xmax) - max(box_1.xmin, box_2.xmin)
    height_of_overlap_area = min(box_1.ymax, box_2.ymax) - max(box_1.ymin, box_2.ymin)
    area_of_overlap = 0.0
    if (width_of_overlap_area < 0.0 or height_of_overlap_area < 0.0):
        area_of_overlap = 0.0
    else:
        area_of_overlap = width_of_overlap_area * height_of_overlap_area
    box_1_area = (box_1.ymax - box_1.ymin)  * (box_1.xmax - box_1.xmin)
    box_2_area = (box_2.ymax - box_2.ymin)  * (box_2.xmax - box_2.xmin)
    area_of_union = box_1_area + box_2_area - area_of_overlap
    retval = 0.0
    if area_of_union <= 0.0:
        retval = 0.0
    else:
        retval = (area_of_overlap / area_of_union)
    return retval


def ParseYOLOV3Output(blob, resized_im_h, resized_im_w, original_im_h, original_im_w, threshold, objects):

    out_blob_h = blob.shape[2]
    out_blob_w = blob.shape[3]

    side = out_blob_h
    anchor_offset = 0

    if len(anchors) == 18:   ## YoloV3
        if side == yolo_scale_13:
            anchor_offset = 2 * 6
        elif side == yolo_scale_26:
            anchor_offset = 2 * 3
        elif side == yolo_scale_52:
            anchor_offset = 2 * 0

    elif len(anchors) == 12: ## tiny-YoloV3
        if side == yolo_scale_13:
            anchor_offset = 2 * 3
        elif side == yolo_scale_26:
            anchor_offset = 2 * 0

    else:                    ## ???
        if side == yolo_scale_13:
            anchor_offset = 2 * 6
        elif side == yolo_scale_26:
            anchor_offset = 2 * 3
        elif side == yolo_scale_52:
            anchor_offset = 2 * 0

    side_square = side * side
    output_blob = blob.flatten()

    for i in range(side_square):
        row = int(i / side)
        col = int(i % side)
        for n in range(num):
            obj_index = EntryIndex(side, coords, classes, n * side * side + i, coords)
            box_index = EntryIndex(side, coords, classes, n * side * side + i, 0)
            scale = output_blob[obj_index]
            if (scale < threshold):
                continue
            x = (col + output_blob[box_index + 0 * side_square]) / side * resized_im_w
            y = (row + output_blob[box_index + 1 * side_square]) / side * resized_im_h
            height = math.exp(output_blob[box_index + 3 * side_square]) * anchors[anchor_offset + 2 * n + 1]
            width = math.exp(output_blob[box_index + 2 * side_square]) * anchors[anchor_offset + 2 * n]
            for j in range(classes):
                class_index = EntryIndex(side, coords, classes, n * side_square + i, coords + 1 + j)
                prob = scale * output_blob[class_index]
                if prob < threshold:
                    continue
                obj = DetectionObject(x, y, height, width, j, prob, (original_im_h / resized_im_h), (original_im_w / resized_im_w))
                objects.append(obj)
    return objects


def main_IE_infer():
    global cam_input
    global m_input_size
    args = build_argparser().parse_args()
    cam_input = args.video
    m_input_size = args.size

    window_name = "Video"
    cap = cv2.VideoCapture(cam_input)
    if cap.isOpened() != True:
        print("USB Camera Open Error!!!")
        sys.exit(0)
    camera_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    camera_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    wait_key_time = 1
    vidfps = 30
    cap.set(cv2.CAP_PROP_FPS, vidfps)
    fps = ""
    framepos = 0
    frame_count = 0
    skip_frame = 0
    elapsedTime = 0
    new_w = int(camera_width * min(m_input_size/camera_width, m_input_size/camera_height))
    new_h = int(camera_height * min(m_input_size/camera_width, m_input_size/camera_height))

    plugin = IEPlugin(device=args.device)
    if args.tiny: 
        if "MYRIAD" in args.device:
            model_xml = "lrmodels/tiny-YoloV3/FP16/frozen_tiny_yolo_v3.xml" #<--- MYRIAD Tiny-YoloV3
            model_bin = os.path.splitext(model_xml)[0] + ".bin"
        if "CPU" in args.device:
            if platform == "win32":
                plugin.add_cpu_extension("cpu_extension_avx2.dll") #<---- CPU extension for Windows
            else:
                plugin.add_cpu_extension("lib/libcpu_extension.so") #<---- CPU extension for Linux
            model_xml = "lrmodels/tiny-YoloV3/FP32/frozen_tiny_yolo_v3.xml"
            model_bin = os.path.splitext(model_xml)[0] + ".bin"
        if "GPU" in args.device:
            model_xml = "lrmodels/tiny-YoloV3/FP32/frozen_tiny_yolo_v3.xml"
            model_bin = os.path.splitext(model_xml)[0] + ".bin"
    else:
        if "MYRIAD" in args.device:
            model_xml = "lrmodels/YoloV3/FP16/frozen_yolo_v3.xml" #<--- MYRIAD YoloV3
            model_bin = os.path.splitext(model_xml)[0] + ".bin"
        if "CPU" in args.device:
            if platform == "win32":
                plugin.add_cpu_extension("cpu_extension_avx2.dll") #<---- CPU extension for Windows
            else:
                plugin.add_cpu_extension("lib/libcpu_extension.so") #<---- CPU extension for Linux
            model_xml = "lrmodels/YoloV3/FP32/frozen_yolo_v3.xml"
            model_bin = os.path.splitext(model_xml)[0] + ".bin"
        if "GPU" in args.device:
            model_xml = "lrmodels/YoloV3/FP32/frozen_yolo_v3.xml"
            model_bin = os.path.splitext(model_xml)[0] + ".bin"
    
    time.sleep(1)

    net = IENetwork(model=model_xml, weights=model_bin)
    input_blob = next(iter(net.inputs))
    exec_net = plugin.load(network=net)

    while cap.isOpened():
        t1 = time.time()

        ret, image = cap.read()
        if not ret:
            break

        resized_image = cv2.resize(image, (new_w, new_h), interpolation = cv2.INTER_CUBIC)
        canvas = np.full((m_input_size, m_input_size, 3), 128)
        canvas[(m_input_size-new_h)//2:(m_input_size-new_h)//2 + new_h,(m_input_size-new_w)//2:(m_input_size-new_w)//2 + new_w,  :] = resized_image
        prepimg = canvas
        prepimg = prepimg[np.newaxis, :, :, :]     # Batch size axis add
        prepimg = prepimg.transpose((0, 3, 1, 2))  # NHWC to NCHW
        outputs = exec_net.infer(inputs={input_blob: prepimg})

        objects = []

        for output in outputs.values():
            objects = ParseYOLOV3Output(output, new_h, new_w, camera_height, camera_width, 0.4, objects)

        # Filtering overlapping boxes
        objlen = len(objects)
        for i in range(objlen):
            if (objects[i].confidence == 0.0):
                continue
            for j in range(i + 1, objlen):
                if (IntersectionOverUnion(objects[i], objects[j]) >= 0.4):
                    if objects[i].confidence < objects[j].confidence:
                        objects[i], objects[j] = objects[j], objects[i]
                    objects[j].confidence = 0.0
        
        # Drawing boxes
        for obj in objects:
            if obj.confidence < 0.2:
                continue
            label = obj.class_id
            confidence = obj.confidence
            #if confidence >= 0.2:
            label_text = LABELS[label] + " (" + "{:.1f}".format(confidence * 100) + "%)"
            cv2.rectangle(image, (obj.xmin, obj.ymin), (obj.xmax, obj.ymax), box_color, box_thickness)
            cv2.putText(image, label_text, (obj.xmin, obj.ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, label_text_color, 1)

        cv2.putText(image, fps, (camera_width - 170, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Result", image)

        k = cv2.waitKey(33)
        if cv2.waitKey(1) & k==27:
            break

        elapsedTime = time.time() - t1
        fps = "(Playback) {:.1f} FPS".format(1/elapsedTime)

    cv2.destroyAllWindows()
    del net
    del exec_net
    del plugin


if __name__ == '__main__':
    sys.exit(main_IE_infer() or 0)

