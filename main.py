from util import get_json, read_json, read_fits
from plot import plot
from telemetry import get_telemetry
from shear import shear_matrix

if __name__ == "__main__":

    # path = "/global/cfs/cdirs/desi/spectro/ETC/20201214/00067745/gfaetc_00067745.fits"
    # data = read_fits(path)
    # shear_data = shear_matrix(data)
    # plot(data, shear_data)
    path = "/global/cfs/cdirs/desi/spectro/data"
    etc_files = get_json(path)

    for etc_file in etc_files:
        data = read_json(etc_file)
        shear_data = shear_matrix(data)

        plot(data, shear_data)

    # print(get_telemetry())
