

def Piirto_suorakaide_poikkileikkaus_h_b_sc(h,b, sc=100):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    # b = b*1000
    # h= h*1000
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.add_patch(patches.Rectangle((0, 0), b, h, facecolor='white', edgecolor='black'))
    
    ### MITTA VAAKA ALKU ###
    # sc = 200
    mitta = [[[0,sc+h],[b,sc+h]]]
            # [[b_eff1,-sc],[b_w+b_eff1,-sc]],
            # [[b-b_eff2,-sc+h1],[b,-sc+h1]],
            # [[0,-sc+h1],[b_eff1,-sc+h1]]]
    
    for i in range(len(mitta)):
        xy1 = mitta[i][0]
        xy2 = mitta[i][1]
        # print(f"i = {i} , xy1 = {xy1},xy2 = {xy2}")
        ax.annotate("", xy=xy1, xytext=xy2, textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
        ax.annotate("", xy=xy1, xytext=xy2, textcoords=ax.transData, arrowprops=dict(arrowstyle='|-|'))
        bbox=dict(fc="white", ec="none")
        xx  = xy2[0]-xy1[0]
        ax.text(xy1[0]+((xy2[0]-xy1[0])/2), xy2[1], f" {xx:.6} mm", ha="center", va="center", bbox=bbox,rotation=0)
    ### MITTA VAAKA LOPPU ###
    
        ### MITTA PYSTY ALKU ###
    # sc = 200
    mitta = [[[-sc/2,0],[-sc/2,h]]]
            # [[b+sc,0],[b+sc,float(e_1.value)*1000]],
            # [[b/2,0],[b/2,float(y.value)*1000]],
            # [[b+sc*3,0],[b+sc*3,float(e_2.value)*1000]]]
            # [[b-b_eff2,-sc+h1],[b,-sc+h1]],
            # [[0,-sc+h1],[b_eff1,-sc+h1]]]
    for i in range(len(mitta)):
        xy1 = mitta[i][0]
        xy2 = mitta[i][1]
        # print(f"i = {i} , xy1 = {xy1},xy2 = {xy2}")
        ax.annotate("", xy=xy1, xytext=xy2, textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
        ax.annotate("", xy=xy1, xytext=xy2, textcoords=ax.transData, arrowprops=dict(arrowstyle='|-|'))
        bbox=dict(fc="white", ec="none")
        xx  = xy2[1]-xy1[1]
        ax.text(xy2[0], xy1[1]+((xy2[1]-xy1[1])/2), f" {xx:.6} mm", ha="center", va="center", bbox=bbox,rotation=90)
    ### MITTA PYSTY LOPPU ###
    
    
    # Aseta akselien rajat ja poista akselit
    ax.set_xlim(-sc, b+sc*2)
    ax.set_ylim(-sc, h+sc*2)
    ax.axis('on')

    plt.show()