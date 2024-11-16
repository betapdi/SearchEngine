import json
import os
from classes import Document, Database

def inputStopWords(filePath):
    data = set()
    with open(filePath, "r", encoding='utf-8') as file:
        for line in file: 
            data.add(line.rstrip('\n'))
            
    return data

def readFile(filePath):
    # print(filePath)
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            # print(data)

            return Document(data)

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
    
    return Database(dataList)

