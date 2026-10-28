import bpy
import math
import os
import sys
from mathutils import Vector

"""
EURO SOCIAL PC — mini générateur procédural de personnages.
Usage:
  blender -b -t 2 --python production/asset_generator.py -- --character kevin --out output/assets
Personnages disponibles: kevin, junior, maya.
Le générateur crée un .blend réutilisable et une image PNG de contrôle.
Ce prototype automatisable ne remplace pas encore un modèle sculpté/riggé professionnel.
"""

def cli_args():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    result = {"character": "kevin", "out": "output/assets", "size": "640"}
    i = 0
    while i < len(args):
        if args[i] in ("--character", "--out", "--size") and i + 1 < len(args):
            key = {"--character": "character", "--out": "out", "--size": "size"}[args[i]]
            result[key] = args[i + 1]
            i += 2
        else:
            i += 1
    return result

CFG = {
    "kevin": {
        "name": "Kévin — Le Boss", "skin": (0.34, 0.115, 0.052), "skin_hi": (0.48, 0.205, 0.095),
        "hair": (0.022, 0.012, 0.009), "top": (0.025, 0.035, 0.052), "accent": (1.0, 0.57, 0.025),
        "style": "afro", "hoodie": True, "cap": False, "glasses": False, "braids": False,
        "tagline": "LE BOSS"
    },
    "junior": {
        "name": "Junior — Algorithm", "skin": (0.27, 0.085, 0.038), "skin_hi": (0.42, 0.16, 0.075),
        "hair": (0.018, 0.012, 0.01), "top": (0.025, 0.16, 0.55), "accent": (0.05, 0.55, 1.0),
        "style": "short", "hoodie": False, "cap": True, "glasses": True, "braids": False,
        "tagline": "ALGORITHM"
    },
    "maya": {
        "name": "Maya — La Juge", "skin": (0.40, 0.18, 0.085), "skin_hi": (0.56, 0.29, 0.14),
        "hair": (0.025, 0.012, 0.016), "top": (0.72, 0.08, 0.32), "accent": (1.0, 0.62, 0.12),
        "style": "braids", "hoodie": False, "cap": False, "glasses": False, "braids": True,
        "tagline": "LA JUGE"
    }
}

def material(name, color, rough=0.58, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Roughness"].default_value = rough
    bs.inputs["Metallic"].default_value = metallic
    return m

def smooth(obj, mat):
    obj.data.materials.append(mat)
    if obj.type == "MESH":
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj

def ball(name, loc, scale, mat, segments=32, rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return smooth(o, mat)

def rounded_box(name, loc, scale, mat, bevel=0.12):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new("Arrondi doux", "BEVEL")
        mod.width = bevel
        mod.segments = 5
        o.modifiers.new("Normales pondérées", "WEIGHTED_NORMAL")
    return o

def line(name, coords, mat, thickness=0.025):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 16
    curve.bevel_depth = thickness
    curve.bevel_resolution = 4
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(coords)-1)
    for bp, co in zip(spline.bezier_points, coords):
        bp.co = co
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj

def text_obj(body, loc, size, mat, name):
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = body
    curve.size = size
    curve.extrude = 0.002
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.data.materials.append(mat)
    return obj

def build(character):
    c = CFG[character]
    skin = material("Peau | " + character, c["skin"])
    skin_hi = material("Lumière peau", c["skin_hi"])
    hair = material("Cheveux", c["hair"], 0.82)
    cloth = material("Tenue", c["top"], 0.78)
    accent = material("Accent identitaire", c["accent"], 0.42, 0.08)
    white = material("Blanc chaud", (0.96, 0.93, 0.86), 0.35)
    eye_dark = material("Iris et pupilles", (0.045, 0.018, 0.009), 0.25)
    mouth = material("Bouche", (0.075, 0.018, 0.018), 0.65)
    bg = material("Fond bleu pétrole", (0.018, 0.045, 0.075), 0.92)
    gold = material("Bijoux dorés", (0.95, 0.52, 0.06), 0.28, 0.55)

    # Corps, vêtements et cou.
    torso = ball("Silhouette vêtement", (0, 0.12, 1.25), (0.82, 0.48, 0.92), cloth)
    ball("Cou", (0, 0.0, 2.03), (0.27, 0.28, 0.32), skin)
    if c["hoodie"]:
        hood = ball("Capuche arrière", (0, 0.35, 2.10), (0.72, 0.38, 0.70), cloth)
        ball("Col", (0, -0.28, 1.94), (0.42, 0.19, 0.18), accent)
        for x in (-0.16, 0.16):
            line("Cordon", [(x,-0.42,1.94),(x*1.04,-0.46,1.67),(x*1.08,-0.44,1.48)], white, 0.018)
        if character == "kevin":
            line("Emblème couronne", [(-0.24,-0.45,1.22),(-0.22,-0.46,1.40),(-0.08,-0.46,1.31),(0,-0.46,1.46),(0.10,-0.46,1.31),(0.22,-0.46,1.40),(0.24,-0.45,1.22),(-0.24,-0.45,1.22)], accent, 0.035)
    else:
        rounded_box("Veste", (0, 0.12, 1.32), (1.52, 0.65, 1.18), cloth, 0.24)
        line("Liseré veste", [(0,-0.23,1.85),(0,-0.25,1.18),(0,-0.23,0.90)], accent, 0.025)

    # Bras stylisés, mains et jambes.
    for side in (-1, 1):
        arm = ball("Bras", (side*0.82, 0.03, 1.35), (0.23, 0.27, 0.65), cloth)
        arm.rotation_euler[1] = side * math.radians(17)
        ball("Main", (side*0.91, -0.06, 0.82), (0.22, 0.19, 0.22), skin_hi)
        ball("Jambe", (side*0.32, 0.12, 0.36), (0.24, 0.28, 0.48), cloth)
        ball("Basket", (side*0.34, -0.12, 0.10), (0.34, 0.43, 0.15), white)

    # Tête et oreilles : formes séparées mais douces.
    ball("Tête", (0, -0.04, 2.58), (0.70, 0.57, 0.83), skin, 48, 32)
    for side in (-1, 1):
        ball("Oreille", (side*0.68, -0.03, 2.56), (0.16, 0.15, 0.23), skin_hi)
        ball("Oreille intérieure", (side*0.72, -0.145, 2.56), (0.07, 0.035, 0.12), skin)
        x = side*0.255
        ball("Œil blanc", (x, -0.535, 2.70), (0.19, 0.085, 0.205), white)
        ball("Iris", (x+0.025, -0.612, 2.69), (0.095, 0.035, 0.12), eye_dark)
        ball("Reflet", (x+0.045, -0.644, 2.735), (0.028, 0.015, 0.034), white, 16, 12)
        brow = ball("Sourcil", (x, -0.535, 2.98), (0.22, 0.07, 0.055), hair)
        brow.rotation_euler[1] = -side*math.radians(10)
    ball("Nez", (0, -0.61, 2.47), (0.13, 0.17, 0.20), skin_hi)
    ball("Joue gauche", (-0.39,-0.44,2.39), (0.25,0.17,0.23), skin_hi)
    ball("Joue droite", (0.39,-0.44,2.39), (0.25,0.17,0.23), skin_hi)
    line("Sourire", [(-0.27,-0.58,2.29),(-0.14,-0.635,2.23),(0,-0.65,2.22),(0.16,-0.63,2.24),(0.28,-0.58,2.30)], mouth, 0.032)
    line("Lèvre", [(-0.12,-0.615,2.18),(0,-0.635,2.17),(0.12,-0.615,2.18)], skin_hi, 0.018)

    # Coiffure signature adaptée à chaque personnage.
    if c["style"] == "afro":
        ball("Volume afro", (0, 0.02, 3.28), (0.73, 0.55, 0.42), hair, 40, 28)
        for row, (z, count) in enumerate([(3.18, 9), (3.34, 9), (3.49, 7)]):
            for i in range(count):
                x = (i-(count-1)/2)*0.15
                y = -0.18 + (0.035 if i%2 else 0)
                ball("Boucle texturée", (x,y,z + (0.025 if (i+row)%2 else -0.015)), (0.12,0.13,0.14), hair, 20, 12)
    elif c["style"] == "short":
        ball("Cheveux courts", (0, 0.01, 3.22), (0.68, 0.53, 0.30), hair)
    else:
        ball("Chignon tressé", (0, 0.16, 3.30), (0.40,0.38,0.30), hair)
        for side in (-1, 1):
            for i in range(7):
                x = side*(0.42 + 0.035*(i%2))
                z = 3.15 - i*0.14
                ball("Tresse", (x,0.01,z), (0.085,0.10,0.13), hair, 20, 12)
        for i in range(5):
            ball("Tresse couronne", ((i-2)*0.18,-0.10,3.42), (0.11,0.12,0.12), hair, 20, 12)

    if c["cap"]:
        cap = ball("Casquette bleue", (0, -0.03, 3.37), (0.69,0.56,0.18), accent)
        rounded_box("Visière casquette", (0,-0.48,3.31), (0.76,0.36,0.07), accent, 0.08)
    if c["glasses"]:
        for side in (-1,1):
            frame = material("Monture lunettes", (0.012,0.014,0.02), 0.28, 0.15)
            ball("Lunette", (side*0.255,-0.625,2.70), (0.22,0.045,0.18), frame)
            ball("Verre", (side*0.255,-0.666,2.70), (0.175,0.022,0.135), material("Verre fumé", (0.06,0.10,0.13),0.2,0.2))
        line("Pont lunettes", [(-0.07,-0.66,2.72),(0,-0.69,2.74),(0.07,-0.66,2.72)], frame, 0.025)
    if character == "maya":
        for side in (-1,1):
            ball("Boucle oreille", (side*0.73,-0.14,2.35), (0.09,0.035,0.12), gold)

    # Fond et socle simple pour une fiche de personnage.
    rounded_box("Socle", (0,0.20,-0.06), (2.2,1.5,0.16), bg, 0.08)
    text_mat = material("Texte titre", (1.0,0.82,0.30), 0.45, 0.0)
    title = text_obj(c["name"].upper(), (-1.15,-0.70,3.86), 0.22, text_mat, "Titre de fiche")
    title.rotation_euler[0] = math.radians(90)

    # Sol studio.
    rounded_box("Plateau studio", (0,1.0,-0.20), (200,200,0.2), bg, 0.02)
    bpy.ops.object.camera_add(location=(4.2,-10.5,4.0))
    cam = bpy.context.object
    cam.rotation_euler = (Vector((0,0.0,1.92))-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 4.65
    scene = bpy.context.scene
    scene.camera = cam
    for loc, energy, color, size in [
        ((-4,-4,7), 850, (1.0,0.70,0.46), 4.5),
        ((4,1,5), 1100, (0.18,0.48,1.0), 3.0),
        ((0,-4,3.5), 320, (1.0,0.88,0.72), 4.0)
    ]:
        bpy.ops.object.light_add(type="AREA", location=loc)
        lamp = bpy.context.object
        lamp.data.energy = energy
        lamp.data.color = color
        lamp.data.shape = "DISK"
        lamp.data.size = size
        lamp.rotation_euler = (Vector((0,0,2.0))-lamp.location).to_track_quat("-Z","Y").to_euler()

    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 3
    scene.eevee.gtao_factor = 1.25
    scene.render.resolution_x = int(opts["size"])
    scene.render.resolution_y = int(int(opts["size"])*4/3)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    scene.world.color = (0.018,0.025,0.045)
    scene.render.filepath = os.path.join(opts["out"], character + "-character-sheet.png")
    scene.frame_end = 1
    scene.frame_set(1)
    return scene

opts = cli_args()
character = opts["character"].lower()
if character not in CFG:
    raise SystemExit("Personnage inconnu. Choisir: kevin, junior ou maya")
os.makedirs(opts["out"], exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = build(character)
blend_path = os.path.join(opts["out"], character + "-character.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
bpy.ops.render.render(write_still=True)
print("ASSET_GENERATOR_OK", character, blend_path, scene.render.filepath)
