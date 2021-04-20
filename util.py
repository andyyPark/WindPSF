import os
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
            data["GUIDE"][gfa] = {"model": GMM.predict(gmm_params)}

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

    data = dict()
    data["expinfo"] = {
        "expid": json_data["expinfo"]["expid"],
        "night": json_data["expinfo"]["night"],
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

