def Teräs_rist_esimerkki_print():
    print("""
name = "Taso_ristikko_JV"
L = 28500#mm#Katon pääkannattajan jänneväli: 
b = 48000#mm #Hallin pituus
h = 9700#mm #Korkein piste 
h2 = 9200 # Pilarin korkeus
h1 = 7200#mm# Hallin vapaa korkeus lattiasta 
c = 6000#mm#Kehäväli: 
d = 1 # kpl Kehiä vierekkäin ### Ei vielä ihan valmista piirtä mutta dimension eivät toimi
max_kayt = 1 # Käyttäaste: saa maks olla 1 voidaan pienentää

q_k = 2.5 # Lumi kN/m^2
g_k = 0.5 # Yläpohja_rakenteet oma paino ilma ristikko kN/m^2
q = (c/1000)*((0.8*q_k*1.5)+g_k*1.15)

import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import matplotlib.path as mpath
from datetime import datetime


from metku.framefem import framefem as fem
from metku.raami.frame_node import FrameNode
from metku.raami.frame_member import FrameMember, SteelFrameMember
from metku.raami.frame_loads import PointLoad, LineLoad, PWLineLoad, LoadIDs, LoadCase, LoadCombination
from metku.raami.frame_supports import Support, FixedSupport, XYHingedSupport, XHingedSupport, YHingedSupport
from metku.raami.exports import AbaqusOptions, write_elset, write_nset



from metku.raami.raami_plane_truss import Ktruss_example, Ntruss_example
from metku.raami.raami_plane_truss import SlopedTruss
from metku.raami.exports import AbaqusOptions
from metku.raami.raami_truss_opt import minimize_eccentricity
from metku.optimization.solvers.slsqp import SLSQP
from metku.optimization.solvers.trust_region import TrustRegionConstr

def LauriKTruss(span,h2,h1,dx,nel_chord=4,nel_brace=4,ndiv=4):
    t = SlopedTruss(L1=0.5*span,L2=0.5*span,h2=h2,h1=h1,dx1=dx,dx2=dx)
    t.braces_as_beams = True
    t.generate_topology('K',ndiv,nel_chord=nel_chord,nel_brace=nel_brace)
    t.generate_supports()
    t.generate_joints()    
    t.symmetry()
    t.generate_uniform_load(q=-q)
    t.generate_fem(model='no_eccentricity')

    print("Structural analysis..")
    t.structural_analysis(load_id=t.load_ids[0],support_method="REM")
    print("Done.")

    top = {'material': 'S355', 'class': 2, 'utility': max_kayt}
    bottom = {'material': 'S355', 'class': 2, 'utility': max_kayt}
    braces = {'material': 'S355', 'class': 2, 'utility_tens': max_kayt, 'utility_comp':max_kayt}

    t.optimize_members(verb=True,top=top,bottom=bottom,braces=braces,limit_width=True)

    P, x0 = minimize_eccentricity(t,min_gap=10)   


    solver = SLSQP()
    #solver = TrustRegionConstr()
    #min_ecc, xmin = solver.solve(P,x0=x0,verb=True)
    #t.plot(geometry=True,loads=False)

    #t.clear_fem()
    #t.generate_fem(model="ecc_elements")
    #t.fem.draw()

    #t.print_member_utilization('Utilization.txt')

    # fig_save_opts = {'filename':'default.pdf','format':'pdf','orientation':'landscape','papertype':'a3'}    
    # t.plot(geometry=True,loads=False,save=True,saveopts=fig_save_opts)

    #t.generate_fem(model='ecc_elements')
    #opts = AbaqusOptions(x_monitor = 0.5*t.span, n_monitored = 2)
    #t.to_abaqus(filename='K-ristikko',partname="K-ristikko",options=opts)


    return t


if __name__ == "__main__":

    t = LauriKTruss(span=L,h2=h-h1,h1=h2-h1,dx=1500,nel_chord=3,nel_brace=3,ndiv=3)
    #t =  Ktruss_example(h2=2000,h1=1500,dx1=1000,dx2=1000,first=False,edges=True)
    #t =  Ntruss_example(h2=2000,h1=1500,dx1=1500,dx2=1500,first=False,edges=True)

    #t.generate_fem(model='en1993')
    #t.generate_fem(model='no_eccentricity')
    #t.structural_analysis(load_id=t.load_ids[0],support_method="REM")
    #x, xc = t.joints[4].brace_chord_face_x()
    #t.bmd(scale=10,load_id=t.load_ids[0])

#t.plot(geometry=True,loads=False)








#### TO DXF ###
import ezdxf

doc = ezdxf.new("R2010")
msp = doc.modelspace()

def dxf_list(points):
    num = len(points)
    for i  in range(num):
        if i+1 < num:
            p1 = points[i][0]
            p2 = points[i][1]
            p3 = points[i+1][0]
            p4 = points[i+1][1]
            msp.add_line((p1, p2), (p3, p4))
            # print([[p1, p2], [p3, p4]])



def dxf_add_rectangle(x1,x2,y1,y2):
    points = [[x1,y1],
            [x2,y1],
            [x2,y2],
            [x1,y2],
            [x1,y1]]
    dxf_list(points)

import numpy as np

x_p = np.linspace(0,b,int(b/c)+1)
y_p = np.arange(0,(int(d)+1)*L,L)

num = len(x_p)
num_y = len(y_p)
for i in range(num):
    for ii in range(num_y):
        if i+1 < num:
            if ii+1 < num_y:
                # p.append([v_x,v_y])
                p1 = x_p [i]
                p2 = y_p [ii]
                p3 = x_p [i]
                p4 = y_p [ii+1]
                msp.add_line((p1, p2), (p3, p4))

rec = dxf_add_rectangle
p = 0
for i in range(d+1):
    rec(p,b,p,L*i)

def ristiikko_pilari(x_of,text_s):
    ### Ristikko piirto alkaa ###
    off_x = b+L+x_of # Offset x
    off_y = h2
    f = t
    for v in f.members:
        number = v
        try:
            integer = int(number)
            vv = integer
            if integer > 0:
                vv = integer
            elif integer < 0:
                vv = integer
            else:
                vv = integer
        except ValueError:
            vv = f"{v}"
        # print(vv)
            # print("Enter integer value")
        p1 = f.members[vv].coords()[0][0]+off_x
        p2 = f.members[vv].coords()[0][1]+off_y
        p3 = f.members[vv].coords()[1][0]+off_x
        p4 = f.members[vv].coords()[1][1]+off_y
        # print(f.members[vv])
        # print(p1,p2,p3,p4)
        msp.add_line((p1, p2), (p3, p4))

        px = (p1+p3)/2
        py = (p2+p4)/2
        import numpy as np
        attribuutit = {
            'insert': (px, py),  # x, y sijainti
            'char_height': 50,  # merkin korkeus
            'rotation': np.rad2deg(f.members[vv].angle),        # Tekstin kiertokulma astetta
            'width': 1000  # Määritä tekstilaatikon leveys
        }
        if text_s == True:
            text = f"{f.members[vv].cross_section},id = {vv},""kayt_ast ={:.3f}".format(f.members[vv].utilization[0])
            msp.add_mtext(text, dxfattribs=attribuutit)
    ### Ristikko piirto loppu ###

    ### PILARI alkaa ###
    points = [[[off_x,0],[off_x,h2]],
        [[off_x+L,0],[off_x+L,h2]]]
    num = len(points)
    for i  in range(num):
        # if i+1 < num:
            p1 = points[i][0][0]
            p2 = points[i][0][1]
            p3 = points[i][1][0]
            p4 = points[i][1][1]            
            msp.add_line((p1, p2), (p3, p4))

    #### Mitta Vaaka alkaa ####
    dim_points = [[[points[0][1][0],points[0][1][1]],[points[1][1][0],points[1][1][1]]],
                [[0,L],[b,L]],
                [[0,L-(L/10)],[c,L-(L/10)]]]
                    #,
                # [[points[0][0][0],points[0][0][1]],[points[1][1][1],points[1][1][1]]]]

    for i  in range(len(dim_points)):
        dim = msp.add_aligned_dim(p1=(dim_points[i][0][0],dim_points[i][0][1]), p2=(dim_points[i][1][0],dim_points[i][1][1]), distance=h/3,    override={
            "dimtxsty": "Standard",
            "dimtxt": 800,
            "dimclrt": 1,
            "dimexo": h/4,  # offset from measurement point
            "dimlwe": 1000,   # 0.35mm line weight
            "dimexe": 100,  # length above dimension line
            "dimasz": 400,  # arrow size in drawing units
            "dimblk": "OBLIQUE",  # arrow block name
        })
        dim.render()
    #### Mitta Vaaka loppu ####


    #### Mitta Pysty alkaa####
    dim_points =[[[points[0][0][0],points[0][0][1]],[points[0][0][0],points[0][1][1]]],
                [[0,0],[0,L]]]
    for i  in range(len(dim_points)):
        dim = msp.add_aligned_dim(p1=(dim_points[i][0][0],dim_points[0][0][1]), p2=(dim_points[i][1][0],dim_points[i][1][1]), distance=h/3,    override={
            "dimtxsty": "Standard",
            "dimtxt": 800,
            "dimclrt": 1,
            "dimexo": h/4,  # offset from measurement point
            "dimlwe": 1000,   # 0.35mm line weight
            "dimexe": 100,  # length above dimension line
            "dimasz": 400,  # arrow size in drawing units
            "dimblk": "OBLIQUE",  # arrow block name
        })
        dim.render()
    #### Mitta Pysty loppu####



ristiikko_pilari(x_of=0,text_s=True)
ristiikko_pilari(x_of=L*2,text_s=False)


name_d = "{}_{}m.dxf".format(name,L/1000)
name_jv = "Member_info_{}_{} m".format(name,L/1000)
doc.saveas(name_d)


    ### Report Excel and PDF Start###
from BW import EXCEL
# name = "O_Member_info_Truss"
data  = []
data.append(["id","PROF"," ","Käyttö-","Pituus","M_Y_Ed","N_Ed","V_z_Ed ","f_y"])
data.append(["    ","   ","   ","aste","[mm]","[kNm]","[kN]","[kN]","[MPa]"])
f = t
for v in f.members:
    number = v
    try:
        integer = int(number)
        vv = integer
        if integer > 0:
            vv = integer
        elif integer < 0:
            vv = integer
        else:
            vv = integer
    except ValueError:
        vv = f"{v}"
    # print(vv)
        # print("Enter integer value")
    d1 = "{}".format(vv)
    d11 = "{}".format(f.members[vv].cross_section)
    d12 = " "
    d2 = "{:.3f}".format(f.members[vv].utilization[0])
    d3 = "{:.1f}".format(f.members[vv].length())
    d4 = "{:.1f} ".format(f.members[vv].MyEd[0]/1000000)
    d5 = "{:.1f} ".format(f.members[vv].NEd[0]/1000)
    d6 = "{:.1f}".format(f.members[vv].VzEd[0]/1000)
    d7 = "{:.1f}".format(f.members[vv].material.fy)
    data.append([d1,d11,d12,d2,d3,d4,d5,d6,d7])


EXCEL.python_list_to_excel(data,name_jv)
EXCEL.excel_to_pdf(name_jv)


### DXF TO PDF start###
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import re

class DXF2IMG(object):

    default_img_format = '.png'
    default_img_res = 300

    def convert_dxf2img(self, names, img_format=default_img_format, img_res=default_img_res):
        for name in names:
            doc = ezdxf.readfile(name)
            msp = doc.modelspace()
            
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise Exception("The DXF document is damaged and can't be converted!")
            else:
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                
                # Set background color to white
                ctx = RenderContext(doc)
                ctx.current_layout = msp  # manually set current_layout
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)

                # Set background color to white
                ax.set_facecolor('#FFFFFF')
                
                # Set line color to black
                for line in ax.lines:
                    line.set_color('#000000')

                img_name = re.findall("(\S+)\.", name)
                first_param = ''.join(img_name) + img_format
                fig.savefig(first_param, dpi=img_res)

if __name__ == '__main__':
    first = DXF2IMG()
    first.convert_dxf2img([name_d], img_format='.png')
    first.convert_dxf2img([name_d], img_format='.pdf')


### DXF TO PDF end###

t.to_robot()

    """)