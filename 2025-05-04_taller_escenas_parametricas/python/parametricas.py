import os
import argparse
import numpy as np
import pandas as pd


try:
    from vedo import Sphere, Cube, Cylinder, Assembly, Plotter
    import vedo
except ImportError:
    vedo = None

try:
    import trimesh
    from trimesh.scene import Scene
    from trimesh.exchange.export import export_mesh
except ImportError:
    trimesh = None

try:
    import open3d as o3d
except ImportError:
    o3d = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "resultados_modificados")
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_points(path):
    if os.path.exists(path):
        try:
            if path.lower().endswith('.csv'):
                df = pd.read_csv(path)
            else:
                df = pd.read_json(path)
            return df[['x','y','z']].values
        except Exception as e:
            print(f"Warning: failed to load '{path}' ({e}), generating random points.")
    return np.random.uniform(-2, 2, size=(18, 3))

def save_points(points, path):
    df = pd.DataFrame(points, columns=['x', 'y', 'z'])
    if path.lower().endswith('.csv'):
        df.to_csv(path, index=False)
    else:
        df.to_json(path, orient='records', indent=2)
    print(f"Saved points to {path}")

def demo_vedo(points, output_prefix):
    if vedo is None:
        print("vedo library not installed, skipping vedo demo.")
        return
    objects = []
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33F3', '#33FFF3']
    
    for i, (x, y, z) in enumerate(points):
        shape_type = i % 3
        scaling_factor = 0.08 + abs(np.sin(i * 0.4)) * 0.2
        
        if shape_type == 0:
            obj = Sphere(pos=(x, y, z), r=scaling_factor, c=colors[i % len(colors)], res=12)
        elif shape_type == 1:
            obj = Cube(pos=(x, y, z), side=scaling_factor*1.5, c=colors[i % len(colors)])
        else:
            height_factor = 0.5 + np.cos(i * 0.3) * 0.5
            obj = Cylinder(pos=(x, y, z), r=scaling_factor*0.7, height=scaling_factor*2*height_factor, 
                         c=colors[i % len(colors)], res=12)
        
        objects.append(obj)
    
    scene = Assembly(objects)
    plt = Plotter(title='Simple Geometric Distribution')
    plt.show(scene, "Press any key to continue...")
    for ext in ['.obj', '.stl', '.glb']:
        out = os.path.join(RESULTS_DIR, f"{output_prefix}_vedo{ext}")
        scene.write(out)
        print(f"vedo scene exported to {out}")


def demo_trimesh(points, output_prefix):
    """
    Generate trimesh primitives, combine into a Scene, export as GLB, and individual OBJ/STL.
    """
    if trimesh is None:
        print("trimesh library not installed, skipping trimesh demo.")
        return
    meshes = []
    
    for i, (x, y, z) in enumerate(points):
        shape_type = (i + 2) % 3  # Different offset from vedo distribution
        radius = 0.1 + 0.15 * np.cos(i * 0.5 + 1)
        
        if shape_type == 0:
            m = trimesh.creation.icosphere(subdivisions=i % 3 + 1, radius=radius)
        elif shape_type == 1:
            box_size = radius * 1.8
            m = trimesh.creation.box(extents=[box_size*0.8, box_size*1.2, box_size])
        else:
            height = radius * (2.5 + np.sin(i))
            m = trimesh.creation.cylinder(radius=radius*0.9, height=height)
        
        m.apply_translation([x, y, z])
        
        # Create gradient colors based on position
        brightness = 0.5 + 0.5 * np.sin(i * 0.5)
        color_value = int(brightness * 255)
        colors = [
            [color_value, 100, 255-color_value, 255],
            [255-color_value, color_value, 100, 255],
            [100, 255-color_value, color_value, 255]
        ]
        m.visual.vertex_colors = colors[shape_type]
        
        meshes.append(m)
    
    scene = Scene(meshes)
    for ext, ftype in [('.obj','obj'),('.stl','stl'),('.glb','glb')]:
        out = os.path.join(RESULTS_DIR, f"{output_prefix}_trimesh{ext}")
        export_mesh(scene, out, file_type=ftype)
        print(f"trimesh scene exported to {out}")
    for idx, mesh in enumerate(meshes[:3]):
        for ext, ftype in [('.obj','obj'),('.stl','stl')]:
            out = os.path.join(RESULTS_DIR, f"{output_prefix}_object_{idx}{ext}")
            export_mesh(mesh, out, file_type=ftype)
            print(f"  - object {idx} exported to {out}")


def demo_open3d(points, output_prefix):
    """
    Generate open3d primitives, merge into one mesh, display and export as PLY/OBJ/STL.
    """
    if o3d is None:
        print("open3d library not installed, skipping open3d demo.")
        return
    mesh_list = []
    
    for i, (x, y, z) in enumerate(points):
        shape_type = (i + 1) % 3  # Different offset from other distributions
        size = 0.12 + 0.1 * abs(np.sin(i * 0.25))
        position_factor = np.sqrt(x*x + y*y + z*z) / 3
        
        if shape_type == 0:
            mesh = o3d.geometry.TriangleMesh.create_sphere(radius=size)
        elif shape_type == 1:
            w_factor = 0.8 + 0.4 * np.sin(i * 0.7)
            h_factor = 0.8 + 0.4 * np.cos(i * 0.7)
            mesh = o3d.geometry.TriangleMesh.create_box(width=size*w_factor, height=size*h_factor, depth=size)
        else:
            cylinder_height = size * (2 + np.sin(i * 0.5))
            mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=size*0.7, height=cylinder_height)
        
        mesh.translate((x, y, z))
        
        # Create color based on position and shape type
        red = 0.3 + 0.7 * (1 if shape_type == 0 else position_factor)
        green = 0.3 + 0.7 * (1 if shape_type == 1 else position_factor)
        blue = 0.3 + 0.7 * (1 if shape_type == 2 else position_factor)
        
        mesh.paint_uniform_color([red, green, blue])
        mesh.compute_vertex_normals()
        mesh_list.append(mesh)
    
    combined = mesh_list[0]
    for m in mesh_list[1:]:
        combined += m
    
    o3d.visualization.draw_geometries([combined], window_name='Basic Shapes Pattern')
    for ext in ['.obj', '.stl', '.ply']:
        out = os.path.join(RESULTS_DIR, f"{output_prefix}_open3d{ext}")
        o3d.io.write_triangle_mesh(out, combined)
        print(f"open3d mesh exported to {out}")


def main():
    parser = argparse.ArgumentParser(description='Parametric 3D Scene Generation Demo')
    parser.add_argument('-i', '--input', default='points.csv', help='CSV or JSON input file with x,y,z')
    parser.add_argument('-e', '--export-data', help='Path to export loaded/generated points to CSV or JSON')
    parser.add_argument('-b', '--backend', choices=['vedo', 'trimesh', 'open3d', 'all'], default='all', help='Which backend to run')
    parser.add_argument('-o', '--output-prefix', default='basic_shapes', help='Output filename prefix')
    args = parser.parse_args()

    # sanitize prefix to avoid nested folders
    prefix = os.path.basename(args.output_prefix)
    if not prefix:
        prefix = args.output_prefix

    points = load_points(args.input)
    if args.export_data:
        save_points(points, args.export_data)
    # Run selected backends using sanitized prefix
    if args.backend in ('vedo', 'all'):
        demo_vedo(points, prefix)
    if args.backend in ('trimesh', 'all'):
        demo_trimesh(points, prefix)
    if args.backend in ('open3d', 'all'):
        demo_open3d(points, prefix)

if __name__ == '__main__':
    main()