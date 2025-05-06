import numpy as np
import trimesh
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors

class ModelProcessor:
    """Clase principal para procesar modelos 3D"""
    
    def __init__(self):
        self.input_dir = Path('C:/Users/Usuario/Desktop/7Semestre/Visual/computacion-visual-Daniel/2025-05-04_taller_conversion_formatos_3d/datos')
        self.output_dir = Path('C:/Users/Usuario/Desktop/7Semestre/Visual/computacion-visual-Daniel/2025-05-04_taller_conversion_formatos_3d/Capturas/python')
        self.supported_formats = ['.obj', '.stl', '.glb', '.gltf']
        self.supported_formats = ['.obj', '.stl', '.glb', '.gltf']
        self.enable_visualization = True
        # Límites para la visualización detallada
        self.max_faces_detailed = 10000  # Máximo de caras para visualización detallada
        
    def _ensure_dirs_exist(self):
        """Crear directorios de salida si no existen"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_all_models(self):
        """Importar todos los modelos del directorio de entrada"""
        print(f"Buscando modelos en: {self.input_dir}")
        self.models = []
        self.filenames = []
        
        if not self.input_dir.exists():
            print(f"Error: No se encontró el directorio {self.input_dir}")
            print(f"Creando directorio {self.input_dir}...")
            self.input_dir.mkdir(parents=True, exist_ok=True)
            print(f"Coloca tus modelos 3D en {self.input_dir.absolute()} y ejecuta el programa nuevamente")
            return [], []
            
        for file_path in self.input_dir.iterdir():
            if file_path.suffix.lower() in self.supported_formats:
                try:
                    model = trimesh.load(str(file_path))
                    self.models.append(model)
                    self.filenames.append(file_path.name)
                    print(f"Importado: {file_path.name}")
                except Exception as e:
                    print(f"Error al importar {file_path.name}: {e}")
        
        print(f"Total modelos importados: {len(self.models)}")
        return self.models, self.filenames
    
    def process_model(self, model, name):
        """Procesa un modelo individual y retorna estadísticas"""
        print(f"\n== Procesando modelo: {name} ==")
        
        # Combinar geometrías para escenas
        if isinstance(model, trimesh.Scene):
            if not model.geometry:
                print("  Atención: Escena sin geometrías")
                return None
            processed = trimesh.util.concatenate([mesh for mesh in model.geometry.values()])
        else:
            processed = model
            
        # Información básica
        stats = {
            "vértices": len(processed.vertices),
            "caras": len(processed.faces),
            "cerrado": processed.is_watertight,
            "bbox": processed.bounding_box.extents
        }
        
        # Verificar normales
        try:
            _ = processed.vertex_normals
            stats["normales"] = True
        except:
            stats["normales"] = False
            
        # Calcular vértices únicos
        unique_verts = np.unique(processed.vertices, axis=0)
        stats["duplicados"] = len(processed.vertices) - len(unique_verts)
        stats["porcentaje_duplicados"] = stats["duplicados"] / len(processed.vertices) * 100 if len(processed.vertices) > 0 else 0
        
        # Calcular volumen si es posible
        if processed.is_volume:
            stats["volumen"] = processed.volume
            
        # Mostrar estadísticas
        print(f"  Vértices: {stats['vértices']}")
        print(f"  Caras: {stats['caras']}")
        print(f"  Normales: {'Presentes' if stats['normales'] else 'Ausentes'}")
        print(f"  Watertight: {'Sí' if stats['cerrado'] else 'No'}")
        
        if stats["duplicados"] > 0:
            print(f"  Vértices duplicados: {stats['duplicados']} ({stats['porcentaje_duplicados']:.2f}%)")
        else:
            print("  Sin vértices duplicados")
            
        print(f"  Dimensiones: {stats['bbox']}")
        
        if "volumen" in stats:
            print(f"  Volumen: {stats['volumen']:.3f}")
            
        # Visualizar el modelo si está habilitado
        if self.enable_visualization:
            self.visualize_model(processed, name)
            
        return processed
    
    def visualize_model(self, model, name):
        """Visualiza el modelo usando matplotlib y guarda capturas"""
        print(f"  Generando visualización para: {name}")
        
        # Crear directorio de salida si no existe
        self.output_dir.mkdir(parents=True, exist_ok=True)
        vis_dir = self.output_dir / "visualizaciones"
        vis_dir.mkdir(exist_ok=True)
        print(f"  Directorio de visualizaciones: {vis_dir}")
        
        # Verificar que el modelo tenga datos
        if not hasattr(model, 'vertices') or len(model.vertices) == 0:
            print("  Error: Modelo sin vértices")
            return
            
        # Crear visualización simplificada
        try:
            # Extraer datos básicos
            verts = model.vertices
            base_name = Path(name).stem
            
            # Crear figura
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Configurar límites de visualización
            center = model.centroid
            max_dim = max(model.extents)
            ax.set_xlim(center[0] - max_dim/2, center[0] + max_dim/2)
            ax.set_ylim(center[1] - max_dim/2, center[1] + max_dim/2)
            ax.set_zlim(center[2] - max_dim/2, center[2] + max_dim/2)
            
            # Para modelos grandes, mostrar solo puntos
            if len(model.faces) > self.max_faces_detailed:
                print(f"  Modelo complejo ({len(model.faces)} caras). Mostrando puntos.")
                # Muestreo de puntos para visualización
                n_points = min(5000, len(verts))
                indices = np.random.choice(len(verts), n_points, replace=False)
                sampled_verts = verts[indices]
                
                # Visualizar puntos
                ax.scatter(
                    sampled_verts[:, 0],
                    sampled_verts[:, 1],
                    sampled_verts[:, 2],
                    c='blue', s=1, alpha=0.5
                )
                
                # Añadir caja delimitadora
                bbox = model.bounding_box
                corners = bbox.vertices
                
                # Definir las aristas de un cubo
                edges = [
                    (0, 1), (1, 3), (3, 2), (2, 0),  # base inferior
                    (4, 5), (5, 7), (7, 6), (6, 4),  # base superior
                    (0, 4), (1, 5), (2, 6), (3, 7)   # conexiones
                ]
                
                # Dibujar aristas
                for edge in edges:
                    ax.plot3D(
                        [corners[edge[0]][0], corners[edge[1]][0]],
                        [corners[edge[0]][1], corners[edge[1]][1]],
                        [corners[edge[0]][2], corners[edge[1]][2]],
                        'red', linewidth=1
                    )
            else:
                # Para modelos más pequeños, muestra algunas caras
                print(f"  Mostrando modelo con {min(1000, len(model.faces))} caras.")
                # Muestrear caras para la visualización
                n_faces = min(1000, len(model.faces))
                indices = np.random.choice(len(model.faces), n_faces, replace=False)
                faces_sample = model.faces[indices]
                
                # Crear colección de triángulos
                triangles = []
                for face in faces_sample:
                    triangle = [verts[i] for i in face]
                    triangles.append(triangle)
                
                # Asignar colores
                face_colors = np.random.rand(len(triangles), 3) * 0.7 + 0.3
                
                # Dibujar malla
                mesh = plt.art3d.Poly3DCollection(
                    triangles,
                    facecolors=face_colors,
                    linewidths=0.1,
                    alpha=0.8
                )
                ax.add_collection3d(mesh)
            
            # Configuración final y guardado
            ax.set_title(f'Modelo: {base_name}')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            
            # Guardar figura
            output_path = vis_dir / f"{base_name}_vista.png"
            print(f"  Guardando imagen en: {output_path}")
            plt.tight_layout()
            plt.savefig(str(output_path), dpi=150)
            plt.close(fig)
            
            print(f"  Visualización guardada en: {output_path}")
        except Exception as e:
            import traceback
            print(f"  Error en visualización: {e}")
            print(traceback.format_exc())
    
    def export_model(self, model, filename, format_ext):
        """Exporta un modelo al formato indicado"""
        if not model:
            return False
            
        self._ensure_dirs_exist()
        output_path = self.output_dir / f"{filename}{format_ext}"
        
        try:
            model.export(str(output_path))
            print(f"Guardado: {output_path}")
            return True
        except Exception as e:
            print(f"Error al exportar a {format_ext}: {e}")
            return False
    
    def generate_comparison_report(self, processed_models, names):
        """Genera un informe comparativo entre modelos"""
        if not processed_models or not names:
            print("No hay modelos para comparar")
            return
            
        print("\n=== COMPARACIÓN DE MODELOS ===")
        
        # Preparar tabla de comparación
        headers = ["Modelo", "Vértices", "Caras", "Duplicados", "Watertight"]
        col_widths = [20, 12, 12, 15, 10]
        divider = "+" + "+".join("-" * (w+2) for w in col_widths) + "+"
        
        # Mostrar encabezados
        header_row = "|" + "|".join(f" {h:{w}} " for h, w in zip(headers, col_widths)) + "|"
        print(divider)
        print(header_row)
        print(divider)
        
        # Datos para el archivo
        report_lines = [divider, header_row, divider]
        
        # Mostrar cada modelo
        for model, name in zip(processed_models, names):
            if not model:
                continue
                
            if isinstance(model, trimesh.Scene):
                model = trimesh.util.concatenate([mesh for mesh in model.geometry.values()])
                
            # Calcular estadísticas
            vertex_count = len(model.vertices)
            face_count = len(model.faces)
            dupes = len(model.vertices) - len(np.unique(model.vertices, axis=0))
            is_closed = "Sí" if model.is_watertight else "No"
            
            # Formatear fila
            row = [name, str(vertex_count), str(face_count), str(dupes), is_closed]
            formatted_row = "|" + "|".join(f" {d:{w}} " for d, w in zip(row, col_widths)) + "|"
            
            print(formatted_row)
            report_lines.append(formatted_row)
            
        print(divider)
        report_lines.append(divider)
        
        # Guardar reporte en archivo
        self._ensure_dirs_exist()
        report_path = self.output_dir / "comparacion_modelos.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
            
        print(f"\nReporte guardado en: {report_path}")
        
        # Generar gráfico comparativo
        self._generate_comparison_chart(processed_models, names)
            
    def _generate_comparison_chart(self, processed_models, names):
        """Genera gráficos comparativos entre los modelos"""
        valid_models = []
        valid_names = []
        
        # Recopilación de datos
        vertices = []
        faces = []
        
        for model, name in zip(processed_models, names):
            if not model:
                continue
                
            if isinstance(model, trimesh.Scene):
                model = trimesh.util.concatenate([mesh for mesh in model.geometry.values()])
                
            valid_models.append(model)
            valid_names.append(Path(name).stem)
            vertices.append(len(model.vertices))
            faces.append(len(model.faces))
            
        if not valid_models:
            return
            
        # Crear gráfico de barras comparativo
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Gráfico de vértices
        ax1.bar(valid_names, vertices, color='skyblue')
        ax1.set_title('Comparación de Vértices')
        ax1.set_ylabel('Número de Vértices')
        ax1.set_xlabel('Modelo')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico de caras
        ax2.bar(valid_names, faces, color='lightgreen')
        ax2.set_title('Comparación de Caras')
        ax2.set_ylabel('Número de Caras')
        ax2.set_xlabel('Modelo')
        ax2.tick_params(axis='x', rotation=45)
        
        # Guardar gráfico
        plt.tight_layout()
        chart_path = self.output_dir / "comparacion_grafica.png"
        plt.savefig(str(chart_path), dpi=150)
        plt.close()
        
        print(f"Gráfico comparativo guardado en: {chart_path}")
             
    def run(self):
        """Ejecuta el flujo completo de procesamiento"""
        # Importar los modelos
        models, filenames = self.import_all_models()
        if not models:
            print("No se encontraron modelos para procesar.")
            return
            
        # Procesar cada modelo
        processed_models = []
        for model, name in zip(models, filenames):
            processed = self.process_model(model, name)
            processed_models.append(processed)
            
        # Generar comparativa
        self.generate_comparison_report(processed_models, filenames)
        
        # Exportar a diferentes formatos
        output_formats = ['.obj', '.stl', '.glb']
        
        for model, filename in zip(processed_models, filenames):
            if not model:
                continue
                
            base_name = Path(filename).stem
            for fmt in output_formats:
                self.export_model(model, f"converted_{base_name}", fmt)
                
        print("\nProceso completado.")


processor = ModelProcessor()
processor.run()