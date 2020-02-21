import os

#create variables
my_path = hou.ui.selectFile(file_type=hou.fileType.Directory)
my_path_expanded = hou.expandString(my_path)
my_files_list = os.listdir(my_path_expanded)
network_nodes = []

#create geo node
loader = hou.node('/obj').createNode('geo', "OBJ_Loader")

#create file nodes to import objects from directory
for i in my_files_list:
        print(i)
        obj_file_node = loader.createNode('file', i)
        obj_file_node.parm('file').set(os.path.join(my_path, i))
        obj_file_node.parm('missingframe').set(1)
        network_nodes.append(obj_file_node)
#create merge node
merge_node = loader.createNode('merge', 'OBJs_Merger')
#connect files nodes to merge.
for j in network_nodes:
        merge_node.setNextInput(j)
#Create & connect merge to null 
null_node = loader.createNode('null', 'OUT_GEO')
null_node.setFirstInput(merge_node)
null_node.setDisplayFlag(True)
null_node.setRenderFlag(True)
null_node.setCurrent(True, clear_all_selected=True)

#Layout network
loader.layoutChildren()