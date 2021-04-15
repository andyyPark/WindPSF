from util import get_json, read_json
from plot import plot
from telemetry import get_telemetry
from shear import shear_matrix

if __name__ == "__main__":

    path = "/global/cfs/cdirs/desi/spectro/data"
    etc_files = get_json(path)
    etc_files = [etc_files[1]]

    for etc_file in etc_files:
        data = read_json(etc_file)
        shear_data = shear_matrix(data)

        plot(data, shear_data)

    # print(get_telemetry())
