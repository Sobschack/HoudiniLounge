selection = hou.selectedNodes()
for nodes in selection :
    kids = nodes.children()
    for node in kids :
        if node.type().name() == "null":
            node.destroy()