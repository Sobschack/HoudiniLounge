import hou
#create global network instance
my_network = hou.node("/obj/").children()

#create /mat context instance
mat_context = hou.node("/mat")

#create exiting material list
exiting_shds = []
shaders = mat_context.children()
for i in shaders:
    exiting_shds.append(i.name())
# if exiting_shds:
#     print exiting_shds
# else:
#     print "Liste de shaders vide"

#create glTF loader subnetwork
glTF_Loader = hou.node('/obj').createNode('subnet', 'glTF_Loader')
glTF_Loader.moveToGoodPosition()

#create a list of all glTF hierarchy nodes in /obj
gltf_hierarchy_list = []
for nodes in my_network:
    if nodes.type().name() == 'gltf_hierarchy':
        gltf_hierarchy_list.append(nodes)

#create sub_geo for each glTF hierarchy in glTF_Loader
for nodes in gltf_hierarchy_list:
    #create subnet to host all gltf nodes in the glTF_Loader
    geo_node = glTF_Loader.createNode('subnet', nodes.name())
    #find and list all geo node in glTF hierarchy
    sub_geo = nodes.children()
    for i in sub_geo :
        geo_node_list = []
        if i.type().name() == 'geo':
            geo_node_list.append(i)
            new_glTF_node = hou.copyNodesTo(geo_node_list, geo_node)[0]
            GLTF = new_glTF_node.children()[0]
            #get selection class hou.Geometry to find an Attribute value
            geo = GLTF.geometry()
            shd_Prim_Name = geo.findPrimAttrib("shop_materialpath")
            value = shd_Prim_Name.strings()[0]
            #get only shader name
            shd_name = str(value.split("/")[-1])
            new_shd_primattrib = 'setprimattrib(0, "shop_materialpath", @primnum, "/mat/' + shd_name + '","set");'
            #create and set Rrim Wrangler to rename shop_materialpath attribute
            wrang = new_glTF_node.createNode("attribwrangle", "Set_New_Material_Path")
            wrang.parm('class').set(1)
            wrang.parm('snippet').set(new_shd_primattrib)
            wrang.setFirstInput(GLTF)
            #create normal node and set it to Face Area
            normal_node = new_glTF_node.createNode('normal', 'Normal_by_face')
            normal_node.setFirstInput(wrang)
            normal_node.parm('cuspangle').set(20)
            normal_node.parm('method').set(2)
            #create OUT null object, select and highlight it
            null_OUT = new_glTF_node.createNode('null', 'OUT')
            null_OUT.setFirstInput(normal_node)
            null_OUT.setDisplayFlag(True)
            null_OUT.setRenderFlag(True)
            null_OUT.setCurrent(True, clear_all_selected=True)
            new_glTF_node.layoutChildren()
    #Process material
    for j in sub_geo :
        mat_network_list = []
        if j.type().name() == 'matnet':
            mat_network_list.append(j)
            shds = j.children()
            shds_to_append = []
            for k in shds:
                if not k.name() in exiting_shds:
                 shds_to_append.append(k)
            new_shds = hou.copyNodesTo(shds_to_append, mat_context)
            
glTF_Loader.layoutChildren()
mat_context.layoutChildren()