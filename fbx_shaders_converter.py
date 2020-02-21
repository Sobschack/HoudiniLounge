import hou
import os

node = hou.pwd()

#Variable
fbx_texture_path = "/$HIP/geo/fbx/Textures/"
fbx_materials = hou.selectedNodes()[0]
fbx_materials_name = fbx_materials.name()
materials_list = hou.node('/mat').children()
current_materials_list = []

for i in materials_list:
        current_materials_list.append(i.name())

#get FBX shaders list
shaders = fbx_materials.children()

for shd in shaders:
    if not shd.name() in current_materials_list:
        #get texture name
        origin_texture_nodes = shd.glob('* ^suboutput')[0]
        origin_texture_path = origin_texture_nodes.evalParm('map1')
        origin_texture_name = str(origin_texture_path.split("\\")[-1])
        texture_path = os.path.join(fbx_texture_path,origin_texture_name)
        #create shader      
        mantraShader = hou.node('/mat').createNode('principledshader::2.0', shd.name())
        if origin_texture_name:
            mantraShader.parm('basecolor_useTexture').set(1)
            mantraShader.parm('basecolor_texture').set(texture_path)
        mantraShader.parm('rough').set(1)
        current_materials_list.append(shd.name())
        print "Material" +" "+current_materials_list[-1]+" "+"created"
    elif shd.name() in current_materials_list:
        print "Shader"+" "+shd.name()+" "+"still exist"
hou.node('/mat').layoutChildren()

#Apply new shaders
current_building = fbx_materials.parent()
my_network = current_building.allSubChildren()

mat_node_list = []
for node in my_network:
    if node.type().name() == 'material':
        num_materials = node.parm('num_materials')
        mat_node_list.append(node)
        if num_materials != None:
            mat_node = mat_node_list[0]
            mat_count = mat_node.parm("num_materials").eval()
            for i in range(mat_count):
                i = str(i+1)
                old_path = mat_node.parm("shop_materialpath"+i).eval()
                old_shd_name = old_path[-3:]
                mat_node.parm("shop_materialpath"+i).set("/mat/"+old_shd_name)