# FaceCam Extractor
FaceCam Extractor is a simple and intuitive application designed to help users easily extract a specific face camera from a video file. 
The application uses advanced facial recognition technology to isolate the face in the camera view and crops the video accordingly. 
It's an essential tool for video editors, content creators, and anyone who needs to extract a specific face camera from a video file quickly and easily.

How to use it:
```python
path = "test\\folder0"
asd = FaceCamExtractor(path)
asd.extract_all()
```
It will resolve in extracting from all videos in path, camera cut and saving it with screenshot.

Here is some result:
Original screenshot from video:
![Screenshot1](./examples/23_21_05_whole.png.png?raw=true "View from clip")
Cut camera view from video:
![Screenshot1](./examples/23_21_05_src_cut.png.png?raw=true "View from clip")

You can check more results in the 'examples' folder!



