from util import get_json, read_json
from plot import plot
from telemetry import get_telemetry

if __name__ == "__main__":

    # path = "/global/cfs/cdirs/desi/spectro/data"
    # etc_files = get_json(path)

    # for etc_file in etc_files:
    #     data = read_json(etc_file)
    #     plot(data)

    print(get_telemetry())
