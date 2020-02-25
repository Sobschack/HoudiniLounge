import hou

sel = hou.selectedNodes()[0]
geo = sel.geometry()

node = geo.findPrimAttrib("shop_materialpath")
value = node.strings()
print node
print type(node)
print value
print type(value)