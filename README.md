# Facial Recognition Attendance System

## Overview
This project is a **Facial Recognition Attendance System** designed to automate the attendance management process by utilizing facial recognition technology. It captures images, recognizes faces, and logs attendance seamlessly, ensuring efficiency and accuracy.

## Features
- **Face Detection and Recognition**: Detects faces in real-time using a webcam.
- **Attendance Logging**: Records attendance with timestamps.
- **Database Integration**: Stores and retrieves attendance data for future reference.
- **User-Friendly Interface**: Easy to operate with clear prompts.

## Prerequisites
Ensure you have the following installed:

- **Python 3.6 or above**
- Libraries:
  - `opencv-python`
  - `numpy`
  - `pandas`
  - `dlib`
  - `face_recognition`

To install the required libraries, use:
```bash
pip install -r requirements.txt
```

## Getting Started
### Clone the Repository
```bash
git clone https://github.com/Yash-Gupta5911/FacialRecognition_Attendance.git
cd FacialRecognition_Attendance
```

### Run the Application
1. Add the images of individuals to the `dataset` folder.
   - Each image should be labeled with the person's name (e.g., `John_Doe.jpg`).

2. Train the facial recognition model:
   ```bash
   python encode_faces.py
   ```

3. Start the attendance system:
   ```bash
   python recognize_faces.py
   ```

4. Attendance will be logged in the `attendance.csv` file.

## Project Structure
```
FacialRecognition_Attendance
│
├── dataset/              # Folder for storing face images
├── encode_faces.py       # Script to encode face images
├── recognize_faces.py    # Script to recognize faces and log attendance
├── attendance.csv        # CSV file for storing attendance logs
├── requirements.txt      # Dependencies for the project
└── README.md             # Project documentation
```

## Usage
- Place new face images in the `dataset` folder.
- Run `encode_faces.py` to update encodings.
- Launch `recognize_faces.py` to start the recognition process.

## Limitations
- Lighting conditions can affect accuracy.
- Limited to frontal face images for better recognition.

## Contributions
Contributions are welcome! Feel free to fork the repository and create pull requests for enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **OpenCV** for image processing.
- **dlib** and **face_recognition** for face detection and recognition.

