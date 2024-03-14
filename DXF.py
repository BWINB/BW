def BW_DXF_to_CSV_txt(DXF_file_ilman_ext):
    kohde = DXF_file_ilman_ext
    #kohde = 'Teräs'
    dwg_file_path = "{}.dxf".format(kohde)  # Anna oikea polku DXF-tiedostoon
    csv_file_path = "{}_raaka.csv".format(kohde)  # Anna polku, johon tallennetaan CSV-tiedosto

    CSV_luettelo_tyhja = '{}_luettelo_tyhja.csv'.format(kohde)
    CSV_luettelo = '{}_luettelo.csv'.format(kohde)
    PDF_luettelo = '{}_luettelo.pdf'.format(kohde)
    
    ####
    import ezdxf
    import csv

    def extract_text_from_entity(entity):
        if entity.dxftype() in ("TEXT", "MTEXT"):
            return entity.dxf.text
        elif entity.dxftype() == "INSERT":
            texts = []
            attribs = entity.attribs
            for attrib in attribs:
                texts.append(attrib.dxf.text)
            return texts
        else:
            return None

    def extract_text_from_doc(doc):
        texts = []

        msp = doc.modelspace()
        for entity in msp:
            text = extract_text_from_entity(entity)
            if text is not None:
                if isinstance(text, list):
                    texts.extend(text)
                else:
                    texts.append(text)

        return texts

    def save_to_csv(data, output_file):
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Teksti"])
            for text in data:
                writer.writerow([text])


    doc = ezdxf.readfile(dwg_file_path)
    texts = extract_text_from_doc(doc)

    # Tallenna kaikki tekstit CSV-tiedostoon
    save_to_csv(texts, csv_file_path)



def DXF_to_CSV_line(dxf_file,csv_file):
           
    import ezdxf
    import csv
    
    # Lue DXF-tiedosto
    doc = ezdxf.readfile(dxf_file)

    # Valitse mallit, joista haluat tiedot
    modelspace = doc.modelspace()

    # Luo CSV-tiedosto tiedoille
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Kirjoita otsikkorivi CSV-tiedostoon
        csvwriter.writerow(["Type", "Start Point", "End Point", "Radius", "Center"])

        # Iteroi kaikkien piirustusentiteettien läpi
        for entity in modelspace:
            if entity.dxftype() == 'LINE':
                # Kirjoita viivan tiedot
                csvwriter.writerow([entity.dxftype(), entity.dxf.start, entity.dxf.end])
            elif entity.dxftype() == 'CIRCLE':
                # Kirjoita ympyrän tiedot
                csvwriter.writerow([entity.dxftype(), '', '', entity.dxf.radius, entity.dxf.center])

def tulosta_metku_members_to_dxf (f,dxf_name):
    import ezdxf

    # create a new DXF R2010 document
    doc = ezdxf.new("R2010")

    # add new entities to the modelspace
    msp = doc.modelspace()
    # add a LINE entity

    for i in range(len(f.members)):
        p1 = f.members[i].coords()[0][0]
        p2 = f.members[i].coords()[0][1]
        p3 = f.members[i].coords()[1][0]
        p4 = f.members[i].coords()[1][1]
        msp.add_line((p1, p2), (p3, p4))
        # print(p1,p2,p3,p4)
        
    # save the DXF document
    doc.saveas(dxf_name)

# def tulosta_metku_truss_members_to_dxf (f,dxf_name):
#     import ezdxf

#     # create a new DXF R2010 document
#     doc = ezdxf.new("R2010")

#     # add new entities to the modelspace
#     msp = doc.modelspace()
#     # add a LINE entity

#     for v in f.members:
#         # print(v)
#         vv = f"{v}"
#         #f.append(t.members[vv])
#         p1 = f.members[vv].coords()[0][0]
#         p2 = f.members[vv].coords()[0][1]
#         p3 = f.members[vv].coords()[1][0]
#         p4 = f.members[vv].coords()[1][1]
#         msp.add_line((p1, p2), (p3, p4))


#     # for i in range(len(f.members)):
#     #     p1 = f.members[i].coords()[0][0]
#     #     p2 = f.members[i].coords()[0][1]
#     #     p3 = f.members[i].coords()[1][0]
#     #     p4 = f.members[i].coords()[1][1]
#     #     msp.add_line((p1, p2), (p3, p4))
#     #     # print(p1,p2,p3,p4)
        
#     # save the DXF document
#     doc.saveas(dxf_name)

def tulosta_metku_truss_members_to_dxf (f,dxf_name):
    import ezdxf

    # create a new DXF R2010 document
    doc = ezdxf.new("R2010")

    # add new entities to the modelspace
    msp = doc.modelspace()
    # add a LINE entity

    for v in f.members:
        # print(v)
        number = v
        try:
            integer = int(number)
            vv = integer
            if integer > 0:
                vv = integer
                # print "positive", integer
            elif integer < 0:
                vv = integer
                # print "Negative", integer
            else:
                vv = integer
                # print "Number is", integer

        except ValueError:
            vv = f"{v}"
        # print(vv)
            # print("Enter integer value")
        p1 = f.members[vv].coords()[0][0]
        p2 = f.members[vv].coords()[0][1]
        p3 = f.members[vv].coords()[1][0]
        p4 = f.members[vv].coords()[1][1]
        # print(p1,p2,p3,p4)
        msp.add_line((p1, p2), (p3, p4))

        # try:
        #     p5 = f.members[vv].coords()[2][0]
        #     p6 = f.members[vv].coords()[2][1]
        #     msp.add_line((p3, p4), (p5, p6))
        # except ValueError:
        #     vvv = 0

#     # save the DXF document
    doc.saveas(dxf_name)




def tulosta_metku_truss_members_to_dxf_member_text (f,dxf_name,show_member = True):
    import ezdxf

    # create a new DXF R2010 document
    doc = ezdxf.new("R2010")

    # add new entities to the modelspace
    msp = doc.modelspace()
    # add a LINE entity

    for v in f.members:
        # print(v)
        number = v
        try:
            integer = int(number)
            vv = integer
            if integer > 0:
                vv = integer
                # print "positive", integer
            elif integer < 0:
                vv = integer
                # print "Negative", integer
            else:
                vv = integer
                # print "Number is", integer

        except ValueError:
            vv = f"{v}"
        # print(vv)
            # print("Enter integer value")
        p1 = f.members[vv].coords()[0][0]
        p2 = f.members[vv].coords()[0][1]
        p3 = f.members[vv].coords()[1][0]
        p4 = f.members[vv].coords()[1][1]
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
        text = f"{f.members[vv].cross_section},id = {vv},""kayt_ast ={:.3f}".format(f.members[vv].utilization[0])
        if show_member ==True:
            msp.add_mtext(text, dxfattribs=attribuutit)


        # try:
        #     p5 = f.members[vv].coords()[2][0]
        #     p6 = f.members[vv].coords()[2][1]
        #     msp.add_line((p3, p4), (p5, p6))
        # except ValueError:
        #     vvv = 0

#     # save the DXF document
    doc.saveas(dxf_name)



def DXF_piirtä_esimerkki():
    print("""
import ezdxf
dxf_name = "Poikkileikkaus.dxf"
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
            print([[p1, p2], [p3, p4]])



def dxf_add_rectangle(x1,x2,y1,y2):
    points = [[x1,y1],
             [x2,y1],
             [x2,y2],
             [x1,y2],
             [x1,y1]]
    dxf_list(points)



rec = dxf_add_rectangle
rec(0,10,0,20)
rec(10,20,20,40)

doc.saveas(dxf_name)
          """)

def dxf_list(points):
    num = len(points)
    for i  in range(num):
        if i+1 < num:
            p1 = points[i][0]
            p2 = points[i][1]
            p3 = points[i+1][0]
            p4 = points[i+1][1]
            msp.add_line((p1, p2), (p3, p4))
            print([[p1, p2], [p3, p4]])



def dxf_add_rectangle(x1,x2,y1,y2):
    points = [[x1,y1],
             [x2,y1],
             [x2,y2],
             [x1,y2],
             [x1,y1]]
    dxf_list(points)
def dxf_export_to_pdf_or_png(dxf_name,to_format_end):
    import matplotlib.pyplot as plt
    import ezdxf
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    # import wx
    import glob
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
                    raise exception("The DXF document is damaged and can't be converted!")
                else :
                    fig = plt.figure()
                    ax = fig.add_axes([0, 0, 1, 1])
                    ctx = RenderContext(doc)
                    ctx.set_current_layout(msp)
                    # ctx.current_layout.set_colors(bg='#FFFFFF')
                    out = MatplotlibBackend(ax)
                    Frontend(ctx, out).draw_layout(msp, finalize=True)

                    img_name = re.findall("(\S+)\.",name)  # select the image name that is the same as the dxf file name
                    first_param = ''.join(img_name) + img_format  #concatenate list and string
                    fig.savefig(first_param, dpi=img_res)


    if __name__ == '__main__':
        first =  DXF2IMG()
        first.convert_dxf2img([dxf_name],img_format=to_format_end)

def DXF_rec(b,h,name,on_pdf = False,on_png = False):
    #h = 1000
    #b = 200
    #name = "Test"
    #on_pdf = True # Check if to print pdf
    #on_png = False # Check if to print png


    #### START DRAWING DXF ###
    import ezdxf
    doc = ezdxf.new("R2010") # Version
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

    def dxf_add_rectangle(x1,x2,y1,y2):
        points = [[x1,y1],
                [x2,y1],
                [x2,y2],
                [x1,y2],
                [x1,y1]]
        dxf_list(points)


    rec = dxf_add_rectangle
    p_x = 0 # Start corner x
    p_y = 0 # Start corner y
    rec(p_x,b+p_x,p_y,h+p_y)


    # SAVE TO DXF
    name_d = "{}.dxf".format(name)
    doc.saveas(name_d)
    #### END DRAWING DXF ###

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
        if on_png == True:
            first.convert_dxf2img([name_d], img_format='.png')

        if on_pdf == True:
            first.convert_dxf2img([name_d], img_format='.pdf')

    ### DXF TO PDF end###


def DXF_rec_dimension(b,h,name,dim_y ,dim_x,dim_sc,on_pdf ,on_png ):
    #h = 1000
    #b = 20000
    #dim_y = h
    #dim_x = dim_y
    #dim_sc = 0.5
    #name = "Test_dimension"
    #on_pdf = True # Check if to print pdf
    #on_png = False # Check if to print png


    #### START DRAWING DXF ###
    import ezdxf
    doc = ezdxf.new("R2010") # Version
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

    def dxf_add_rectangle(x1,x2,y1,y2):
        points = [[x1,y1],
                [x2,y1],
                [x2,y2],
                [x1,y2],
                [x1,y1]]
        dxf_list(points)


    rec = dxf_add_rectangle
    p_x = 0 # Start corner x
    p_y = 0 # Start corner y
    rec_1 = [p_x,b+p_x,p_y,h+p_y]
    rec(rec_1[0],rec_1[1],rec_1[2],rec_1[3])

    ### Dimensions Starts!!!

    #### Mitta Vaaka alkaa ####
    def lista_x1x2y1y2_to_split_p1p2_dim(rec_1):
        return [[rec_1[0],rec_1[2]-dim_y],[rec_1[1],rec_1[2]-dim_y]]
    dim_points = [lista_x1x2y1y2_to_split_p1p2_dim(rec_1)]

    #dim_points = [[[points[0][1][0],points[0][1][1]],[points[1][1][0],points[1][1][1]]],
    #            [[0,L],[b,L]],
    #            [[0,L-(L/10)],[c,L-(L/10)]]]

    for i  in range(len(dim_points)):
        dim = msp.add_aligned_dim(p1=(dim_points[i][0][0],dim_points[i][0][1]), p2=(dim_points[i][1][0],dim_points[i][1][1]), distance=h/3,    override={
            "dimtxsty": "Standard",
            "dimtxt": 800*dim_sc,
            "dimclrt": 6, #Color
            "dimexo": h/4,  # offset from measurement point
            "dimlwe": 100,   # 0.35mm line weight
            "dimexe": 100,  # length above dimension line
            "dimasz": 400,  # arrow size in drawing units
            "dimblk": "OBLIQUE",  # arrow block name
        })
        dim.render()
    #### Mitta Vaaka loppu ####


    #### Mitta Pysty alkaa####
    def lista_x1x2y1y2_to_split_p1p2_dim_hight(rec_1):
        return [[rec_1[0],rec_1[2]],[rec_1[0],rec_1[3]]]
    dim_points = [lista_x1x2y1y2_to_split_p1p2_dim_hight(rec_1)]

    #dim_points =[[[points[0][0][0],points[0][0][1]],[points[0][0][0],points[0][1][1]]],
    #            [[0,0],[0,L]]]
    for i  in range(len(dim_points)):
        dim = msp.add_aligned_dim(p1=(dim_points[i][0][0],dim_points[0][0][1]), p2=(dim_points[i][1][0],dim_points[i][1][1]), distance=h/3,    override={
            "dimtxsty": "Standard",
            "dimtxt": 800*dim_sc,
            "dimclrt": 6, #Color
            "dimexo": h/4,#h/4,  # offset from measurement point
            "dimlwe": 100,   # 0.35mm line weight
            "dimexe": 100,  # length above dimension line
            "dimasz": 400,  # arrow size in drawing units
            "dimblk": "OBLIQUE",  # arrow block name
        })
        dim.render()
    #### Mitta Pysty loppu####

    ### Dimensions Ends!!!





    # SAVE TO DXF
    name_d = "{}.dxf".format(name)
    doc.saveas(name_d)
    #### END DRAWING DXF ###

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
        if on_png == True:
            first.convert_dxf2img([name_d], img_format='.png')

        if on_pdf == True:
            first.convert_dxf2img([name_d], img_format='.pdf')

    ### DXF TO PDF end###


def DXF_rec_dimension_print_as_text_simple_example():

	print("""
	b = 7000
	h = 250
	DXF_rec_dimension(b ,h ,name="BEAM_h={}m ,b={}m ".format(h/1000,b/1000),dim_sc = 0.2,on_pdf = True,on_png = False,dim_y = h,dim_x = dim_y)
	""")





def DXF_rec_dimension_As_text_complete_example():
	print("""
    def DXF_rec_dimension(b,h,name,dim_sc = 0.5,on_pdf = False,on_png = False,dim_y = h,dim_x = dim_y):
    #h = 1000
    #b = 20000
    #dim_y = h
    #dim_x = dim_y
    #dim_sc = 0.5
    #name = "Test_dimension"
    #on_pdf = True # Check if to print pdf
    #on_png = False # Check if to print png


    #### START DRAWING DXF ###
    import ezdxf
    doc = ezdxf.new("R2010") # Version
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

    def dxf_add_rectangle(x1,x2,y1,y2):
        points = [[x1,y1],
                [x2,y1],
                [x2,y2],
                [x1,y2],
                [x1,y1]]
        dxf_list(points)


    rec = dxf_add_rectangle
    p_x = 0 # Start corner x
    p_y = 0 # Start corner y
    rec_1 = [p_x,b+p_x,p_y,h+p_y]
    rec(rec_1[0],rec_1[1],rec_1[2],rec_1[3])

    ### Dimensions Starts!!!

    #### Mitta Vaaka alkaa ####
    def lista_x1x2y1y2_to_split_p1p2_dim(rec_1):
        return [[rec_1[0],rec_1[2]-dim_y],[rec_1[1],rec_1[2]-dim_y]]
    dim_points = [lista_x1x2y1y2_to_split_p1p2_dim(rec_1)]

    #dim_points = [[[points[0][1][0],points[0][1][1]],[points[1][1][0],points[1][1][1]]],
    #            [[0,L],[b,L]],
    #            [[0,L-(L/10)],[c,L-(L/10)]]]

    for i  in range(len(dim_points)):
        dim = msp.add_aligned_dim(p1=(dim_points[i][0][0],dim_points[i][0][1]), p2=(dim_points[i][1][0],dim_points[i][1][1]), distance=h/3,    override={
            "dimtxsty": "Standard",
            "dimtxt": 800*dim_sc,
            "dimclrt": 6, #Color
            "dimexo": h/4,  # offset from measurement point
            "dimlwe": 100,   # 0.35mm line weight
            "dimexe": 100,  # length above dimension line
            "dimasz": 400,  # arrow size in drawing units
            "dimblk": "OBLIQUE",  # arrow block name
        })
        dim.render()
    #### Mitta Vaaka loppu ####


    #### Mitta Pysty alkaa####
    def lista_x1x2y1y2_to_split_p1p2_dim_hight(rec_1):
        return [[rec_1[0],rec_1[2]],[rec_1[0],rec_1[3]]]
    dim_points = [lista_x1x2y1y2_to_split_p1p2_dim_hight(rec_1)]

    #dim_points =[[[points[0][0][0],points[0][0][1]],[points[0][0][0],points[0][1][1]]],
    #            [[0,0],[0,L]]]
    for i  in range(len(dim_points)):
        dim = msp.add_aligned_dim(p1=(dim_points[i][0][0],dim_points[0][0][1]), p2=(dim_points[i][1][0],dim_points[i][1][1]), distance=h/3,    override={
            "dimtxsty": "Standard",
            "dimtxt": 800*dim_sc,
            "dimclrt": 6, #Color
            "dimexo": h/4,#h/4,  # offset from measurement point
            "dimlwe": 100,   # 0.35mm line weight
            "dimexe": 100,  # length above dimension line
            "dimasz": 400,  # arrow size in drawing units
            "dimblk": "OBLIQUE",  # arrow block name
        })
        dim.render()
    #### Mitta Pysty loppu####

    ### Dimensions Ends!!!





    # SAVE TO DXF
    name_d = "{}.dxf".format(name)
    doc.saveas(name_d)
    #### END DRAWING DXF ###

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
        if on_png == True:
            first.convert_dxf2img([name_d], img_format='.png')

        if on_pdf == True:
            first.convert_dxf2img([name_d], img_format='.pdf')

    ### DXF TO PDF end###
    """)