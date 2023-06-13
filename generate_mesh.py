import urdfpy
import open3d as o3d
import trimesh
import random
import ipdb

import argparse
import os

from preprocess_urdf import add_effort_attribute


def get_link_by_name(urdf_data, link_name):
    for link in urdf_data.links:
        if link.name == link_name:
            return link
    return None

def apply_rotation_to_mesh(mesh, rotation_matrix, origin):
    # move to origin -> rotate -> move back
    origin_back = -origin[:3, 3]
    origin_move = origin[:3, 3]
    mesh.translate(origin_back)
    mesh.transform(rotation_matrix)
    mesh.translate(origin_move)
    
    return mesh  


def main(args):

    # load urdf file
    urdf_file = os.path.join(args.urdf_path, 'preprocess.urdf')
    urdf_data = urdfpy.URDF.load(urdf_file)

    meshes = []
    mesh_loaded = {}
    
    # load moveable meshes
    for joint in urdf_data.joints:
        if joint.joint_type == 'fixed':
            # pass if joint is fixed
            continue
        elif joint.joint_type == 'prismatic':
            # apply translation to the mesh
            children_link = get_link_by_name(urdf_data, joint.child)
            # random distance and fix it for every visual part
            axis = joint.axis
            distance = random.uniform(joint.limit.lower, joint.limit.upper)
            trans_matrix = trimesh.transformations.translation_matrix(distance * axis)
            
            for visual in children_link.visuals:
                mesh_file = os.path.join(args.urdf_path , visual.geometry.mesh.filename)
                mesh = o3d.io.read_triangle_mesh(mesh_file)
            
                mesh.translate(trans_matrix[:3, 3])
                meshes.append(mesh)
                mesh_loaded[mesh_file] = True
                              
        elif joint.joint_type == 'revolute':
            # apply rotation to the mesh
            children_link = get_link_by_name(urdf_data, joint.child)
            # random angle
            axis = joint.axis
            angle = random.uniform(joint.limit.lower, joint.limit.upper)
            rotate_matrix = trimesh.transformations.rotation_matrix(angle, axis)
            
            for visual in children_link.visuals:
                mesh_file = os.path.join(args.urdf_path , visual.geometry.mesh.filename)
                mesh = o3d.io.read_triangle_mesh(mesh_file)
                
                mesh = apply_rotation_to_mesh(mesh, rotate_matrix, joint.origin)
                meshes.append(mesh)
                mesh_loaded[mesh_file] = True
                
    # load remain meshes
    for link in urdf_data.links:
        for visual in link.visuals:
            mesh_file = os.path.join(args.urdf_path , visual.geometry.mesh.filename)
            if mesh_file in mesh_loaded:
                # pass if mesh is already loaded
                continue
            mesh = o3d.io.read_triangle_mesh(mesh_file)
            meshes.append(mesh)
            mesh_loaded[mesh_file] = True
                
    # merge all meshes
    merged_mesh = o3d.geometry.TriangleMesh()
    for mesh in meshes:
        merged_mesh += mesh

    # load all meshes
    meshes_all = []
    for link in urdf_data.links:
        for visual in link.visuals:
            mesh_file = os.path.join(args.urdf_path , visual.geometry.mesh.filename)
            mesh = o3d.io.read_triangle_mesh(mesh_file)
            meshes_all.append(mesh)
    all_shape = o3d.geometry.TriangleMesh()
    for shape in meshes_all:
        all_shape += shape

    # save to .obj
    obj_file = os.path.join(args.urdf_path, 'new_shape.obj')
    all_file = os.path.join(args.urdf_path, 'all_shape.obj')
    o3d.io.write_triangle_mesh(obj_file, merged_mesh)
    o3d.io.write_triangle_mesh(all_file, all_shape)
            
if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--urdf_path', type=str, default='./19179/')
    args = parser.parse_args()
    
    # preprocess urdf file
    original_urdf = os.path.join(args.urdf_path, 'mobility.urdf')
    add_effort_attribute(original_urdf, args.urdf_path)
    
    main(args)
    