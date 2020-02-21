sel = hou.selectedNodes()
for nodes in sel :
    kids = nodes.children()
    for node in kids :
        if node.type().name() == "null":
            node.destroy()