sel = hou.selectedNodes()
node_list = []
for nodes in sel :
    kids = nodes.children()
    for node in kids :
        if "Spine" in node.name():
            node_list.append(node.name())
print(node_list)