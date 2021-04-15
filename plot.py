import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches


def plot(data, shear_data, nrows=1, figsize=(12, 10)):

    guide_gmm = data["GUIDE"]

    if len(guide_gmm.keys()) == 0:
        print(data["expinfo"], "has etc json but no model")
        return

    if len(guide_gmm.keys()) == 1:
        print(data["expinfo"])

    model_sum = {guide: guide_gmm[guide]["model"].sum() for guide in guide_gmm.keys()}
    model_max = np.median([guide_gmm[guide]["model"].max() / model_sum[guide] for guide in guide_gmm.keys()])
    vmin, vmax = -0.1 * model_max, 1.0 * model_max
    norm = np.max(np.array([guide_gmm[guide]["model"].sum() for guide in guide_gmm.keys()]))

    fig, axs = plt.subplots(nrows=nrows, ncols=len(guide_gmm.keys()), figsize=figsize)
    axs = np.array(axs)
    axs = axs.reshape(-1)

    fig.subplots_adjust(hspace=0.3, wspace=0)

    fiber_diam_um = 107
    pixel_size_um = 15
    radius = 0.5 * fiber_diam_um / pixel_size_um

    for i, guide in enumerate(guide_gmm.keys()):

        axs[i].imshow(
            guide_gmm[guide]["model"] / norm,
            vmin=vmin, vmax=vmax,
            origin="lower",
            extent=2
            * [
                -guide_gmm[guide]["model"].shape[0] / 2,
                guide_gmm[guide]["model"].shape[0] / 2,
            ],
            cmap=plt.cm.magma,
            interpolation="bicubic",
        )
        fiber = plt.Circle((0, 0), radius, color="g", fill=False, alpha=0.7)
        axs[i].add_patch(fiber)
        axs[i].grid(False)
        axs[i].axis("off")
        title = "{guide}\n{nstar} ".format(guide=guide, nstar=guide_gmm[guide]["nstar"])
        title += "stars" if guide_gmm[guide]["nstar"] > 1 else "star"
        axs[i].set_title(title)

        s = shear_data[guide]['s']
        e1 = shear_data[guide]['e1']
        e2 = shear_data[guide]['e2']

        if data['expinfo']['night'] == '20210326' and data['expinfo']['expid'] == 82357:
            print(s, e1, e2) 

        draw_ellipse_se1e2(axs[i], 0, 0, s, e1, e2, data['expinfo'])

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
                color="w",
                fontsize=15,
            )
            axs[i].set_zorder(1)


    path = "./Plots/{night}/etc-{expid}.png".format(
        night=data["expinfo"]["night"], expid=expid
    )

    if not os.path.isdir("./Plots/{night}".format(night=data["expinfo"]["night"])):
        os.makedirs("./Plots/{night}".format(night=data["expinfo"]["night"]))

    plt.savefig(path)
    plt.close()

def draw_ellipse_se1e2(ax, x0, y0, s, g1, g2, info, nsigmas=1, **ellipseopts):
    g = np.sqrt(g1 ** 2 + g2 ** 2)
    if g > 1:
        print(info, 'failed')
        print(g1 ** 2 + g2 ** 2)
        raise ValueError('g1 ** 2 + g2 ** 2 > 1')
    center = np.array([x0, y0])
    angle = np.rad2deg(0.5 * np.arctan2(g2, g1))
    ratio = np.sqrt((1 + g) / (1 - g))
    width = 2 * s * ratio * nsigmas
    height  = 2 * s / ratio * nsigmas
    kwargs = dict(color='w', ls='-', lw=2, alpha=0.7, fill=False)
    kwargs.update(ellipseopts)
    ellipse = matplotlib.patches.Ellipse(center, width, height, angle, **kwargs)
    ax.add_artist(ellipse)
