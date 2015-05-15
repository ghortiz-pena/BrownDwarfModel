import numpy as np
import matplotlib
#matplotlib.use('PS')
import matplotlib.pyplot as plt
import Coordinates as coords

def main():

    # First, physical constants in MKS units
    L = 2 # Specifying the magnetic L-shell
    m = 9.11e-31 # mass of an electron, in kg
    e_0 = 1.6e-19 # charge of an electron, in Coulombs
    P = 7200 # rotation period of the star, in seconds
    B_0 = 0.256 # magnetic field strength at the radius of the star, in Tesla
    pi = np.pi # pi
    inc = pi/3 # inclination between the magnetic dipole axis and the line of sight
    d = pi/3 # inclination angle between the rotation axis and the magnetic dipole axis    
    # the local electron cyclotron frequency at the radius of the star, for v/c = 0.1 in Hz
    f_0 = e_0 * (B_0/(2*pi*m)) * (np.sqrt(1 - 0.1**2))

    pos = np.array([])
    phase = np.array([(i%P)/float(P) for i in range(P)])
    I = np.array([])
    f = np.array([])
    for t in range(P):
        phis = np.array([i*5 * 2*pi/P for i in range(10)]) 
        phis = phis + (t%P)*((2*pi)/P) # making 10 relevant lines, offset by 5 seconds
        
        lines = np.array([coords.Spherical([L, pi/2, phis[i]]) for i in range(10)])

        for i in range(10):
            lines[i] = lines[i].rotate(d)
            lines[i].q['r'] = lines[i].q['r'] * np.cos(pi/2 - lines[i].q['theta'])**2
            lines[i] = lines[i].rotate(inc)
            f = np.append(f, min(1, np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2) / (lines[i].q['r']**(3))))
            perp = pi/2 - np.arccos(2 * np.cos(lines[i].q['theta']) / np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2))
            mu = (lines[i].q['theta'] - perp)/(2*pi)
            I = np.append(I, np.exp(-np.power(mu, 2.) / (2 * np.power(0.01, 2.)))/np.sqrt(2*pi*0.0001))

        pos = np.append(pos, lines)

    pos.shape = (P, 10)
    f.shape = (P, 10)
    I.shape = (P, 10)

    f = f * 1000
    t = phase*P
    flux = np.zeros((1001, P))
    for i in range(P):
        for j in range(10):
            flux[f[i, j], t[i]] = I[i, j]

            
    dims = [0, 1, 0, 1]
    plt.imshow(flux, aspect = 'auto', origin = 'lower', extent = dims, cmap='gray')
    plt.ylabel(r"$\frac{f}{f_{B_0}}$")
    plt.xlabel(r"Phase")
    plt.title("Relative Intensity")
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    main()
                  
                         

        
