import hou

sel = hou.selectedNodes()[0] #must be a hou.ShopNode or hou.ObjNode instance
kids = sel.children() #must be a tuple of nodes

move_to = hou.node("/mat")

print "sel est de type : "type(sel)
print "kids est de type : " type(kids)

hou.copyNodesTo(kids, move_to)

# sel est de type : <class 'hou.ShopNode'>
# kids est de type : <type 'tuple'>