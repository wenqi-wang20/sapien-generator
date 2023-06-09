import xml.etree.ElementTree as ET
import urdfpy
import trimesh
import random
import ipdb

import argparse
import os

def add_effort_attribute(urdf_file, urdf_path):
    tree = ET.parse(urdf_file)
    root = tree.getroot()

    for joint in root.iter('joint'):
        joint_limit = joint.find('limit')

        if joint_limit is not None and 'effort' not in joint_limit.attrib:
            # add effort attribute, default value is 0.0
            joint_limit.attrib['effort'] = '0.0'
            # add velocity attribute, default value is 0.0
            joint_limit.attrib['velocity'] = '0.0'

    tree.write(os.path.join(urdf_path, 'preprocess.urdf'))

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--urdf_path', type=str, default='./19179/')
    args = parser.parse_args()
    
    urdf_file = os.path.join(args.urdf_path, 'mobility.urdf')
    add_effort_attribute(urdf_file, args.urdf_path)
