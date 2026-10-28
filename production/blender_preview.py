import bpy
import math
from mathutils import Vector

# Preview 3D simple et reproductible, 10 secondes, 360x640.
# Les modèles sont des placeholders originaux : ils ne sont pas encore les assets finaux.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 360
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 120
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.world.color = (0.025, 0.025, 0.035)
scene.render.image_settings.color_depth = "8"
scene.render.film_transparent = False
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1

def material(name, color, roughness=0.8, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

sandwich_mat = material("Pain dore", (0.88, 0.53, 0.20))
lettuce_mat = material("Salade", (0.18, 0.52, 0.22))
shirt_blue = material("Tenue Junior bleu", (0.06, 0.28, 0.78))
shirt_red = material("Tenue Kevin rouge", (0.78, 0.10, 0.12))
shirt_yellow = material("Tenue Maya jaune", (0.96, 0.63, 0.08))
skin = material("Peau stylisee", (0.56, 0.31, 0.18))
dark = material("Lunettes et chaussures", (0.025, 0.025, 0.035), 0.35)
ground_mat = material("Sol de rue", (0.11, 0.14, 0.18))
wall_mat = material("Mur quartier", (0.28, 0.23, 0.21))
bottle_mat = material("Bouteille", (0.08, 0.42, 0.36), 0.25)
white = material("Blanc", (0.96, 0.94, 0.88))

def cube(name, loc, scale, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat: obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Bords doux", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        obj.modifiers.new("Normales", "WEIGHTED_NORMAL")
    return obj

def uv(name, loc, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj

# Sol et façade, construits autour du point de vue.
cube("Sol", (0, 0, -0.18), (12, 12, 0.3), ground_mat)
cube("Façade boutique", (0, 3.4, 2.0), (9, 0.3, 4.5), wall_mat)
cube("Enseigne", (0, 3.18, 3.35), (3.8, 0.08, 0.55), shirt_blue, 0.05)

# Sandwich vedette sur un petit support.
cube("Comptoir", (0, 0.55, 0.35), (3.6, 1.0, 0.25), dark, 0.06)
cube("Sandwich pain bas", (0, 0.15, 0.62), (1.2, 0.55, 0.18), sandwich_mat, 0.08)
cube("Sandwich salade", (0, 0.15, 0.75), (1.08, 0.48, 0.08), lettuce_mat, 0.03)
top = cube("Sandwich pain haut", (0, 0.15, 0.86), (1.18, 0.55, 0.18), sandwich_mat, 0.09)
top.rotation_euler[1] = math.radians(-5)

# Bouteille qui sert à la chute comique.
bottle = uv("Bouteille au sol", (0.78, -0.4, 0.10), (0.13, 0.34, 0.11), bottle_mat)
bottle.rotation_euler[1] = math.radians(80)

def character(name, x, y, shirt, z=0.0):
    body = uv(name + " corps", (x, y, z + 1.05), (0.38, 0.28, 0.58), shirt)
    head = uv(name + " tête", (x, y - 0.015, z + 1.78), (0.34, 0.32, 0.37), skin)
    # Cheveux / casquette sombre et yeux visibles depuis la caméra avant.
    uv(name + " cheveux", (x, y, z + 2.02), (0.35, 0.32, 0.18), dark)
    uv(name + " oeil gauche", (x - 0.12, y - 0.295, z + 1.81), (0.045, 0.035, 0.05), white)
    uv(name + " oeil droit", (x + 0.12, y - 0.295, z + 1.81), (0.045, 0.035, 0.05), white)
    for side in (-1, 1):
        arm = uv(name + " bras", (x + side * 0.43, y, z + 1.12), (0.13, 0.15, 0.40), shirt)
        arm.rotation_euler[1] = side * math.radians(18)
        leg = uv(name + " jambe", (x + side * 0.17, y, z + 0.42), (0.14, 0.16, 0.35), dark)
    return body, head

kevin_body, kevin_head = character("Kevin Le Boss", -1.35, -0.8, shirt_red)
junior_body, junior_head = character("Junior Algorithm", 1.35, -0.8, shirt_blue)
maya_body, maya_head = character("Maya La Juge", 0.0, -1.35, shirt_yellow)
# Lunettes iconiques de Junior.
cube("Lunettes Junior", (1.35, -1.105, 1.82), (0.48, 0.055, 0.11), dark, 0.02)

# Animation des personnages : approche du comptoir puis glissade légère de Kevin.
for obj in (kevin_body, kevin_head):
    obj.keyframe_insert(data_path="location", frame=1)
    obj.location.x += 0.48
    obj.keyframe_insert(data_path="location", frame=54)
    obj.location.z -= 0.55
    obj.rotation_euler.y = math.radians(65)
    obj.keyframe_insert(data_path="location", frame=78)
    obj.keyframe_insert(data_path="rotation_euler", frame=78)
for obj in (junior_body, junior_head):
    obj.keyframe_insert(data_path="location", frame=1)
    obj.location.x -= 0.4
    obj.keyframe_insert(data_path="location", frame=65)
for obj in (maya_body, maya_head):
    obj.keyframe_insert(data_path="location", frame=1)
    obj.location.z += 0.08
    obj.keyframe_insert(data_path="location", frame=100)

# Caméra portrait.
bpy.ops.object.camera_add(location=(0, -12.8, 5.4))
cam = bpy.context.object
cam.name = "Camera verticale"
target = Vector((0, 0.2, 1.15))
direction = target - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
cam.data.type = "ORTHO"
cam.data.ortho_scale = 7.8
scene.camera = cam
cam.data.lens = 50

# Éclairage doux.
bpy.ops.object.light_add(type="AREA", location=(-4, -5, 8))
key = bpy.context.object
key.name = "Lumière principale"
key.data.energy = 850
key.data.shape = "DISK"
key.data.size = 7
key.rotation_euler = (math.radians(25), 0, math.radians(-25))
bpy.ops.object.light_add(type="AREA", location=(4, 2, 6))
fill = bpy.context.object
fill.name = "Lumière de remplissage"
fill.data.energy = 500
fill.data.size = 5
fill.rotation_euler = (math.radians(20), 0, math.radians(150))

# Les clés d'animation sont interpolées de manière fluide.
for obj in scene.objects:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"

scene.render.filepath = "/tmp/euro_frames/frame_"
scene.camera.data.dof.use_dof = False
scene.render.image_settings.file_format = "PNG"
scene.render.resolution_percentage = 100
scene.frame_set(1)
bpy.ops.render.render(animation=True)
