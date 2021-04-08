import json
import numpy as np
import desietc.gmm


def read_json(path):

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

    for guide in json_data["acquisition"].keys():
        if json_data["acquisition"][guide]["nstar"] > 0:
            gmm_params = np.array(json_data["acquisition"][guide]["gmm"])
            data["GUIDE"][guide] = {
                "model": GMM.predict(gmm_params),
                "FWHM": json_data["acquisition"][guide]["fwhm"],
                "nstar": json_data["acquisition"][guide]["nstar"],
            }

    return data
