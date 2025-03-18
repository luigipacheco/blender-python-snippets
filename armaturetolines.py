import bpy
import bmesh

def create_bone_lines(armature_name, mesh_name="Bone_Lines"):
    # Get the armature object
    armature = bpy.data.objects.get(armature_name)
    if not armature or armature.type != 'ARMATURE':
        print("Armature not found or invalid.")
        return

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(mesh_name, mesh)
    
    # Link the new object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh for the new mesh
    bm = bmesh.new()

    # Store vertex groups for later parenting
    vertex_groups = {}

    # Go through each bone in the armature
    for bone in armature.data.bones:
        head = bone.head_local
        tail = bone.tail_local

        # Create two vertices at the bone's head and tail
        v1 = bm.verts.new(head)
        v2 = bm.verts.new(tail)

        # Connect them with an edge to form a line
        bm.edges.new((v1, v2))

        # Ensure the armature modifier works properly
        obj.vertex_groups.new(name=bone.name)
        vertex_groups[bone.name] = obj.vertex_groups[bone.name]

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Parent the new mesh to the armature
    obj.parent = armature

    # Add an armature modifier to bind it to the skeleton
    mod = obj.modifiers.new(name="Armature", type='ARMATURE')
    mod.object = armature

    # Assign each vertex to the correct bone
    mesh.update()
    for vert in obj.data.vertices:
        closest_bone = min(armature.data.bones, key=lambda b: (b.head_local - vert.co).length)
        vertex_groups[closest_bone.name].add([vert.index], 1.0, 'REPLACE')

    print("Bone lines created and parented!")

# Run the function with the name of your armature
create_bone_lines("Armature")
