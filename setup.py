# Setup build file for compile .py to .exe
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["mediapipe", "cv2"],
    "include_files": ["functions/", "ressources/", "menu_fct.py"],
}

setup(
    name = "Virtualis",
    version = "0.1",
    description = "Application allowing you to use a virtual mouse with your finger using AI recognition.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("menu.py", base="Win32GUI", icon="./ressources/virtual_mouse_logo.ico")]
)

# Run "python setup.py build" to have the .exe for the app