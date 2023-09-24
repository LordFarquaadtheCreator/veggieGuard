import subprocess, os, re
from flask import Flask, request, jsonify


def run_darknet(image_path):
    # Specify the path to the darknet executable and your YOLO configuration file
    os.chdir("/Users/fahadfaruqi/Desktop/veggieGuard/darknet")
    darknet_cmd = "./darknet detect cfg/yolov3.cfg yolov3.weights"

    # Call darknet using subprocess and capture its output
    process = subprocess.Popen(
        darknet_cmd.split() + [image_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for the process to finish and get the output
    stdout, stderr = process.communicate()

    # Check if there were any errors
    if process.returncode != 0:
        print("Error executing darknet:")
        print(stderr.decode("utf-8"))
        return None

    # Parse the output into a list of dictionaries
    output_lines = stdout.decode("utf-8").split("\n")
    output_lines.pop(0)

    return output_lines


def parse_list_entry(entry):
    # Split the entry by ': ' to separate item and percentage
    parts = entry.split(": ")

    # Check if there are two parts (item and percentage)
    if len(parts) == 2:
        item = parts[0].strip()
        percentage_str = parts[1].strip("%")

        # Convert the percentage string to a float
        try:
            percentage = float(percentage_str)
        except ValueError:
            print(f"Error: Unable to convert '{percentage_str}' to a float.")
            return None

        # Create a dictionary and store item and percentage
        result = {"item": item, "confidence": percentage}
        return result
    else:
        print(f"Error: Invalid entry format: {entry}")
        return None


app = Flask(__name__)
import json


@app.route("/analyze", methods=["GET"])
def analyze(image_path="data/food.png"):
    results = run_darknet(image_path)

    if results is not None:
        # Store the results in a hashmap
        object_map = []
        for result in results:
            object_map.append(parse_list_entry(result))

        # Print or use the list as needed
        return json.dumps(object_map)


analyze()
