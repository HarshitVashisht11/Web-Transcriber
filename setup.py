from setuptools import find_packages, setup
from setuptools.command.install import install
import os
import sys
import subprocess

class CustomInstallCommand(install):
    def run(self):
        self.create_venv()
        self.install_in_venv()
        install.run(self)

    def create_venv(self):
        venv_path = os.path.join(os.getcwd(), 'venv')
        if not os.path.exists(venv_path):
            print("Creating a virtual environment (venv)...")
            subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
            print("Virtual environment created.")

    def install_in_venv(self):
        venv_python = os.path.join(os.getcwd(), 'venv', 'bin', 'python')
        subprocess.run([venv_python, '-m', 'pip', 'install', 'Flask==2.9.6', 'whisper==1.1.10', 'torch==2.1.1'], check=True)

setup(
    name="Transcriber",
    py_modules=["main"],
    version="1.0.0",
    description="Your description here",
    cmdclass={'install': CustomInstallCommand},
    entry_points={
        'console_scripts': [
            'transcriber=main:run_app',
        ],
    },
)
