def tulosta_pdf_noinput():
    print("!jupyter nbconvert --to webpdf  --no-input  *.ipynb")

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

        if show_member ==True:
            msp.add_mtext(f.members[vv].cross_section, dxfattribs=attribuutit)


        # try:
        #     p5 = f.members[vv].coords()[2][0]
        #     p6 = f.members[vv].coords()[2][1]
        #     msp.add_line((p3, p4), (p5, p6))
        # except ValueError:
        #     vvv = 0

#     # save the DXF document
    doc.saveas(dxf_name)