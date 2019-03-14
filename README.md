# OpenVINO-YOLO
Inference of YoloV3 / tiny-YoloV3 on Laptop & RaspberryPi3 & NCS2
 
### Inspired and based on 

**https://github.com/PINTO0309/OpenVINO-YoloV3**

### Video 'street.mp4'

**https://www.youtube.com/watch?v=OEygtMfTbEY&t=19s**

### Clone Repository && Download Models
```bash
git clone https://github.com/gplast/OpenVINO-YOLO.git
cd OpenVINO-YOLO/
./dowload_all.sh # Use this to download all the models
```

### openvino_test (python) :
```bash
usage: openvino_test.py [-h] [-d DEVICE] [-s SIZE] [-v VIDEO] [--tiny]

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Specify the target device to infer on; CPU, GPU, FPGA
                        or MYRIAD is acceptable. Sample will look for a
                        suitable plugin for device specified (CPU by default)
  -s SIZE, --size SIZE  Specify the CNN input size
  -v VIDEO, --video VIDEO
                        Specify the name of the input video (CAMERA by
                        default)
  --tiny                Use tiny-YoloV3

```

### YoloV3 on Laptop CPU
```bash
python3 openvino_test.py -d CPU
```

### YoloV3 on Neural Compute Stick 2
```bash
python3 openvino_test.py -d MYRIAD
```

### Tiny-YoloV3 on Laptop CPU
```bash
python3 openvino_test.py -d CPU --tiny
```

### Tiny-YoloV3 on Neural Compute Stick 2
```bash
python3 openvino_test.py -d MYRIAD --tiny
```

### openvino_MultiStick_test (python) :
```bash
usage: openvino_MultiStick_test.py [-h] [-numncs NUMBER_OF_NCS] [-s SIZE]
                                   [-v VIDEO] [--tiny]

optional arguments:
  -h, --help            show this help message and exit
  -numncs NUMBER_OF_NCS, --numberofncs NUMBER_OF_NCS
                        Number of NCS. (Default=1)
  -s SIZE, --size SIZE  Specify the CNN input size
  -v VIDEO, --video VIDEO
                        Specify the name of the input video (CAMERA by
                        default)
  --tiny                Use tiny-YoloV3

```

### Multistick - YoloV3 on Neural Compute Stick 2
```bash
python3 openvino_MultiStick_test.py -numncs 1 #specify the number of NCS2
```

### Multistick - Tiny-YoloV3 on Neural Compute Stick 2
```bash
python3 openvino_MultiStick_test.py --tiny -numncs 1 #specify the number of NCS2
```

### OpenVINO C++ Usage
```bash
./object_detection_demo_yolov3_async -h
InferenceEngine: 
    API version ............ <version>
    Build .................. <number>

object_detection_demo_yolov3_async [OPTION]
Options:

    -h                        Print a usage message.
    -i "<path>"               Required. Path to a video file (specify "cam0" to work with camera).
    -m "<path>"               Required. Path to an .xml file with a trained model.
      -l "<absolute_path>"    Optional. Required for CPU custom layers.Absolute path to a shared library with the layers implementation.
          Or
      -c "<absolute_path>"    Optional. Required for GPU custom kernels.Absolute path to the .xml file with the kernels description.
    -d "<device>"             Optional. Specify a target device to infer on (CPU, GPU). The demo will look for a suitable plugin for the specified device
    -pc                       Optional. Enable per-layer performance report.
    -r                        Optional. Output inference results raw values showing.
    -t                        Optional. Probability threshold for detections.
    -iou_t                    Optional. Filtering intersection over union threshold for overlapping boxes.
    -auto_resize              Optional. Enable resizable input with support of ROI crop and auto resize.
```  

This Script will build main.cpp and object_detection_demo_yolov3_async.hpp from cpp and create the executable
```bash
sudo ./compile_cpp.sh

#YoloV3 - CPU
cpp/./object_detection_demo_yolov3_async -i street.mp4 -m lrmodels/YoloV3/FP32/frozen_yolo_v3.xml -d CPU -t 0.2

#YoloV3 - GPU
cpp/./object_detection_demo_yolov3_async -i street.mp4 -m lrmodels/YoloV3/FP32/frozen_yolo_v3.xml -d GPU -t 0.2

#YoloV3 - MYRIAD
cpp/./object_detection_demo_yolov3_async -i street.mp4 -m lrmodels/YoloV3/FP16/frozen_yolo_v3.xml -d MYRIAD -t 0.2


#Tiny-YoloV3 - CPU
cpp/./object_detection_demo_yolov3_async -i street.mp4 -m lrmodels/tiny-YoloV3/FP32/frozen_tiny_yolo_v3.xml -d CPU -t 0.2

#Tiny-YoloV3 - GPU
cpp/./object_detection_demo_yolov3_async -i street.mp4 -m lrmodels/tiny-YoloV3/FP32/frozen_tiny_yolo_v3.xml -d GPU -t 0.2

#Tiny-YoloV3 - MYRIAD
cpp/./object_detection_demo_yolov3_async -i street.mp4 -m lrmodels/tiny-YoloV3/FP16/frozen_tiny_yolo_v3.xml -d MYRIAD -t 0.2
```

## Environment (YOU MUST USE TENSORFLOW <= 1.12.0)

- LaptopPC (Intel 8th Core i5-8250U)
- Ubuntu 18.04 x86_64
- RaspberryPi3
- Raspbian Stretch armv7l
- OpenVINO toolkit 2018 R5 (2018.5.455)
- Python 3.6
- OpenCV 4.0.1-openvino
- Tensorflow v1.11.0 or Tensorflow-GPU v1.11.0 (pip install)
- YoloV3 (MS-COCO)
- tiny-YoloV3 (MS-COCO)
- Intel Neural Compute Stick v2
  
<br>
<br>

# Environment construction procedure
### 1. Work with LaptopPC (Ubuntu 18.04)
1.OpenVINO R5 Full-Install. Execute the following command.
```bash
cd ~
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1tlDW_kDOchWbkZbfy5WfbsW-b_GpXgr7" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1tlDW_kDOchWbkZbfy5WfbsW-b_GpXgr7" -o l_openvino_toolkit_p_2018.5.445.tgz
tar -zxf l_openvino_toolkit_p_2018.5.445.tgz
rm l_openvino_toolkit_p_2018.5.445.tgz
cd l_openvino_toolkit_p_2018.5.445
sudo -E ./install_cv_sdk_dependencies.sh

## GUI version installer
sudo ./install_GUI.sh
 or
## CUI version installer
sudo ./install.sh
```
2.Configure the Model Optimizer. Execute the following command.
```bash
cd /opt/intel/computer_vision_sdk/install_dependencies
sudo -E ./install_cv_sdk_dependencies.sh
nano ~/.bashrc
source /opt/intel/computer_vision_sdk/bin/setupvars.sh

source ~/.bashrc
cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/install_prerequisites
sudo ./install_prerequisites.sh
```
3.【Optional execution】 Additional installation steps for the Intel® Movidius™ Neural Compute Stick v1 and Intel® Neural Compute Stick v2
```bash
sudo usermod -a -G users "$(whoami)"
cat <<EOF > 97-usbboot.rules
SUBSYSTEM=="usb", ATTRS{idProduct}=="2150", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idProduct}=="2485", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idProduct}=="f63b", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
EOF

sudo cp 97-usbboot.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo ldconfig
rm 97-usbboot.rules
```
4.【Optional execution】 Additional installation steps for processor graphics (GPU)
```bash
cd /opt/intel/computer_vision_sdk/install_dependencies/
sudo -E su
uname -r
4.15.0-42-generic #<--- display kernel version sample

### Execute only when the kernel version is older than 4.14
./install_4_14_kernel.sh

./install_NEO_OCL_driver.sh
sudo reboot
```

### 2. Work with RaspberryPi (Raspbian Stretch)
**[Note] Only the execution environment is introduced.**  
  
1.Execute the following command.
```bash
sudo apt update
sudo apt upgrade
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1rBl_3kU4gsx-x2NG2I5uIhvA3fPqm8uE" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1rBl_3kU4gsx-x2NG2I5uIhvA3fPqm8uE" -o l_openvino_toolkit_ie_p_2018.5.445.tgz
tar -zxvf l_openvino_toolkit_ie_p_2018.5.445.tgz
rm l_openvino_toolkit_ie_p_2018.5.445.tgz
sed -i "s|<INSTALLDIR>|$(pwd)/inference_engine_vpu_arm|" inference_engine_vpu_arm/bin/setupvars.sh
```
2.Execute the following command.
```bash
nano ~/.bashrc
### Add 1 row below
source /home/pi/inference_engine_vpu_arm/bin/setupvars.sh

source ~/.bashrc
### Successful if displayed as below
[setupvars.sh] OpenVINO environment initialized

sudo usermod -a -G users "$(whoami)"
sudo reboot
```
3.Update USB rule.
```bash
sh inference_engine_vpu_arm/install_dependencies/install_NCS_udev_rules.sh
### It is displayed as follows
Update udev rules so that the toolkit can communicate with your neural compute stick
[install_NCS_udev_rules.sh] udev rules installed
```
**[Note] OpenCV 4.0.1 will be installed without permission when the work is finished.
If you do not want to affect other environments, please edit environment variables after installation is completed.**
<br>
<br>
<br>
<br>

# Neural Compute Stick 2
**https://ncsforum.movidius.com/discussion/1302/intel-neural-compute-stick-2-information**

# Issue
**[OpenVINO failing on YoloV3's YoloRegion, only one working on FP16, all working on FP32](https://software.intel.com/en-us/forums/computer-vision/topic/804019)**  
**[Regarding YOLO family networks on NCS2. Possibly a work-around](https://software.intel.com/en-us/forums/computer-vision/topic/805425)**  
**[Convert YOLOv3 Model to IR](https://software.intel.com/en-us/forums/computer-vision/topic/805370)**  

# Reference
**https://github.com/opencv/opencv/wiki/Intel%27s-Deep-Learning-Inference-Engine-backend**
**https://github.com/opencv/opencv/wiki/Intel%27s-Deep-Learning-Inference-Engine-backend#raspbian-stretch**
