from dsviz.canvas import svg_plus_pdf
from dsviz.datastructures import VizList, VizBST, VizTree
from ds2.tree import Tree

def figpath(name):
    return '../figures/' + name

def drawbst(T, name):
    vizT = VizBST(T._root, (5,5))
    with svg_plus_pdf(600, vizT.height + 10, figpath(name)) as canvas:
        vizT.draw(canvas)

def drawlist(L, name):
    vizL = VizList(L)
    vizL.position = (5,5)
    with svg_plus_pdf(600, 60, figpath(name)) as canvas:
        vizL.draw(canvas)

def drawtree(T, name):
    if isinstance(T, list):
        T = Tree(T)
    vizT = VizTree(T)
    vizT.position = (5,5)
    with svg_plus_pdf(600, vizT.height + 10, figpath(name)) as canvas:
        vizT.draw(canvas)
