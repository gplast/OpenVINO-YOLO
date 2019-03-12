# OpenVINO-YOLO
Inference of YoloV3 / tiny-YoloV3 on Laptop & RaspberryPi3 & NCS2
 
### Inspired and based on 

**https://github.com/PINTO0309/OpenVINO-YoloV3**

### Video 'street,mp4'

**https://www.youtube.com/watch?v=OEygtMfTbEY&t=19s**

### Edit the python script value cam_input:
```bash
cam_input = 0 #For Camera
cam_input = 'street.mp4' #change with the name of your video
```

### Clone Repository
```bash
git clone https://github.com/gplast/OpenVINO-YOLO.git
cd OpenVINO-YOLO/
```
  
### YoloV3 on Laptop CPU
```bash
cd lrmodels/YoloV3/FP32
./download_yolov3lrFP32.sh
cd ../../../
python3 openvino_yolov3_test.py -d CPU
```

### YoloV3 on Neural Compute Stick 2
```bash
cd lrmodels/YoloV3/FP16
./download_yolov3lrFP16.sh
cd ../../../
python3 openvino_yolov3_test.py -d MYRIAD
```

### Tiny-YoloV3 on Laptop CPU
```bash
cd lrmodels/tiny-YoloV3/FP32
./download_tiny-yolov3lrFP32.sh
cd ../../../
python3 openvino_tiny-yolov3_test.py -d CPU
```

### Tiny-YoloV3 on Neural Compute Stick 2
```bash
cd lrmodels/tiny-YoloV3/FP16
./download_tiny-yolov3lrFP16.sh
cd ../../../
python3 openvino_tiny-yolov3_test.py -d MYRIAD
```

### Multistick - YoloV3 on Neural Compute Stick 2
```bash
cd lrmodels/YoloV3/FP16
./download_yolov3lrFP16.sh
cd ../../../
python3 openvino_yolov3_MultiStick_test.py -numncs 1 #specify the number of NCS2
```

### Multistick - Tiny-YoloV3 on Neural Compute Stick 2
```bash
cd lrmodels/tiny-YoloV3/FP16
./download_tiny-yolov3lrFP16.sh
cd ../../../
python3 openvino_tiny-yolov3_MultiStick_test.py -numncs 1 #specify the number of NCS2
```

## Environment

- LaptopPC (Intel 8th Core i5-8250U)
- Ubuntu 18.04 x86_64
- RaspberryPi3
- Raspbian Stretch armv7l
- OpenVINO toolkit 2018 R5 (2018.5.445)
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
$ cd ~
$ curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1tlDW_kDOchWbkZbfy5WfbsW-b_GpXgr7" > /dev/null
$ CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
$ curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1tlDW_kDOchWbkZbfy5WfbsW-b_GpXgr7" -o l_openvino_toolkit_p_2018.5.445.tgz
$ tar -zxf l_openvino_toolkit_p_2018.5.445.tgz
$ rm l_openvino_toolkit_p_2018.5.445.tgz
$ cd l_openvino_toolkit_p_2018.5.445
$ sudo -E ./install_cv_sdk_dependencies.sh

## GUI version installer
$ sudo ./install_GUI.sh
 or
## CUI version installer
$ sudo ./install.sh
```
2.Configure the Model Optimizer. Execute the following command.
```bash
$ cd /opt/intel/computer_vision_sdk/install_dependencies
$ sudo -E ./install_cv_sdk_dependencies.sh
$ nano ~/.bashrc
source /opt/intel/computer_vision_sdk/bin/setupvars.sh

$ source ~/.bashrc
$ cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/install_prerequisites
$ sudo ./install_prerequisites.sh
```
3.【Optional execution】 Additional installation steps for the Intel® Movidius™ Neural Compute Stick v1 and Intel® Neural Compute Stick v2
```bash
$ sudo usermod -a -G users "$(whoami)"
$ cat <<EOF > 97-usbboot.rules
SUBSYSTEM=="usb", ATTRS{idProduct}=="2150", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idProduct}=="2485", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idProduct}=="f63b", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
EOF

$ sudo cp 97-usbboot.rules /etc/udev/rules.d/
$ sudo udevadm control --reload-rules
$ sudo udevadm trigger
$ sudo ldconfig
$ rm 97-usbboot.rules
```
4.【Optional execution】 Additional installation steps for processor graphics (GPU)
```bash
$ cd /opt/intel/computer_vision_sdk/install_dependencies/
$ sudo -E su
$ uname -r
4.15.0-42-generic #<--- display kernel version sample

### Execute only when the kernel version is older than 4.14
$ ./install_4_14_kernel.sh

$ ./install_NEO_OCL_driver.sh
$ sudo reboot
```

### 2. Work with RaspberryPi (Raspbian Stretch)
**[Note] Only the execution environment is introduced.**  
  
1.Execute the following command.
```bash
$ sudo apt update
$ sudo apt upgrade
$ curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1rBl_3kU4gsx-x2NG2I5uIhvA3fPqm8uE" > /dev/null
$ CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
$ curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1rBl_3kU4gsx-x2NG2I5uIhvA3fPqm8uE" -o l_openvino_toolkit_ie_p_2018.5.445.tgz
$ tar -zxvf l_openvino_toolkit_ie_p_2018.5.445.tgz
$ rm l_openvino_toolkit_ie_p_2018.5.445.tgz
$ sed -i "s|<INSTALLDIR>|$(pwd)/inference_engine_vpu_arm|" inference_engine_vpu_arm/bin/setupvars.sh
```
2.Execute the following command.
```bash
$ nano ~/.bashrc
### Add 1 row below
source /home/pi/inference_engine_vpu_arm/bin/setupvars.sh

$ source ~/.bashrc
### Successful if displayed as below
[setupvars.sh] OpenVINO environment initialized

$ sudo usermod -a -G users "$(whoami)"
$ sudo reboot
```
3.Update USB rule.
```bash
$ sh inference_engine_vpu_arm/install_dependencies/install_NCS_udev_rules.sh
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
