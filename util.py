import os
import csv
import json
import numpy as np

import fitsio
import desietc.gmm


def read_fits(path):
    """
    Read fits file and return gmm parameters
    """
    fits_info = fitsio.read_header(path)
    gfa_names = [
        "GUIDE0", "GUIDE2", "GUIDE3",
        "GUIDE5", "GUIDE7", "GUIDE8"]

    data = dict()
    data["expinfo"] = {"night": fits_info["NIGHT"],
                       "expid": fits_info["EXPID"],
                       "MJD": fits_info["MJD-OBS"]}
    data["GUIDE"] = dict()

    psf_pixels = 25
    psf_grid = np.arange(psf_pixels + 1) - psf_pixels / 2
    GMM = desietc.gmm.GMMFit(psf_grid, psf_grid)

    with fitsio.FITS(path, mode="r") as hdus:
        for gfa in gfa_names:
            if gfa not in hdus: continue

            gmm_params = fitsio.read(path, ext=gfa+"M")
            psf = GMM.predict(gmm_params)
            psf[psf < 0.0] = 0.0
            data["GUIDE"][gfa] = {"model": psf}

    return data


def get_json(path):
    """
    Get etc-json files from path
    """
    files = [
        os.path.join(path, file)
        for file in os.listdir(path)
        if file != "README.html" and file >= "20210319"
    ]  # Make it robust using regex

    etc_files = []
    for file in files:
        for expid in os.listdir(file):
            etc = f"etc-{expid}.json"
            if etc in os.listdir(os.path.join(file, expid)):
                etc_files.append(os.path.join(file, expid, etc))

    return etc_files


def read_json(path):
    """
    Read one etc-json file from path
    """

    with open(path) as f:
        json_data = json.load(f)


    # Skip expid that has 0 gmm
    empty_gmm = [len(json_data["acquisition"][camera].get("gmm", []))
                   for camera in json_data["acquisition"].keys()]

    if sum(empty_gmm) == 0 or "acq_mjd" not in json_data["expinfo"]:
        return None

    data = dict()
    data["expinfo"] = {
        "expid": json_data["expinfo"]["expid"],
        "night": json_data["expinfo"]["night"],
        "mjd": json_data["expinfo"]["acq_mjd"]
    }
    data["GUIDE"] = dict()

    psf_pixels = 25
    psf_grid = np.arange(psf_pixels + 1) - psf_pixels / 2
    GMM = desietc.gmm.GMMFit(psf_grid, psf_grid)

    nll_threshold = 100

    for guide in json_data["acquisition"].keys():
        # Check if the GUIDE has a model
        if json_data["acquisition"][guide]["nstar"] > 0:

            # Check bad psf models
            if json_data["acquisition"][guide]["nll"] > nll_threshold:
                continue

            gmm_params = np.array(json_data["acquisition"][guide]["gmm"])
            if len(gmm_params) == 0:
                continue

            psf = GMM.predict(gmm_params)
            psf[psf < 0.0] = 0.0

            data["GUIDE"][guide] = {
                "model": psf,
                "FWHM": json_data["acquisition"][guide]["fwhm"],
                "nstar": json_data["acquisition"][guide]["nstar"],
            }

    return data


def write_csv(night, expid, mjd, a, b, beta, output='./shear.csv'):
    """
    Write shear data
    """
    if len(a) != len(b):
        raise ValueError("len(a) != len(b)")

    if len(b) != len(beta):
        raise ValueError("len(b) != len(beta)")

    gfa_names = [
        "GUIDE0", "GUIDE2", "GUIDE3",
        "GUIDE5", "GUIDE7", "GUIDE8"
    ]
    fieldnames = ["NIGHT", "EXPID", "MJD"]

    for camera in gfa_names:
        fieldnames.extend(["A"+camera[-1], "B"+camera[-1], "BETA"+camera[-1]])

    if not os.path.exists(output):
        with open(output, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(output, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        row = {"NIGHT": night, "EXPID": expid, "MJD": mjd}

        for camera in gfa_names:
            row["A"+camera[-1]] = a.get(camera, 0)
            row["B"+camera[-1]] = b.get(camera, 0)
            row["BETA"+camera[-1]] = np.rad2deg(beta.get(camera, 0))

        writer.writerow(row)





