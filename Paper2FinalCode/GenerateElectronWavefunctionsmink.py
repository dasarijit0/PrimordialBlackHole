#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np 
import math
import matplotlib.pyplot as plt 
from scipy import optimize
from scipy.optimize import fsolve


from sympy import symbols
from sympy.physics.wigner import wigner_3j
import module1 as m1 # module1 contains the function to convert r_star to r\n",

import I_functions_class as Inp
from astropy.io import fits
import sys 
import os 

k = -1*int(sys.argv[1])

hdu_c = fits.open('/users/PCON0003/koivuemily/PrimordialBlackHole/Constants.fits')


nu =  hdu_c[0].header['nu']
mu = hdu_c[0].header['mu']
lam = hdu_c[0].header['lam']
GC = hdu_c[0].header['GC']
c = hdu_c[0].header['c']
tol = hdu_c[0].header['tol']

M = hdu_c[0].header['M']
r_initial = hdu_c[0].header['r_init']
r_final= hdu_c[0].header['r_final']
T = hdu_c[0].header['Temp']

Elec_direc = hdu_c[0].header['E_direc']



h = np.linspace(.01*T,20.*T,2000)



hdu = fits.Header()
hdu['type']='Electron Wavefunction'
hdu['r_init']=r_initial
hdu['r_final']=r_final
hdu['M']= M
hdu['l']=k
hdu['tol']=tol
hdu['mu']=mu
hdu['nu']=nu
hdu['lam']=lam
empty_primary = fits.PrimaryHDU(header=hdu)
hdul = fits.HDUList([empty_primary])


# In[20]:


for x in range(len(h)):
    EWF = Inp.ElectronWaveFunction(nu, h[x], k, mu, M, lam, GC, c, tol)
    r_points, F_points, G_points = EWF.RK_4(r_initial, r_final, 240000, up = True)
    r_points_in, F_points_in, G_points_in = EWF.RK_4(r_final, r_initial, 240000, up = False)
    R,T,delta = EWF.get_R_and_T_coeff(r_points,F_points,G_points,r_points_in,F_points_in,G_points_in)

    
    #store every other point in the file
    #also save the reversed rin, and photon fields in so that you only have to store one r values
    
    #cutoff r to 2000M so that we can match analytically in the integrator later

    col1r = fits.Column(name='rpoints_up',format='D',array=r_points[::2])
    col2F = fits.Column(name='F_points_up',format='M',array=F_points[::2])
    col2G = fits.Column(name='G_points_up',format='M',array=G_points[::2])
    col2Fin = fits.Column(name='F_points_in',format='M',array=F_points_in[::-1][::2])
    col2Gin = fits.Column(name='G_points_in',format='M',array=G_points_in[::-1][::2])
    
    cols = fits.ColDefs([col1r, col2F,col2G,col2Fin,col2Gin])
    table_hdu = fits.BinTableHDU.from_columns(cols)
    table_hdu.header['h']=h[x]
    table_hdu.header['R']=R
    table_hdu.header['T']=T
    table_hdu.header['delta']=delta
    
    hdul.append(table_hdu)



hdul.writeto(Elec_direc +'min'+str(np.abs(k))+'ExtendedOmega.fits')






