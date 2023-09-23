# veggieGuard
Computer vision application that indentifies new items in a fridge and notifies users when a perishable is about to expire

# Download YOLO (via [Darknet](https://pjreddie.com/darknet/install/#cuda))
- goto [darknet.yolo](https://pjreddie.com/darknet/yolo/) and download yolo
```
git clone https://github.com/pjreddie/darknet
cd darknet
make
```
- `wget https://pjreddie.com/media/files/yolov3.weights` 
    - or [physically download it](https://pjreddie.com/media/files/yolov3.weights)
- this will download test data, which can be tested via the `darknet/data` folder
- to run a test of it (from the darknet folder) you can run `./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg`

# [Download OpenCV](https://efcomputer.net.au/blog/4-steps-to-install-darknet-with-cuda-and-opencv-for-realtime-object-detection/) 

- `cd $home`
- `mkdir OpenCV`
- `cd OpenCV`
- `git clone https://github.com/opencv/opencv.git`
- `git clone https://github.com/opencv/opencv_contrib.git`
- `mkdir build_opencv`
- `cd build_opencv`
- `cmake -DCMAKE_BUILD_TYPE=Release -D OPENCV_GENERATE_PKGCONFIG=ON -DBUILD_EXAMPLES=ON -D CMAKE_INSTALL_PREFIX=/usr/local ../opencv`
    - you will need `cmake` downloaded for this
    - `brew install cmake`
- `make -j7`
- `sudo make install`
- `pkg-config --cflags opencv4`

## Try to compile darknet again
if you encounter the error where it still can’t find opencv.pc, you might want to check that you have the opencv4.pc in the following location
`ls /usr/local/lib/pkgconfig/opencv4.pc`
- if you do then just copy opencv4 to opencv by using the following command
`sudo cp /usr/local/lib/pkgconfig/opencv4.pc /usr/local/lib/pkgconfig/opencv.pc`

Now try to compile darknet again but first you will need to change the option `opencv=1` in the Makefile. When you try to run the make command you might get the following error if you are using opencv version 4.
`error: #error "OpenCV 4.x+ requires enabled C++11 support"`

To solve this you will need to edit the Makefile by adding the `-std=c++11` in the following line:
`CPP=g++ -std=c++11`

### any errors that come up can be googled! (That's how I fixed it!)

# Download CUDA

