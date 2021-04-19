import numpy as np


def shear_matrix(data):
    """
    Computes the second moment matrix
    """
    profiles = data['GUIDE']
    shear_data = dict()

    for guide in profiles:
        Q = np.zeros((2, 2))

        profile = profiles[guide]['model']
        center = profile.shape[0] / 2
        y, x = np.indices((profile.shape))

        rx = (x - center) ** 2
        ry = (y - center) ** 2
        rxy = (x - center) * (y - center)

        denom = np.sum(profile)

        Q[0, 0] = np.sum(rx.ravel() * profile.ravel()) / denom
        Q[1, 1] = np.sum(ry.ravel() * profile.ravel()) / denom
        Q[0, 1] = np.sum(rxy.ravel() * profile.ravel()) / denom
        Q[1, 0] = Q[0, 1]

        a2, b2 = compute_a2b2(Q)
        beta = compute_beta(Q, a2, b2)
        s, e1, e2 = get_se1e2(Q)
        
        if a2 < 0.0 or b2 < 0.0:
            print(a2, b2)
            print(data['expinfo'], 'has invalid a or b')
            print(Q)

        a, b = np.sqrt(a2), np.sqrt(b2)
        g = (a - b) / (a + b)

        g1, g2 = compute_reduced(g, beta)

        shear_data[guide] = {
            "Q": Q, "a2": a2, "b2": b2, "beta": beta, 
            "s": s, "e1": e1, "e2": e2, "g1": g1, "g2": g2
        }

    return shear_data

def get_se1e2(Q):
    """
    Given the second moment matrix, compute s, e1, and e2
    """
    Q11 = Q[0, 0]
    Q22 = Q[1, 1]
    Q12 = Q[0, 1]

    e1 = (Q11 - Q22) / (Q11 + Q22 + 2 * np.sqrt(Q11 * Q22 - Q12 ** 2))
    e2 = 2 * Q12 / (Q11 + Q22 + 2 * np.sqrt(Q11 * Q22 - Q12 ** 2))

    s = np.linalg.det(Q) ** (1/4)

    return s, e1, e2

def compute_a2b2(Q):
    """
    Given the second moment matrix, compute a^2 and b^2
    """
    Q11 = Q[0, 0]
    Q22 = Q[1, 1]
    Q12 = Q[0, 1]
    a2t = 0.5 * (Q11 + Q22 + np.sqrt((Q11 - Q22) ** 2 + 4 * Q12 ** 2))
    b2t = 0.5 * (Q11 + Q22 - np.sqrt((Q11 - Q22) ** 2 + 4 * Q12 ** 2))
    a2, b2 = max(a2t, b2t), min(a2t, b2t)

    return a2, b2

def compute_beta(Q, a2, b2):
    """
    Given the second moment matrix, a^2, and b^2 
    compute the angle between the axis with length a
    and e_1
    """
    Q12 = Q[0, 1]
    beta = 0.5 * np.arcsin(2 * Q12 / (a2 - b2))

    return beta

def compute_reduced(g, beta):
    """
    Compute reduced shear components
    """
    g1 = g * np.cos(2 * beta)
    g2 = g * np.sin(2 * beta)

    return g1, g2
