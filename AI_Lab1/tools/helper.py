from tools.exceptions import WrongBoardSizeFormat, WrongStartEndPointsFormat
import os
import shutil
import matplotlib.pyplot as plt

def load_data(file_name):
        filename = "test_files\\" + file_name
        file = open(filename)
        
        i=0
        width = 0
        height = 0
        points = []

        for line in file:
            data = line.split(";")
            if i == 0:
                if len(data) == 2:
                    width, height = int(data[0]), int(data[1])
                else:
                    msg = "Wrong board size, expected 2 params, got:" + len(data)
                    raise WrongBoardSizeFormat(msg)
            else:
                if len(data) != 4:
                    msg = "Wrong number of points, expected 4, got:" + len(data)
                    raise WrongStartEndPointsFormat(msg)
                else:
                    start_point = [int(data[0]), int(data[1])]
                    end_point = [int(data[2]), int(data[3])]
                    pair = [start_point, end_point]
                    points.append(pair)
            i += 1

        return width, height, points


def prepare_folder_for_imgs():
    if os.path.isdir('best_individuals'):
        shutil.rmtree('best_individuals/')
    try:
        os.mkdir('best_individuals')
    except OSError:
        print("Caanot create directory for best individuals!")


def make_chart(best, worst, avg):
    plt.plot(best, label='best fitness')
    plt.plot(worst, label='worst fitness')
    plt.plot(avg, label='average fitness')
    plt.xlabel('Generation number')
    plt.ylabel('Fitness value')
    plt.legend()
    plt.show()