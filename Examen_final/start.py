#!/usr/bin/env python3
"""
🚀 Script de inicio rápido para el Sistema de Reconocimiento Facial

Este script facilita la ejecución del sistema modernizado.
Incluye verificaciones de dependencias y configuración automática.
"""

import sys
import os
import subprocess
from pathlib import Path

def print_banner():
    """Muestra el banner del sistema"""
    print("=" * 60)
    print("🔐 SISTEMA DE RECONOCIMIENTO FACIAL")
    print("🎨 Versión Modernizada 2025")
    print("=" * 60)
    print()

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'cv2', 'tkinter', 'PIL', 'numpy', 'imutils'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'tkinter':
                import tkinter
            elif package == 'PIL':
                from PIL import Image
            elif package == 'numpy':
                import numpy
            elif package == 'imutils':
                import imutils
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("💡 Instala con: pip install opencv-python pillow numpy imutils")
        return False
    
    print("✅ Todas las dependencias están disponibles")
    return True

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print("\n📁 Verificando estructura del proyecto...")
    
    required_files = [
        'simple_modern.py',
        'process/config_modern.py',
        'process/utils.py',
        'process/database/config.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Estructura del proyecto correcta")
    return True

def setup_directories():
    """Crea directorios necesarios si no existen"""
    print("\n📂 Configurando directorios...")
    
    directories = [
        'process/database/users',
        'process/database/faces'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"  📁 Creado: {directory}")
        else:
            print(f"  ✅ Existe: {directory}")

def show_menu():
    """Muestra el menú principal"""
    print("\n🎯 ¿Qué deseas hacer?")
    print()
    print("1. 🚀 Iniciar Sistema de Reconocimiento Facial")
    print("2. 🧪 Verificar Sistema y Dependencias")
    print("3. ❌ Salir")
    print()

def run_modern_interface():
    """Ejecuta la interfaz moderna"""
    print("\n🚀 Iniciando Interfaz Moderna...")
    print("💡 Presiona Ctrl+C para detener")
    print("-" * 40)
    
    try:
        # Importar y ejecutar la interfaz moderna
        import tkinter as tk
        from simple_modern import SimpleModernGUI
        
        root = tk.Tk()
        app = SimpleModernGUI(root)
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n🔒 Sistema detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al ejecutar la interfaz: {e}")
        print("💡 Verifica que todas las dependencias estén instaladas")

def run_system_check():
    """Ejecuta verificación completa del sistema"""
    print("\n🧪 VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("=" * 50)
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    
    # Verificar estructura
    struct_ok = check_project_structure()
    
    # Configurar directorios
    setup_directories()
    
    # Resumen
    print("\n📋 RESUMEN DE VERIFICACIÓN")
    print("-" * 30)
    print(f"Dependencias: {'✅ OK' if deps_ok else '❌ FALLO'}")
    print(f"Estructura:   {'✅ OK' if struct_ok else '❌ FALLO'}")
    
    if deps_ok and struct_ok:
        print("\n🎉 Sistema listo para usar!")
    else:
        print("\n⚠️  Se encontraron problemas. Revisa los mensajes anteriores.")

def main():
    """Función principal"""
    print_banner()
    
    # Verificación inicial rápida
    if not os.path.exists('simple_modern.py'):
        print("❌ Error: No se encontró simple_modern.py")
        print("💡 Asegúrate de estar en el directorio del proyecto")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Selecciona una opción (1-3): ").strip()
            
            if choice == '1':
                if check_dependencies() and check_project_structure():
                    setup_directories()
                    run_modern_interface()
                else:
                    print("\n❌ No se puede ejecutar. Verifica el sistema primero (opción 2)")
            
            elif choice == '2':
                run_system_check()
            
            elif choice == '3':
                print("\n👋 ¡Hasta luego!")
                break
            
            else:
                print("\n❌ Opción inválida. Selecciona 1-3.")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
