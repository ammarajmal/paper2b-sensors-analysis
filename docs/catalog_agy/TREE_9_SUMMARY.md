# Tree 9 Summary: Vendor ROS Workspace (Camera driver nodes, acquisition GUI, and real-time detection wrappers)

## Overview and Scope
Tree 9 contains 402 total scanned files (375 catalogued, 27 identical duplicates).
Vendor ROS Workspace (Camera driver nodes, acquisition GUI, and real-time detection wrappers).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `data/MVSDK/demo/GTK_Demo/GTK_demo.cpp`
- `data/MVSDK/demo/GTK_Demo/NewPanel.cpp`
- `data/MVSDK/demo/GTK_Demo/NewPanel.h`
- `data/MVSDK/demo/GTK_Demo/config.h`
- `data/MVSDK/demo/GTK_Demo/inc/Demo.h`
- `data/MVSDK/demo/GTK_Demo/inc/callbacks.h`
- `data/MVSDK/demo/GTK_Demo/inc/interface.h`
- `data/MVSDK/demo/GTK_Demo/inc/support.h`

## Key Results and Stated Findings
- **`data/MVSDK/demo/GTK_Demo/src/Demo.cpp`**: "GtkWidget *radio_50hz=lookup_widget(main_window, "50HZ")"
- **`data/MVSDK/demo/GTK_Demo/src/Demo.cpp`**: "GtkWidget *radio_60hz=lookup_widget(main_window, "60HZ")"
- **`data/MVSDK/demo/GTK_Demo/src/callbacks.cpp`**: "radio_50hz  = GTK_WIDGET(gtk_builder_get_object(Demo_builder, "50HZ"))"
- **`data/MVSDK/demo/GTK_Demo/src/callbacks.cpp`**: "radio_60hz  = GTK_WIDGET(gtk_builder_get_object(Demo_builder, "60HZ"))"
- **`data/MVSDK/demo/GTK_Demo/src/interface.cpp`**: "radio_50hz  = GTK_WIDGET(gtk_builder_get_object(Demo_builder, "50HZ"))"
- **`data/MVSDK/demo/GTK_Demo/src/interface.cpp`**: "radio_60hz  = GTK_WIDGET(gtk_builder_get_object(Demo_builder, "60HZ"))"
- **`data/MVSDK/demo/OpenCv/main.cpp`**: "// Try to capture a frame within a 1000 ms timeout"
- **`data/MVSDK/demo/QT5_Demo/mainwindow.cpp`**: "//设置自动曝光时消频闪的频率。0:50HZ , 1:60HZ"
- **`data/MVSDK/demo/QT5_Demo/mainwindow.cpp`**: "//设置自动曝光时消频闪的频率。0: 50hz  1:60hz"

## Planned or Missing Elements
- `data/MVSDK/include/CameraApi.h`: 对于CMOS传感器，其曝光的单位是按照行来计算的，因此，曝光时间并不能在微秒级别连续可调。而是会按照整行来取舍。在调用本函数设定曝光时间后，建议再调用@link
- `data/MVSDK/include/CameraApi.h`: For CMOS sensors, the unit of exposure is calculated in rows, so the exposure ti
- `data/MVSDK/include/CameraApi.h`: 已废弃，使用CameraSetIOStateEx，它对所有型号相机的输出状态值统一为1高 0低
- `data/MVSDK/include/CameraDefine.h`: 某些型号的相机不支持此功能，对于不支持此功能的相机这个标志相当于@link #CAMERA_GET_IMAGE_PRIORITY_OLDEST @endlink
- `data/MVSDK/include/CameraDefine.h`: Some models do not support this feature
- `data/MVSDK/include/CameraDefine.h`: USB相机uParam取值：

## Duplicate Files Across Trees
- `data/MVSDK/demo/QT_Demo/capturethread.cpp`: identical to Tree 9 (`data/MVSDK/demo/QT5_Demo/capturethread.cpp`)
- `data/MVSDK/demo/QT_Demo/capturethread.h`: identical to Tree 9 (`data/MVSDK/demo/QT5_Demo/capturethread.h`)
- `data/MVSDK/demo/multicamera_demo/inc/support.h`: identical to Tree 9 (`data/MVSDK/demo/GTK_Demo/inc/support.h`)
- `data/MVSDK/demo/multicamera_demo/src/support.cpp`: identical to Tree 9 (`data/MVSDK/demo/GTK_Demo/src/support.cpp`)
- `data/cam_try/checkingConnectedCameras.py`: identical to Tree 9 (`data/cam_try/checking.py`)
- `data/cam_try/cv_grab2.py`: identical to Tree 9 (`data/MVSDK/demo/python_demo/cv_grab2.py`)
- `data/cam_try/cv_grab_callback.py`: identical to Tree 9 (`data/MVSDK/demo/python_demo/cv_grab_callback.py`)
- `data/cam_try/grab.py`: identical to Tree 9 (`data/MVSDK/demo/python_demo/grab.py`)
