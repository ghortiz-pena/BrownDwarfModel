def header(f_name):
    from numpy import pi
    f = open(f_name)
    line = f.readline()
    l = line.split()
    while l[0] == "#":
        line = f.readline()
        l = line.split()
    n = int(l[0])
    distr = l[1]
    line = f.readline()
    l = line.split()
    P = int(l[0])
    B = float(l[1])
    beta = float(l[2])
    inc = float(l[3])*pi/180
    Ls = []
    ds = []
    lngs = []
    for i in range(n):
        line = f.readline()
        l = line.split()
        Ls.append(float(l[0]))
        ds.append(float(l[1])*pi/180)
        lngs.append(float(l[2])*pi/180)

    return n, distr, P, B, beta, inc, Ls, ds, lngs

def main():
    import numpy as np
    import matplotlib
    matplotlib.use('PS')
    import matplotlib.pyplot as plt
    import Coordinates as coords

    # First, reading in physical constants in MKS units

    m = 9.11e-31 # mass of an electron, in kg
    e_0 = 1.6e-19 # charge of an electron, in Coulombs
    pi = np.pi   # pi
    
    n, distr, P, B_0, beta, inc, L, d, lng = header('dynsim.in')

    # the local electron cyclotron frequency at the radius of the star, for v/c = 0.1; in Hz
    f_0 = e_0 * (B_0/(2*pi*m))    
    pos = np.array([])
    phase = np.array([i/float(P) for i in range(2*P)]) # phase, to plot the results
    I = np.array([])
    f = np.array([])
    for t in range(2*P):
        phis = np.array([(i*5) * 2*pi/P for i in range(5*n)]) 
        # making 5 relevant lines per magnetic loop, offset by 5 seconds
        for i in range(n):
            phis[i*5 : (i+1)*5] = phis[i*5 : (i+1)*5] + (t%P)*((2*pi)/P) + lng[i]

        # Each line will be at r = L, theta = i in the rotating frame
        lines = np.array([coords.Spherical([L[i/5], inc, phis[i]]) for i in range(5*n)])

        for i in range(5*n):
            lines[i] = lines[i].rotate(d[i/5]) # First the coordinates are rotated into the dipole frame
            # Then the equation for the L-shell is used to determine the 'true' distance from the center
            lines[i].q['r'] = lines[i].q['r'] * np.cos(pi/2 - lines[i].q['theta'])**2
            # calculating the frequency relative to the local electron cyclotron frequency at the radius of the star
            
            
            # determining the beaming angle of the emission
            if distr == "shell":
                beam = pi/2 - np.arccos(2 * np.cos(lines[i].q['theta']) / np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2))
                f_i = min(1, np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2) / (lines[i].q['r']**(3)) * np.sqrt(1 - beta**2))
            if distr == "cone":
                f_i = min(1, np.sqrt(1 + 3 * np.cos(lines[i].q['theta'])**2) / (lines[i].q['r']**(3)) / np.sqrt(1 - beta**2))
                beam = np.arccos(beta / np.sqrt(1 - f_i))

            f = np.append(f, f_i)
            mu = abs((lines[i].q['theta'] - beam)/(2*pi))
            # Determining circular polarization 
            if lines[i].q['theta'] < pi/2:
                CP = 1
            else:
                CP = -1

            I = np.append(I, CP * np.exp(-np.power(mu, 2.) / (2 * np.power(0.01, 2.)))/np.sqrt(2*pi*0.0001))

        pos = np.append(pos, lines)

    pos.shape = (2*P, 5*n)
    f.shape = (2*P, 5*n)
    I.shape = (2*P, 5*n)

    # This section is simply constructing the 2-dimensional array so it's simple to view using matplotlib
    f = f * 1000
    t = phase*P
    flux = np.zeros((1001, 2*P))
    for i in range(2*P):
        for j in range(5*n):
            flux[f[i, j], t[i]] = I[i, j]

    print np.amax(f) / 1000 * f_0 / 1e9       
    dims = [0, 2, 0, f_0 / 1e9]
    plt.imshow(flux, aspect = 'auto', origin = 'lower', extent = dims, cmap='gray')
    #
    plt.ylabel(r"Frequency (GHz)")
    plt.xlabel(r"Phase")
    plt.title("Relative Intensity")
    plt.colorbar()
    plt.savefig('../../Desktop/DynSim/Spectrum')
    #plt.plot(phase, I[:, 1])
    plt.show()

if __name__ == '__main__':
    main()
                  
                         

        
