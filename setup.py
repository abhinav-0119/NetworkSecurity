from setuptools import find_packages, setup

def requirements(file_path):
    try:
        requirements=[]
        with open (file_path) as file_obj:
            require=file_obj.readlines()
            requirements=[req.replace("\n","") for req in require]
            if "-e ." in requirements:
                requirements.remove("-e .")
            return requirements
    except FileNotFoundError:
        print("requirements.txt not found")
        return []

setup(
    name="NETWORK SECURITY PROJECT",
    version="0.0.1",
    author="ABHINAV ANAND",
    author_email="anandabhinav0119@gmail.com",
    packages=find_packages(),
    install_requires=requirements("requirements.txt")
)
