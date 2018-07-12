import numpy as np
import matplotlib.pyplot as plt

#finds point in wavelength window
def win_int (wv, fl, error,eff_wv):
    c = 3E18 
    h = 6.62607004e-34
    nu = c / wv
    fnu = (wv**2 / c) * fl
    #integrate top
    top = fnu /(h*nu)
    int_top = np.trapz(top,nu)
    #integrate bottom
    bottom = 1 / (h*nu)
    int_bottom = np.trapz(bottom, nu)
    #divide the two
    phot = int_top/int_bottom
    return phot * (c / eff_wv**2)


#defines continuum and calculates EW
def eqwdth(win_b, win_r, win_line, fl, wv, error):
    idb = []
    idl = []
    idr = []
    
    #x values
    blue_avg = np.mean(win_b)
    red_avg = np.mean(win_r)
    
    for i in range(len(wv)):
        if win_b[0] <= wv[i] <= win_b[1]:
            idb.append(i)
        if win_r[0] <= wv[i] <= win_r[1]:
            idr.append(i)
        if win_line[0] <= wv[i] <= win_line[1]:
            idl.append(i)

    #y values         
    blue_pt = win_int(wv[idb], fl[idb], error[idb],blue_avg)
    red_pt = win_int(wv[idr], fl[idr], error[idr],red_avg)
    
    cont = ((red_pt - blue_pt)/(red_avg - blue_avg))*(wv[idl] - blue_avg) + blue_pt
    
    integrand = 1 - (fl[idl]/cont)
    ew_value = np.trapz(integrand, wv[idl])
    print(ew_value)
    
#     plt.figure(figsize=[12,8])
#     plt.plot(wv,fl,'k')
#     plt.plot(wv[idb],fl[idb],'b')
#     plt.plot(wv[idl],fl[idl],'c')    
#     plt.plot(wv[idr],fl[idr],'r')
#     plt.plot(wv[idl],cont,'g--')     
#     plt.xlim(win_b[0],win_r[1])
    
    return ew_value