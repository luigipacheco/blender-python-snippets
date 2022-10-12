# based on https://blender.stackexchange.com/questions/93051/align-to-face-normal-vector/276735#276735
import bpy
import mathutils
import bmesh

print("new")
C = bpy.context
cursor = C.scene.cursor
obj = C.active_object
mesh = obj.data
p = mesh.polygons
    
for i in p:
    print(i.index)
    obj.data.polygons.active = i.index
    p = obj.data.polygons
    normal = obj.data.polygons[p.active].normal
    center = obj.data.polygons[p.active].center

    #generate a quaternion rotation from the normal vector
    up = normal.to_track_quat('X', 'Y')

    #print(up)

    #set the cursor to the center location and rotate it to match the up vector
    cursor.location = center
    cursor.rotation_quaternion = up
    cursor.rotation_quaternion.to_euler()
    #get the object world matrix
    mat = obj.matrix_world

    #print(mat)
    #generate the location and rotation
    rot = cursor.rotation_quaternion.to_euler()
    #print(rot)
    loc = mat @ cursor.location.copy()

    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.ops.mesh.primitive_cube_add(location = loc, size = 0.1, rotation =rot)
    bpy.ops.object.empty_add(type='ARROWS',location = loc, rotation =rot)