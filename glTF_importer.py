import hou
#create global network instance
my_network = hou.node("/obj/").children()
mat_context = hou.node("/mat")

#create glTF loader subnetwork
glTF_Loader = hou.node('/obj').createNode('subnet', 'glTF_Loader')
glTF_Loader.moveToGoodPosition()

#create a list of all glTF hierarchy nodes
gltf_hierarchy_list = []
for nodes in my_network:
    if nodes.type().name() == 'gltf_hierarchy':
        gltf_hierarchy_list.append(nodes)

#create sub_geo for each glTF hierarchy in glTF_Loader
for nodes in gltf_hierarchy_list:
    geo_node = glTF_Loader.createNode('subnet', nodes.name())
    sub_geo = nodes.children()
    for i in sub_geo :
        geo_node_list = []
        if i.type().name() == 'geo':
            geo_node_list.append(i)
            new_glTF_node = hou.copyNodesTo(geo_node_list, geo_node)[0]
            GLTF = new_glTF_node.children()[0]
            wrang = new_glTF_node.createNode("attribwrangle", "Set_New_Material_Path")
            wrang.setFirstInput(GLTF)
            null_OUT = new_glTF_node.createNode('null', 'OUT')
            null_OUT.setFirstInput(wrang)
            null_OUT.setFirstInput(wrang)
			null_OUT.setDisplayFlag(True)
			null_OUT.setRenderFlag(True)
			null_OUT.setCurrent(True, clear_all_selected=True)
            new_glTF_node.layoutChildren()
    for j in sub_geo :
        mat_network_list = []
        if j.type().name() == 'matnet':
            mat_network_list.append(j)
            shds = j.children()
            new_shds = hou.copyNodesTo(shds, mat_context)
            
glTF_Loader.layoutChildren()
mat_context.layoutChildren()



# import hou
# #get selection class hou.SopNode
# sel = hou.selectedNodes()[0]

# #get selection class hou.Geometry
# geo = sel.geometry()

# #get currect network path
# network = sel.parent()

# #get value of shop_materialpatch
# shd_Prim_Name = geo.findPrimAttrib("shop_materialpath")
# value = shd_Prim_Name.strings()[0]
# #get only shader name
# shd_name = str(value.split("/")[-1])

# new_shd_attrib = 'setprimattrib(0, "shop_materialpath", @primnum, "/mat/' + shd_name + '","set");'


# #creat wrangler to apply new material patch
# wrang = network.createNode("attribwrangle", "Set_New_Material_Path")
# null_OUT = network.createNode('null', 'OUT')
# wrang.parm('class').set(1)
# wrang.parm('snippet').set(new_shd_attrib)
# wrang.setFirstInput(sel)
# null_OUT.setFirstInput(wrang)
# null_OUT.setDisplayFlag(True)
# null_OUT.setRenderFlag(True)
# null_OUT.setCurrent(True, clear_all_selected=True)
# network.layoutChildren()