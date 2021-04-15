import os
import json
import numpy as np
import desietc.gmm


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
            data["GUIDE"][guide] = {
                "model": GMM.predict(gmm_params),
                "FWHM": json_data["acquisition"][guide]["fwhm"],
                "nstar": json_data["acquisition"][guide]["nstar"],
            }



    return data

