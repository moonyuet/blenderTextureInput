bl_info ={
    "name": "Material Parameter",
    "author" : "Kayla Man",
    "version" : (1,0),
    "blender" : (2,91,0),
    "location" : " ",
    "description" : "importing textures",
    "warning": "", 
    "wiki_url": "",
    "category": "Material Parameter"
}

import bpy
from bpy.props import StringProperty, PointerProperty

class MaterialParamPanel(bpy.types.Panel):
    
    bl_label = "Texture Parameter"
    bl_idname = "MATERIAL_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Material Parameter"
    
    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        ma =ob.active_material
        row=layout.row()
        row.prop(ma.slot_setting, "diffuse")
        row=layout.row()
        row.prop(ma.slot_setting, "normal")
        row=layout.row()
        row.prop(ma.slot_setting, "rough")
        row=layout.row()
        row.prop(ma.slot_setting, "metallic") 
        row=layout.row()
        row.prop(ma.slot_setting, "height") 
         
def updateParam(self, context):
    
    mat = self.id_data
    node = mat.node_tree.nodes
    img = bpy.types.ShaderNodeTexImage
    nodes = [k for k in node
            if isinstance(k,img)]
                
    nodes[0].image = bpy.data.images.load(self.diffuse)
    nodes[1].image = bpy.data.images.load(self.normal)   
    nodes[2].image = bpy.data.images.load(self.rough)
    nodes[3].image = bpy.data.images.load(self.metallic)
    nodes[4].image = bpy.data.images.load(self.height)

class ParamSet(bpy.types.PropertyGroup):

    height: StringProperty(
            name="Height",
            subtype='FILE_PATH',
            update = updateParam) 
    normal: StringProperty(
            name="Normal",
            subtype='FILE_PATH',
            update = updateParam)
    diffuse: StringProperty(
            name="Diffuse",
            subtype='FILE_PATH',
            update = updateParam)
    metallic: StringProperty(
            name="Mtl",
            subtype='FILE_PATH',
            update = updateParam)
    rough : StringProperty(
            name="Rough",
            subtype='FILE_PATH',
            update = updateParam)
            
#disaplacement first, normal second, and other maps after


def register():
    bpy.utils.register_class(MaterialParamPanel)
    bpy.utils.register_class(ParamSet)
    bpy.types.Material.slot_setting=PointerProperty(type=ParamSet)


    
def unregister():
    bpy.utils.unregister_class(MaterialParamPanel)
    bpy.utils.unregister_class(ParamSet)
    del bpy.types.Material.slot_setting

if __name__ == "__main__":
    register()




