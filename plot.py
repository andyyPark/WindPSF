import numpy
import matplotlib.pyplot as plt


def plot(data, nrows=1, figsize=(12, 10)):

    guide_gmm = data["GUIDE"]

    fig, axs = plt.subplots(nrows=nrows, ncols=len(guide_gmm.keys()), figsize=figsize)
    fig.subplots_adjust(hspace=0.3, wspace=0)

    for i, guide in enumerate(guide_gmm.keys()):

        axs[i].imshow(
            guide_gmm[guide]["model"],
            origin="lower",
            extent=2
            * [
                -guide_gmm[guide]["model"].shape[0] / 2,
                guide_gmm[guide]["model"].shape[0] / 2,
            ],
            cmap=plt.cm.magma,
            interpolation="gaussian",
        )
        FWHM = plt.Circle((0, 0), 2 * guide_gmm[guide]["FWHM"], color="g", fill=False)
        axs[i].add_patch(FWHM)
        axs[i].grid(False)
        axs[i].axis("off")
        title = "{guide}\n{nstar} ".format(guide=guide, nstar=guide_gmm[guide]["nstar"])
        title += "stars" if guide_gmm[guide]["nstar"] > 1 else "star"
        axs[i].set_title(title)

        if i == 0:
            expid = "0" * (8 - len(str(data["expinfo"]["expid"]))) + str(
                data["expinfo"]["expid"]
            )
            text = "{night}/{expid}".format(night=data["expinfo"]["night"], expid=expid)
            axs[i].text(
                0.02,
                0.01,
                text,
                verticalalignment="bottom",
                horizontalalignment="left",
                transform=axs[i].transAxes,
                color="white",
                fontsize=15,
            )
            axs[i].set_zorder(1)

    plt.savefig("etc-{expid}.png".format(expid=expid))
    plt.show()
