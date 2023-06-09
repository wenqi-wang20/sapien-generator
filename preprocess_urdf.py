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

    # 遍历所有 joint 元素
    for joint in root.iter('joint'):
        joint_limit = joint.find('limit')

        # 检查是否缺失 effort 属性
        if joint_limit is not None and 'effort' not in joint_limit.attrib:
            # 添加 effort 属性，默认值为 0.0
            joint_limit.attrib['effort'] = '0.0'
            # 添加 velocity 属性，默认值为 0.0
            joint_limit.attrib['velocity'] = '0.0'

    # 保存修改后的 URDF 文件
    tree.write(os.path.join(urdf_path, 'preprocess.urdf'))

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--urdf_path', type=str, default='./19179/')
    args = parser.parse_args()
    
    urdf_file = os.path.join(args.urdf_path, 'mobility.urdf')
    add_effort_attribute(urdf_file, args.urdf_path)
