def main():
    import numpy as np
    import matplotlib
    #matplotlib.use('PS')
    import matplotlib.pyplot as plt
    import Coordinates as coords

    # First, reading in physical constants in MKS units

    m = 9.11e-31 # mass of an electron, in kg
    e_0 = 1.6e-19 # charge of an electron, in Coulombs
    pi = np.pi   # pi

    inpt = open('dynsim.in')
    for line in inpt:
        l = line.split(',')
        if l[0] != "#":
            P = int(l[0])  # rotation period of the star, in seconds
            inc = float(l[1])*(pi/180) # inclination between the rotation axis and the line of sight
            d = float(l[2])*(pi/180) # inclination angle between the rotation axis and the magnetic dipole axis
            L = float(l[3]) # Magnetic L-shell value
            B_0 = float(l[4]) # magnetic field strength at the radius of the star, in Tesla
            beta = float(l[5]) # average v/c of electrons
            distr = l[6] # string indicator of which electron distribution to use

    # the local electron cyclotron frequency at the radius of the star, for v/c = 0.1; in Hz
    f_0 = e_0 * (B_0/(2*pi*m)) * (np.sqrt(1 - beta**2))
    pos = np.array([])
    phase = np.array([i/float(P) for i in range(2*P)]) # phase, to plot the results
    I = np.array([])
    f = np.array([])
    for t in range(2*P):
        phis = np.array([i*5 * 2*pi/P for i in range(10)]) 
        phis = phis + (t%P)*((2*pi)/P) # making 10 relevant lines, offset by 5 seconds

        # Each line will be at r = L, theta = i in the rotating frame
        lines = np.array([coords.Spherical([L, inc, phis[i]]) for i in range(10)])

        for i in range(10):
            lines[i] = lines[i].rotate(d) # First the coordinates are rotated into the dipole frame
            # Then the equation for the L-shell is used to determine the 'true' distance from the center
            lines[i].q['r'] = lines[i].q['r'] * np.cos(pi/2 - lines[i].q['theta'])**2
            # calculating the frequency relative to the local electron cyclotron frequency at the radius of the star
            f_i = np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2) / (lines[i].q['r']**(3))
            f = np.append(f, min(1, f_i))
            # determining the beaming angle of the emission
            if distr == "shell":
                beam = pi/2 - np.arccos(2 * np.cos(lines[i].q['theta']) / np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2))
            if distr == "cone":
                beam = np.arccos(beta / np.sqrt(1 - f_i))

            mu = abs((lines[i].q['theta'] - beam)/(2*pi))
            # Determining circular polarization 
            if lines[i].q['theta'] < pi/2:
                CP = 1
            else:
                CP = -1

            I = np.append(I, CP * np.exp(-np.power(mu, 2.) / (2 * np.power(0.01, 2.)))/np.sqrt(2*pi*0.0001))

        pos = np.append(pos, lines)

    pos.shape = (2*P, 10)
    f.shape = (2*P, 10)
    I.shape = (2*P, 10)

    # This section is simply constructing the 2-dimensional array so it's simple to view using matplotlib
    f = f * 1000
    t = phase*P
    flux = np.zeros((1001, 2*P))
    for i in range(2*P):
        for j in range(10):
            flux[f[i, j], t[i]] = I[i, j]

            
    dims = [0, 2, 0, f_0/1e9]
    plt.imshow(flux, aspect = 'auto', origin = 'lower', extent = dims, cmap='gray')
    #$\frac{f}{f_{B_0}}$
    plt.ylabel(r"Frequency (GHz)")
    plt.xlabel(r"Phase")
    plt.title("Relative Intensity")
    plt.colorbar()
    #plt.savefig('../../Desktop/DynSim/Spectrum')
    #plt.plot(phase, I[:, 1])
    plt.show()

if __name__ == '__main__':
    main()
                  
                         

        
