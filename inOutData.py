import json
import os

def readFile(filePath):
    print(filePath)
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            print(data)

            return data

    except FileNotFoundError:
        print("File Not Found!!")
    
    except json.JSONDecodeError:
        print("Invalid JSON format!!")

def readData():
    folderPath = "data"

    dataList = []

    for file in os.listdir(folderPath):
        filePath = os.path.join(folderPath, file)
        if (os.path.isfile(filePath)):
            # print(f"File: {file}")
            dataList.append(readFile(filePath))

