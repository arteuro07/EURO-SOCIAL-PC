import bpy
import math
from mathutils import Vector

# Prototype artistique Kévin — portrait 3D, 10 s, vertical 9:16.
# Il s'agit d'un test de direction artistique, pas encore d'un rig final.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.eevee.use_gtao = True
scene.eevee.gtao_distance = 3
scene.eevee.gtao_factor = 1.25
scene.render.resolution_x = 360
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 72
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.image_settings.color_depth = "8"
scene.render.film_transparent = False
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1
scene.world.color = (0.035, 0.045, 0.07)

def mat(name, color, rough=0.72, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Roughness"].default_value = rough
    bs.inputs["Metallic"].default_value = metallic
    return m

skin = mat("Peau brun chaud", (0.39, 0.17, 0.085), 0.58)
skin_light = mat("Lumière peau", (0.53, 0.27, 0.14), 0.58)
hair = mat("Cheveux brun très foncé", (0.035, 0.022, 0.018), 0.9)
hoodie = mat("Sweat noir charbon", (0.035, 0.045, 0.06), 0.9)
hoodie_edge = mat("Coutures gris doux", (0.19, 0.20, 0.22), 0.82)
white = mat("Blanc cassé", (0.93, 0.90, 0.82), 0.45)
iris = mat("Iris brun profond", (0.10, 0.045, 0.018), 0.35)
black = mat("Pupilles", (0.008, 0.006, 0.005), 0.25)
gold = mat("Couronne jaune", (1.0, 0.56, 0.035), 0.42, 0.15)
street = mat("Fond bleu nuit", (0.035, 0.09, 0.14), 0.9)
wall = mat("Façade chaude", (0.42, 0.19, 0.11), 0.9)
accent = mat("Accent turquoise", (0.02, 0.43, 0.48), 0.6)

def uv(name, loc, scale, material, seg=32, rings=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o

def cube(name, loc, scale, material, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel:
        mod = o.modifiers.new("Bords arrondis", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        o.modifiers.new("Normales douces", "WEIGHTED_NORMAL")
    return o

def curve_line(name, points, material, bevel=0.025):
    c = bpy.data.curves.new(name, "CURVE")
    c.dimensions = "3D"
    c.resolution_u = 16
    c.bevel_depth = bevel
    c.bevel_resolution = 4
    s = c.splines.new("POLY")
    s.points.add(len(points)-1)
    for p, co in zip(s.points, points):
        p.co = (*co, 1)
    o = bpy.data.objects.new(name, c)
    scene.collection.objects.link(o)
    o.data.materials.append(material)
    return o

# Rue stylisée : formes de bâtiments en arrière-plan pour donner de la profondeur.
cube("Sol", (0, 1.3, -0.25), (18, 12, 0.4), street, 0.05)
for i, x in enumerate([-4.3, -3.25, 3.25, 4.35]):
    h = [4.2, 5.4, 4.8, 5.8][i]
    b = cube("Bâtiment de rue", (x, 2.8, h/2-0.1), (1.45, 0.7, h), wall if i%2==0 else accent, 0.04)
    for z in [1.0, 2.0, 3.0, 4.0]:
        if z < h-0.3:
            cube("Fenêtre", (x, 2.42, z), (0.28, 0.05, 0.42), gold if i%2 else street, 0.025)
# Panneau flou en arrière-plan, comme une enseigne de quartier.
cube("Panneau arrière", (0, 3.0, 3.0), (2.8, 0.12, 1.1), hoodie, 0.12)

# Kévin : silhouette plus travaillée, gros yeux lisibles, boucles de cheveux, sweat à capuche.
torso = uv("Kévin - sweat", (0, 0.25, 1.55), (0.94, 0.48, 1.05), hoodie)
hood = uv("Capuche derrière tête", (0, 0.48, 2.28), (0.78, 0.38, 0.82), hoodie_edge)
head = uv("Kévin - visage", (0, -0.06, 2.58), (0.72, 0.58, 0.91), skin)
# Mâchoire et joues pour éviter la forme de simple boule.
uv("Joue gauche", (-0.42, -0.39, 2.35), (0.30, 0.25, 0.32), skin)
uv("Joue droite", (0.42, -0.39, 2.35), (0.30, 0.25, 0.32), skin)
uv("Oreille gauche", (-0.72, -0.03, 2.55), (0.17, 0.18, 0.27), skin_light)
uv("Oreille droite", (0.72, -0.03, 2.55), (0.17, 0.18, 0.27), skin_light)
# Nez.
uv("Nez", (0, -0.61, 2.46), (0.15, 0.19, 0.23), skin_light)
# Yeux, pupilles et sourcils orientés vers caméra.
for side in [-1, 1]:
    x = side * 0.275
    uv("Œil blanc", (x, -0.535, 2.72), (0.205, 0.095, 0.22), white)
    uv("Iris", (x + 0.025, -0.622, 2.71), (0.105, 0.045, 0.13), iris)
    uv("Pupille", (x + 0.035, -0.662, 2.71), (0.052, 0.025, 0.075), black)
    uv("Reflet œil", (x + 0.055, -0.685, 2.765), (0.025, 0.014, 0.03), white, 16, 12)
    brow = uv("Sourcil expressif", (x, -0.55, 3.00), (0.25, 0.085, 0.07), hair)
    brow.rotation_euler[1] = -side * math.radians(8)
# Sourire incurvé en segments, légèrement asymétrique.
curve_line("Sourire en coin", [(-0.30,-0.594,2.27),(-0.20,-0.64,2.22),(0,-0.66,2.20),(0.19,-0.63,2.23),(0.31,-0.58,2.30)], hair, 0.035)
# Lèvre inférieure.
curve_line("Lèvre inférieure", [(-0.14,-0.625,2.17),(0,-0.65,2.155),(0.14,-0.62,2.17)], skin_light, 0.022)

# Boucles afro : volume principal + boucles individuelles irrégulières.
uv("Afro principal", (0, 0.02, 3.35), (0.77, 0.58, 0.48), hair)
for row, (z, count, radius) in enumerate([(3.25, 9, 0.16), (3.43, 8, 0.17), (3.58, 6, 0.16)]):
    for i in range(count):
        x = (i-(count-1)/2)*0.17
        depth = -0.18 + (0.05 if i%2 else 0)
        uv("Boucle afro", (x, depth, z + (0.035 if (i+row)%2 else -0.02)), (radius, 0.16, radius*1.05), hair, 20, 12)

# Bras, poignets, mains et jambes.
left_arm = uv("Bras gauche", (-0.93, 0.10, 1.62), (0.24, 0.28, 0.66), hoodie)
left_arm.rotation_euler[1] = math.radians(-20)
right_arm = uv("Bras droit", (0.91, -0.02, 1.67), (0.24, 0.27, 0.68), hoodie)
right_arm.rotation_euler[1] = math.radians(20)
uv("Main gauche", (-1.02, -0.12, 1.12), (0.20, 0.17, 0.22), skin)
uv("Main droite", (1.0, -0.16, 1.18), (0.20, 0.17, 0.22), skin)
for side in [-1, 1]:
    uv("Jambe", (side*0.36, 0.22, 0.45), (0.27, 0.31, 0.53), hoodie)
    shoe = uv("Basket", (side*0.38, -0.01, 0.13), (0.34, 0.46, 0.16), white)
# Capuche autour du cou et cordons blancs.
uv("Col du sweat", (0, -0.30, 1.99), (0.48, 0.20, 0.20), hoodie_edge)
for x in [-0.19, 0.19]:
    curve_line("Cordon du sweat", [(x,-0.49,1.98),(x*1.05,-0.51,1.73),(x*1.10,-0.50,1.48)], white, 0.018)
# Logo couronne sur la poitrine.
curve_line("Couronne du logo", [(-0.23,-0.49,1.35),(-0.22,-0.50,1.52),(-0.08,-0.50,1.42),(0,-0.50,1.57),(0.10,-0.50,1.42),(0.22,-0.50,1.52),(0.23,-0.49,1.35),(-0.23,-0.49,1.35)], gold, 0.025)

# Petite animation d'expression : mouvement du corps, inclinaison de tête et haussement des épaules.
for frame, tilt, z in [(1, 0.0, 0.0), (18, -0.04, 0.04), (36, 0.05, 0.0), (54, -0.025, 0.03), (72, 0.0, 0.0)]:
    head.rotation_euler[1] = tilt
    head.location.z = 2.58 + z
    head.keyframe_insert(data_path="rotation_euler", frame=frame)
    head.keyframe_insert(data_path="location", frame=frame)
for frame, angle in [(1,0), (18,math.radians(-7)), (36,math.radians(5)), (54,math.radians(-4)), (72,0)]:
    torso.rotation_euler[1] = angle
    torso.keyframe_insert(data_path="rotation_euler", frame=frame)
# Camera portrait rapprochée, léger mouvement vers le visage.
bpy.ops.object.camera_add(location=(3.4, -10.8, 4.15))
cam = bpy.context.object
cam.name = "Caméra portrait Kévin"
target = Vector((0, 0.05, 2.05))
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.type = "ORTHO"
cam.data.ortho_scale = 4.9
scene.camera = cam
cam.location.x = 3.4
cam.keyframe_insert(data_path="location", frame=1)
cam.location.x = 2.9
cam.keyframe_insert(data_path="location", frame=72)
cam.data.lens = 50

# Éclairage cinématique chaud/froid.
bpy.ops.object.light_add(type="AREA", location=(-4.0, -4.5, 7.0))
key = bpy.context.object
key.data.energy = 950
key.data.shape = "DISK"
key.data.size = 5
key.rotation_euler = (math.radians(25), 0, math.radians(-25))
bpy.ops.object.light_add(type="AREA", location=(4.0, 1.0, 5.0))
rim = bpy.context.object
rim.data.energy = 1100
rim.data.color = (0.15, 0.55, 1.0)
rim.data.size = 3
rim.rotation_euler = (math.radians(25), 0, math.radians(150))
bpy.ops.object.light_add(type="AREA", location=(0, -4.0, 3.4))
fill = bpy.context.object
fill.data.energy = 240
fill.data.size = 4
fill.rotation_euler = (0, 0, 0)

# Lissage des interpolations d'animation.
for obj in scene.objects:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
scene.render.filepath = "/tmp/euro_frames/frame_"
scene.camera.data.dof.use_dof = False
scene.frame_set(1)
bpy.ops.render.render(animation=True)
