from util import read_json
from plot import plot

if __name__ == "__main__":
    path = "etc-00083543.json"

    guide_gmm = read_json(path)
    plot(guide_gmm)
