cp cpp/main.cpp /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/object_detection_demo_yolov3_async

sudo cp cpp/object_detection_demo_yolov3_async.hpp /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/object_detection_demo_yolov3_async

/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/./build_samples.sh

cp $HOME/inference_engine_samples_build/intel64/Release/object_detection_demo_yolov3_async cpp/