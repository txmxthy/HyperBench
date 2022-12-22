import csv
import os
import plotly
from utils import readFilePairs
from jspGA import genetic

if __name__ == '__main__':
    target = None
    files = (os.listdir(os.getcwd() + "/cases"))
    print(files)

    population_size = int(input('Please input the size of population (default: 30): ') or 30)
    mutation_rate = float(input('Please input the size of Mutation Rate (default 0.2): ') or 0.2)
    iterations = int(input('Please input number of iteration (default 2000): ') or 2000)
    maxTime = int(input('Please input the maximum time in seconds (default 30): ') or 30)
    scores = {}
    for file in files:
        times, machines, n = readFilePairs("cases/" + file)
        cost = genetic(times, machines, n, population_size, iterations, mutation_rate, target, maxTime=maxTime)
        scores[file] = cost
    print(scores)
    csv_columns = files
    csv_file = "scores.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(scores)
    except IOError:
        print("I/O error")