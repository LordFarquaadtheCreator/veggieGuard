import subprocess, os


def classify(imageName):
    os.chdir("./darknet")
    subprocess.call(
        [
            "./darknet",
            "detect",
            "cfg/yolov3.cfg",
            "yolov3.weights",
            "data/{imageName}".format(imageName=imageName),
        ]
    )
