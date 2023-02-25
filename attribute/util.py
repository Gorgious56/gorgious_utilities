def get_bmesh_domain(bm, domain):
    if domain == "POINT":
        return bm.verts
    elif domain == "EDGE":
        return bm.edges
    elif domain == "FACE":
        return bm.faces
