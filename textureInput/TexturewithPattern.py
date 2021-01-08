bl_info ={
    "name": "Material Creation",
    "author" : "Kayla Man",
    "version" : (1,0),
    "blender" : (2,91,0),
    "location" : " ",
    "description" : "importing textures into PBR Shader",
    "warning": "", 
    "wiki_url": "",
    "category": "Texture Input"
}
import bpy
from bpy.props import StringProperty, FloatVectorProperty, FloatProperty, PointerProperty

class MaterialTexturePanel(bpy.types.Panel):
    
    bl_label = "PBR Shader Add-on"
    bl_idname = "MATERIAL_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Material Creation"
    
    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        ma =ob.active_material
        row=layout.row()
        row.operator("shader.pbrpat_operator")
        row=layout.row()
        layout.prop(ma, "name")
       
        row=layout.row()
        row.prop(ma.slot_setting, "height")
        row=layout.row()
        row.prop(ma.slot_setting, "normal")
        row=layout.row()
        row.prop(ma.slot_setting, "diffuse")
        row=layout.row()
        row.prop(ma.slot_setting, "metallic")
        row=layout.row()
        row.prop(ma.slot_setting, "rough") 
        row=layout.row()
        row.prop(ma.slot_setting, "pattern")  
        row=layout.row()
        row.prop(ma.slot_setting, "col") 
        row=layout.row()
        row.prop(ma.slot_setting, "size") 
       
class PBR_SHADER(bpy.types.Operator):
    
    bl_label = "PBR_PATTERN"
    bl_idname = "shader.pbrpat_operator"

    def execute(self,context):
         
        activeObject = bpy.context.active_object
        mat_pbr = bpy.data.materials.new(name="PBR Shader")
        mat_pbr.use_nodes = True
        activeObject.data.materials.append(mat_pbr)
        
        bsdf = mat_pbr.node_tree.nodes.get("Principled BSDF")
        
        #normal map
        nrm_node = mat_pbr.node_tree.nodes.new("ShaderNodeNormalMap")
        nrm_tex = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")
        mat_pbr.node_tree.links.new(nrm_tex.outputs[0],nrm_node.inputs[1])
        mat_pbr.node_tree.links.new (nrm_node.outputs[0], bsdf.inputs[19])

        #disaplacement map
        mat_output = mat_pbr.node_tree.nodes.get("Material Output")
        disp_node = mat_pbr.node_tree.nodes.new("ShaderNodeDisplacement")
        disp_tex = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")
        mat_pbr.node_tree.links.new(disp_tex.outputs[0], disp_node.inputs[0])
        mat_pbr.node_tree.links.new(disp_node.outputs[0],mat_output.inputs[2])

        #Mix node for placing pattern
        post_mix = mat_pbr.node_tree.nodes.new("ShaderNodeMixRGB")

        #Mix node for recoloring 
        col_mix = mat_pbr.node_tree.nodes.new("ShaderNodeMixRGB")
        col_mix.use_clamp = True
        col_mix.blend_type = "ADD"

        #diffuse map
        dif_tex = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")
       
        #pattern map
        pat_tex = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")

        #RGB node (for recoloring)
        rgb_node = mat_pbr.node_tree.nodes.new("ShaderNodeRGB")
        
        #mapping and texture coordinate 
        map_node = mat_pbr.node_tree.nodes.new("ShaderNodeMapping")
        map_node.vector_type = 'TEXTURE'
        text_coord = mat_pbr.node_tree.nodes.new("ShaderNodeTexCoord")
        mat_pbr.node_tree.links.new (text_coord.outputs[2], map_node.inputs[0])
        mat_pbr.node_tree.links.new (map_node.outputs[0], pat_tex.inputs[0])

        mat_pbr.node_tree.links.new(pat_tex.outputs[1], col_mix.inputs[1])
        mat_pbr.node_tree.links.new(dif_tex.outputs[0], col_mix.inputs[2])
       

        mat_pbr.node_tree.links.new(pat_tex.outputs[1], post_mix.inputs[0])
        mat_pbr.node_tree.links.new(col_mix.outputs[0], post_mix.inputs[1])
        mat_pbr.node_tree.links.new(rgb_node.outputs[0],post_mix.inputs[2])

        mat_pbr.node_tree.links.new(post_mix.outputs[0],bsdf.inputs[0])
        
        #metallic map
        mtl_tex = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")
        mat_pbr.node_tree.links.new(mtl_tex.outputs[0], bsdf.inputs[4])

        #roughness map
        rough_tex = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")
        mat_pbr.node_tree.links.new(rough_tex.outputs[0], bsdf.inputs[7])

        return {'FINISHED'}


def updateMaterial(self, context):
    
    mat = self.id_data
    node = mat.node_tree.nodes
    img = bpy.types.ShaderNodeTexImage
    nodes = [k for k in node
            if isinstance(k,img)]
                
    nodes[0].image = bpy.data.images.load(self.normal)
    nodes[1].image = bpy.data.images.load(self.height)   
    nodes[2].image = bpy.data.images.load(self.diffuse)
    nodes[3].image = bpy.data.images.load(self.pattern)
    nodes[4].image = bpy.data.images.load(self.metallic)
    nodes[5].image = bpy.data.images.load(self.rough)

def updateCol(self, context):
        mat = self.id_data
        node = mat.node_tree.nodes
        rgb = bpy.types.ShaderNodeRGB
        nodes = [k for k in node
                if isinstance(k,rgb)]
        
        for k in nodes:
                k.outputs[0].default_value = self.col

def updateRepeat(self, context):
        mat = self.id_data
        node = mat.node_tree.nodes
        coord = bpy.types.ShaderNodeMapping
        nodes = [s for s in node
                if isinstance (s, coord)]
        for s in nodes:
                s.inputs[3].default_value[0] = self.size
                s.inputs[3].default_value[1] = self.size
        


#update coordx, y
#update color

class materialSet(bpy.types.PropertyGroup):

    height: StringProperty(
            name="Height",
            subtype='FILE_PATH',
            update = updateMaterial) 

    normal: StringProperty(
            name="Normal",
            subtype='FILE_PATH',
            update = updateMaterial)
    diffuse: StringProperty(
            name="Diffuse",
            subtype='FILE_PATH',
            update = updateMaterial)
    pattern: StringProperty(
            name="Pattern",
            subtype='FILE_PATH',
            update = updateMaterial)
    metallic: StringProperty(
            name="Mtl",
            subtype='FILE_PATH',
            update = updateMaterial)
    rough : StringProperty(
            name="Rough",
            subtype='FILE_PATH',
            update = updateMaterial)
    col: FloatVectorProperty(
            name="BaseColor",
            subtype='COLOR',
            size = 4,
            min = 0.0,
            max = 1.0,
            default=(1,1,1,1),
            update = updateCol)
    size: FloatProperty(
            name="Pattern Scale",
            subtype='NONE',
            default=0.0,
            min=0, max=1,
            update = updateRepeat) 


    #color 
    #float param for coord x, y


def register():
    bpy.utils.register_class(MaterialTexturePanel)
    bpy.utils.register_class(PBR_SHADER)
    bpy.utils.register_class(materialSet)
    bpy.types.Material.slot_setting=PointerProperty(type=materialSet)
    
def unregister():
    bpy.utils.unregister_class(MaterialTexturePanel)
    bpy.utils.unregister_class(PBR_SHADER)
    bpy.utils.unregister_class(materialSet)
    del bpy.types.Material.slot_setting

if __name__ == "__main__":
    register()




