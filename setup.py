from cx_Freeze import setup, Executable

files_to_include = ["main.py", "recognitionclass.py", "face_recognition/__init__.py", "face_recognition/api.py", "face_recognition/face_detection_cli.py", "face_recognition/face_recognition_cli.py"]

executables = [Executable("main.py")]

setup(
    name="FaceRecognition",
    version=1.0,
    description="Face Recognition by Polat",
    options={"build_exe": {"include_files": [(file, file) for file in files_to_include]}},
    executables=executables
)

