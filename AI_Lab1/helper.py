from exceptions import WrongBoardSizeFormat, WrongStartEndPointsFormat

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