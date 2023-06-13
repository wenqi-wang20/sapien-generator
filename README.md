## Sapien PartNet dataset generator

See [PartNet-Mobility Dataset](https://sapien.ucsd.edu/browse) for details of dataset.

The repository use `urdfpy` and `trimesh` to sample the **mobility status** to generate the all-in-one mesh, and we provide two samples.

#### Environment
The generator runs in the environment of `python=3.7.12`. Install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
```

#### Generate
```bash
python generate_mesh.py --urdf_path=./12085
```

![center](./image/rotation.png)
![center](./image/translation.png)
![center](./image/translation2.png)