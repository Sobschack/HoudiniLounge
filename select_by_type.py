sel = hou.selectedNodes()[0]

mat_node_list = []
for node in my_network:
    if node.type().name() == 'material':