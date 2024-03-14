def Boltgrp_calc(fx,fy,mz_m,xf,yf,boltx,bolty,mut_dia,r_dia,alus_dia,l_h,l_b,show_plot = True,show_laskenta = True):
    import numpy as np
    mz = mz_m*1000
    
    import math
    
    if (len(boltx)!=len(bolty)):
        return -1

    number = len(boltx)
    #bolt CGs
    cgx=math.fsum(boltx)/number	
    cgy=math.fsum(bolty)/number

    #Moment due to forces and total moment
    mzfx=fx*(cgy-yf)
    mzfy=-fy*(cgx-xf)
    mztot=mz+mzfx+mzfy

    #direct shear loads
    pfx=fx/number
    pfy=fy/number

    #radii to compute direction cosines
    #radii squared, and radii
    rx = []
    ry = []
    rsquared = []
    r = []

    for i in range(0,number):
        rx.append(boltx[i]-cgx)
        ry.append(bolty[i]-cgy)
        rsquared.append(rx[i]**2 + ry[i]**2)
        r.append(math.sqrt(rsquared[i]))

    sumr2 = math.fsum(rsquared)
    #radius/sum of radii squared to determine tangential force
    #tangential force calculation
    rdsumr2 = []
    ft = []

    for i in range(0,number):
        rdsumr2.append(r[i]/sumr2)
        ft.append(rdsumr2[i]*mztot)

    #determine components of tangential forces in x,y coordinates
    rxdr=[]
    rydr=[]
    pmx=[]
    pmy=[]
    #determine total x, y forces and shear on bolts
    px=[]
    py=[]
    pxy=[]

    for i in range(0,number):
        rxdr.append(rx[i]/r[i])
        rydr.append(ry[i]/r[i])
        pmx.append(-ft[i]*rydr[i])
        pmy.append(ft[i]*rxdr[i])
        px.append(pmx[i]+pfx)
        py.append(pmy[i]+pfy)
        pxy.append(math.sqrt(py[i]**2 + px[i]**2))

    #find resultant total loads and moments to check vs. input
    sx=math.fsum(px)
    sy=math.fsum(py)
    mpx=[]
    mpy=[]

    for i in range(0,number):
        mpx.append(-px[i]*(bolty[i]-yf))
        mpy.append(py[i]*(boltx[i]-xf))

    #check resulting moments calculated at input loads vs input
    rmx=math.fsum(mpx)
    rmy=math.fsum(mpy)
    rmtot=rmx+rmy
    ex=math.fabs(sx-fx)/math.fabs(fx)
    ey=math.fabs(sy-fy)/math.fabs(fy)
    em=math.fabs(rmtot-mz)/math.fabs(mz)
    tulos = [boltx, bolty,px,py,pxy,ex,ey,em]
    



    if show_plot ==True:
        from matplotlib.patches import RegularPolygon
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
        tulos_t = np.transpose(np.array([tulos[0],tulos[1],tulos[2],tulos[3],tulos[4]]))

        fig, ax = plt.subplots(figsize=(10,10))
        reikä_kord =np.array([tulos[0],tulos[1]])
        reikä_kord_t =np.transpose(np.array([tulos[0],tulos[1]]))


        for reunat in reikä_kord_t :
            reiät_hex = RegularPolygon((reunat[0],reunat[1]),numVertices = 6,radius=mut_dia/2 ,edgecolor= "grey",linewidth = 2, facecolor="none")
            reiät_circle = plt.Circle((reunat[0],reunat[1]),radius=r_dia/2 ,edgecolor= "grey",linewidth = 2, facecolor="none")
            aluslevy_pirt =  plt.Circle((reunat[0],reunat[1]),radius=alus_dia/2 ,edgecolor= "grey",linewidth = 2, facecolor="none")
            ax.add_patch(reiät_hex)
            ax.add_patch(reiät_circle)
            ax.add_patch(aluslevy_pirt)


        for arvot in tulos_t:
            ax.annotate("", xy=((arvot[0],arvot[1])), xytext=((arvot[0]+arvot[2],arvot[1]+arvot[3])),arrowprops=dict(arrowstyle="->"),size =10) #Nuoli
            ax.text(arvot[0],arvot[1]+mut_dia,'$ {:.4}kN$'.format(arvot[4]),color = 'black')
        #plt.plot(reikä_kord[:,0:1],reikä_kord[:,1:2],color='blue')

        x = np.array([0,l_b,l_b,0,0])
        y = np.array([0,0,l_h,l_h,0])

        import matplotlib.patches as patches
        style = "Simple, tail_width=0.5, head_width=4, head_length=4"
        kw = dict(arrowstyle=style, color="k")
        a3 = patches.FancyArrowPatch((xf-(xf/10),yf),(xf+(xf/10),yf) ,connectionstyle="arc3,rad=-.9", **kw)
        plt.gca().add_patch(a3)
        ax.text(xf+20,yf+10,'$ M_Ed = {:.4}kNm$'.format(float(mz_m)),color = 'black')

        ax.annotate("", xy=((xf,yf-(20))), xytext=((xf,yf+(20))),arrowprops=dict(arrowstyle="->"),size =10) #Nuoli
        ax.text(xf+20,yf-10,'$ fy = {:.4}kN$'.format(float(fy)),color = 'black')

        ax.annotate("", xy=((xf+(20),yf)), xytext=((xf-(20),yf)),arrowprops=dict(arrowstyle="->"),size =10) #Nuoli
        ax.text(xf-100,yf,'$ fx = {:.4}kN$'.format(float(fx)),color = 'black')


        plt.xlabel('b [mm]')
        plt.ylabel('h [mm]')

        #plt.title('PULTTIRYHMÄ')

        plt.plot(x,y,color='blue')
        plt.savefig("pultti_ryhma.pdf", format="pdf", bbox_inches="tight")
        plt.savefig("pultti_ryhma.png", format="png", bbox_inches="tight")
        plt.show()
    
    if show_laskenta == True:
        return boltx, bolty,px,py,pxy,ex,ey,em
    
def Bolt_tulosta_koordinaatit(s_x, e_x,x_num, s_y, e_y,y_num):
    import numpy as np
    boltx = np.linspace(s_x, e_x,x_num)
    bolty = np.linspace(s_y, e_y,y_num)

    x_coords = []
    y_coords = []

    for x in boltx:
        for y in bolty:
            x_coords.append(x)
            y_coords.append(y)

    x_array = np.array(x_coords)
    y_array = np.array(y_coords)
    
    return x_array, y_array

def Bolt_esimerkki_print():
    
    print(f"""
from BW import BOLT
import numpy as np

s_x = 30 # Start kord-x
e_x = 170 # End kord-x
x_num = 2 # X-rivi määrä

s_y = 30 # Start kord-y
e_y = 300 # End kord-y
y_num = 10 # y-rivi määrä
x_koord, y_koord = BOLT. Bolt_tulosta_koordinaatit(s_x, e_x,x_num, s_y, e_y,y_num)


fx=0.00001 # Voima-X[kN]
fy=float(F_v_lisa_n)#44 # Voima-Y[kN]
mz_m=0.00001 # Voima-Momentti[kN]

boltx = x_koord
bolty=y_koord

xf= np.average(boltx) #Voiman vaikutus X
yf= np.average(bolty) #Voiman vaikutus X


mut_dia = 9 #Mutterin dia
r_dia = 5 #Pultti_dia
alus_dia = 5 #Aluslevy_dia
l_h = 400# Teräslevy korkeus
l_b = 200 # Teräslevy leveys

Bolt_tulos = BOLT.Boltgrp_calc(fx,fy,mz_m,xf,yf,boltx,bolty,mut_dia,r_dia,alus_dia,l_h,l_b,show_plot = True,show_laskenta = True)
Bolt_tulos
        """)