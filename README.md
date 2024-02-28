# MVTrack
Object tracking with motion vector in video bitstream.

## 0. Environment

```OS ubuntu~18.04
   python 3.7
   ffmpeg version 4.4.1 Copyright (c) 2000-2021 the FFmpeg developers
   built with gcc 7 (Ubuntu 7.5.0-3ubuntu1~18.04)
   configuration: --enable-shared --disable-static

```
install imutils and cv2
## 1. Install Instructions

Before running the code, make sure ```ffmpeg-4.4.1``` is installed, if not, do:

1.By https://git.ffmpeg.org/ffmpeg.git, get ffmpeg-4.4.1 version (or 4.4.x)

2.Do this in turn to install ffmpeg

   ```
   cd ffmpeg-4.4.1
   ./configure --enable-shared --disable-static
   make -j8
   make install
   ```   


## 2. Run our code

Now, with the repo folder ```h264_cabac. C``` will ```libavcodec``` folder of ```h264_cabac. C``` :

```cd ffmpeg-4.4.1```

Compile：

```
make
make install
```

Execute：

```
    ffmpeg -c:v h264 -i input.mp4 -f null - 
```

Subsequently, in the execution of the instruction folder to obtain the ```mv.txt``` file to save the motion vector information of all frames;

## 3. Detection

Detect input.mp4 using any object detection model, the test results are saved in the ```results`` CSV file.

## 4. MV-based shift

Get ` ` ` mv. TXT ` ` ` file, and get to the test results ```results``` CSV file, will redefine the inspection results for ```dds_utils. Py``` 在 ```Region``` structure, Run the process_results.py file to reuse the results and save the final results as a final_results CSV file.

```
class Region:
    def __init__(self, fid, x, y, w, h, conf, label, resolution,
                 origin="generic"):
        self.fid = int(fid)
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.conf = float(conf)
        self.label = label
        self.resolution = float(resolution)
        self.origin = origin
```

## 5. Visualization
The original result ```results``` and the reused ```final_results``` as ```nomv_filename``` and 和 ```filename``` variables of ```visual.py``` file, after execution, a visual video file can be obtained. For example, ```demo.mp4``` in the repo.
In the following picture, the green box is the detection result of one frame per second by business process, and the blue box is the MV-based tracking result:
![an image is a 3d matrix RGB](/0000000125.png "An image is a 3D matrix")
![an image is a 3d matrix RGB](/0000000151.png "An image is a 3D matrix")
![an image is a 3d matrix RGB](/0000000155.png "An image is a 3D matrix")
![an image is a 3d matrix RGB](/0000000177.png "An image is a 3D matrix")
