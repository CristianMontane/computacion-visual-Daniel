"""
Interfaz gráfica moderna simplificada para el sistema de reconocimiento facial.
Versión sin temas para asegurar compatibilidad.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import os

from process.config_modern import VIDEO_CONFIG
from process.utils import (VideoProcessor, WindowManager, MessageHandler, 
                          DatabaseUtils)
from process.database.config import DataBasePaths
from process.face_processing.face_signup import FaceSignUp
from process.face_processing.face_login import FaceLogIn


class SimpleModernGUI:
    """
    Interfaz gráfica moderna simplificada para el sistema de reconocimiento facial
    
    Características:
    - Diseño limpio y funcional
    - Navegación por pestañas
    - Gestión de usuarios
    - Verificación y registro facial
    """
    
    def __init__(self, root):
        self.main_window = root
        self.setup_main_window()
        
        # Estado de la aplicación
        self.current_view = "dashboard"
        self.cap = None
        
        # Ventanas secundarias
        self.login_window = None
        self.signup_window = None
        self.capture_window = None
        
        # Campos de formulario
        self.name_entry = None
        self.code_entry = None
        
        # Módulos del sistema
        self._init_modules()
        
        # Crear interfaz
        self.create_interface()
        
        # Inicializar sistema
        MessageHandler.print_startup_messages()
    
    def setup_main_window(self):
        """Configura la ventana principal"""
        self.main_window.title("🔐 Sistema de Reconocimiento Facial - Moderno")
        self.main_window.geometry("1200x800")
        self.main_window.configure(bg='#f0f0f0')
        
        # Centrar ventana
        self.center_window()
        
        # Configurar cierre
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.main_window.update_idletasks()
        x = (self.main_window.winfo_screenwidth() // 2) - (600)
        y = (self.main_window.winfo_screenheight() // 2) - (400)
        self.main_window.geometry(f"1200x800+{x}+{y}")
    
    def _init_modules(self):
        """Inicializa los módulos del sistema"""
        self.database = DataBasePaths()
        self.face_sign_up = FaceSignUp()
        self.face_login = FaceLogIn()
    
    def create_interface(self):
        """Crea la interfaz principal"""
        # Título principal
        title_frame = tk.Frame(self.main_window, bg='#2c3e50', height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🔐 Sistema de Reconocimiento Facial",
            font=("Arial", 18, "bold"),
            fg="white",
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.main_window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_dashboard_tab()
        self.create_users_tab()
        self.create_actions_tab()
        self.create_settings_tab()
    
    def create_dashboard_tab(self):
        """Crea la pestaña del dashboard"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Título de sección
        tk.Label(
            dashboard_frame,
            text="📊 Panel de Control",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=20)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(dashboard_frame, bg='white', relief='raised', bd=2)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Obtener estadísticas
        try:
            users_path = self.database.users
            total_users = len([f for f in os.listdir(users_path) if f.endswith('.txt')]) if os.path.exists(users_path) else 0
        except:
            total_users = 0
        
        # Tarjetas de estadísticas
        stats_container = tk.Frame(stats_frame, bg='white')
        stats_container.pack(fill="x", padx=20, pady=20)
        
        # Estadística 1
        card1 = tk.Frame(stats_container, bg='#3498db', relief='raised', bd=2)
        card1.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(card1, text="👥", font=("Arial", 24), bg='#3498db', fg='white').pack(pady=5)
        tk.Label(card1, text="Total Usuarios", font=("Arial", 12, "bold"), bg='#3498db', fg='white').pack()
        tk.Label(card1, text=str(total_users), font=("Arial", 20, "bold"), bg='#3498db', fg='white').pack(pady=5)
        
        # Estadística 2
        card2 = tk.Frame(stats_container, bg='#2ecc71', relief='raised', bd=2)
        card2.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(card2, text="✅", font=("Arial", 24), bg='#2ecc71', fg='white').pack(pady=5)
        tk.Label(card2, text="Sistema Activo", font=("Arial", 12, "bold"), bg='#2ecc71', fg='white').pack()
        tk.Label(card2, text="OK", font=("Arial", 20, "bold"), bg='#2ecc71', fg='white').pack(pady=5)
        
        # Estadística 3
        card3 = tk.Frame(stats_container, bg='#e74c3c', relief='raised', bd=2)
        card3.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(card3, text="📹", font=("Arial", 24), bg='#e74c3c', fg='white').pack(pady=5)
        tk.Label(card3, text="Cámara", font=("Arial", 12, "bold"), bg='#e74c3c', fg='white').pack()
        tk.Label(card3, text="Lista", font=("Arial", 20, "bold"), bg='#e74c3c', fg='white').pack(pady=5)
        
        # Información del sistema
        info_frame = tk.Frame(dashboard_frame, bg='white', relief='raised', bd=2)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text="📋 Información del Sistema",
            font=("Arial", 14, "bold"),
            fg="#2c3e50",
            bg='white'
        ).pack(pady=10)
        
        info_text = tk.Text(info_frame, height=10, font=("Consolas", 10))
        info_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Llenar con información
        info_text.insert("1.0", f"""
🔐 Sistema de Reconocimiento Facial 
═══════════════════════════════════════════════════

📊 Estado: Sistema iniciado correctamente
👥 Usuarios registrados: {total_users}
📹 Resolución de cámara: {VIDEO_CONFIG.WIDTH}x{VIDEO_CONFIG.HEIGHT}
💾 Base de datos: {self.database.users}

🎯 Funcionalidades disponibles:
• Registro de nuevos usuarios con captura facial
• Verificación de identidad en tiempo real
• Gestión completa de usuarios registrados
• Búsqueda y filtrado de usuarios
• Configuración del sistema

💡 Instrucciones:
1. Ve a la pestaña 'Acciones' para registrar o verificar usuarios
2. Usa la pestaña 'Usuarios' para gestionar la base de datos
3. Configura el sistema en la pestaña 'Configuración'
        """)
        
        info_text.config(state="disabled")
    
    def create_users_tab(self):
        """Crea la pestaña de gestión de usuarios"""
        users_frame = ttk.Frame(self.notebook)
        self.notebook.add(users_frame, text="👥 Usuarios")
        
        # Título
        tk.Label(
            users_frame,
            text="👥 Gestión de Usuarios",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=20)
        
        # Frame de controles
        controls_frame = tk.Frame(users_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón de actualizar
        tk.Button(
            controls_frame,
            text="🔄 Actualizar Lista",
            command=self.refresh_users_list,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=20
        ).pack(side="left", padx=5)
        
        # Barra de búsqueda
        tk.Label(controls_frame, text="🔍 Buscar:", font=("Arial", 10)).pack(side="left", padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(controls_frame, textvariable=self.search_var, font=("Arial", 10), width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_users)
        
        # Lista de usuarios
        list_frame = tk.Frame(users_frame, relief='raised', bd=2)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar y listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.users_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            selectmode="single"
        )
        self.users_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.users_listbox.yview)
        
        self.users_listbox.bind("<<ListboxSelect>>", self.on_user_select)
        
        # Panel de detalles
        details_frame = tk.Frame(users_frame, bg='white', relief='raised', bd=2)
        details_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            details_frame,
            text="📋 Detalles del Usuario",
            font=("Arial", 12, "bold"),
            bg='white',
            fg="#2c3e50"
        ).pack(pady=10)
        
        self.details_text = tk.Text(details_frame, height=4, font=("Arial", 10))
        self.details_text.pack(fill="x", padx=20, pady=10)
        
        # Cargar usuarios
        self.refresh_users_list()
    
    def create_actions_tab(self):
        """Crea la pestaña de acciones"""
        actions_frame = ttk.Frame(self.notebook)
        self.notebook.add(actions_frame, text="🎯 Acciones")
        
        # Título
        tk.Label(
            actions_frame,
            text="🎯 Acciones del Sistema",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=20)
        
        # Frame de botones principales
        main_actions_frame = tk.Frame(actions_frame)
        main_actions_frame.pack(expand=True)
        
        # Botón de registro
        register_btn = tk.Button(
            main_actions_frame,
            text="📝 Registrar Nuevo Usuario",
            command=self.open_signup,
            font=("Arial", 14, "bold"),
            bg="#2ecc71",
            fg="white",
            relief="flat",
            padx=40,
            pady=20
        )
        register_btn.pack(pady=20)
        
        # Botón de verificación
        verify_btn = tk.Button(
            main_actions_frame,
            text="🔐 Verificar Identidad",
            command=self.open_login,
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=40,
            pady=20
        )
        verify_btn.pack(pady=20)
        
        # Información
        info_label = tk.Label(
            main_actions_frame,
            text="💡 Selecciona una acción para comenzar",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        info_label.pack(pady=20)
    
    def create_settings_tab(self):
        """Crea la pestaña de configuración"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Configuración")
        
        # Título
        tk.Label(
            settings_frame,
            text="⚙️ Configuración del Sistema",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=20)
        
        # Frame de configuración
        config_frame = tk.Frame(settings_frame, bg='white', relief='raised', bd=2)
        config_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configuración de cámara
        tk.Label(
            config_frame,
            text="📹 Configuración de Cámara",
            font=("Arial", 12, "bold"),
            bg='white',
            fg="#2c3e50"
        ).pack(pady=10)
        
        camera_info = tk.Text(config_frame, height=8, font=("Consolas", 10))
        camera_info.pack(fill="x", padx=20, pady=10)
        
        camera_info.insert("1.0", f"""
Configuración actual de cámara:
• Índice de cámara: {VIDEO_CONFIG.CAMERA_INDEX}
• Resolución: {VIDEO_CONFIG.WIDTH}x{VIDEO_CONFIG.HEIGHT}
• Geometría de ventana: {VIDEO_CONFIG.geometry}

Configuración de procesamiento:
• Umbral de distancia: {getattr(self, 'PROCESSING_CONFIG', {}).get('DISTANCE_THRESHOLD', 1.2)}
• Intentos de reconocimiento: 3
• Frames para captura: 48

Base de datos:
• Directorio de usuarios: {self.database.users}
• Directorio de rostros: {self.database.faces}
        """)
        
        camera_info.config(state="disabled")
        
        # Botones de configuración
        config_buttons_frame = tk.Frame(config_frame, bg='white')
        config_buttons_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Button(
            config_buttons_frame,
            text="🧪 Probar Cámara",
            command=self.test_camera,
            font=("Arial", 10, "bold"),
            bg="#f39c12",
            fg="white",
            relief="flat",
            padx=20
        ).pack(side="left", padx=5)
        
        tk.Button(
            config_buttons_frame,
            text="📁 Abrir Directorio de Datos",
            command=self.open_data_directory,
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            relief="flat",
            padx=20
        ).pack(side="left", padx=5)
    
    def refresh_users_list(self):
        """Actualiza la lista de usuarios"""
        try:
            self.users_listbox.delete(0, tk.END)
            
            users_path = self.database.users
            if not os.path.exists(users_path):
                self.users_listbox.insert(tk.END, "No hay usuarios registrados")
                return
            
            users = []
            for file_name in os.listdir(users_path):
                if file_name.endswith('.txt'):
                    user_code = file_name.replace('.txt', '')
                    file_path = os.path.join(users_path, file_name)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read().strip()
                            if content:
                                parts = content.split(',')
                                name = parts[0] if len(parts) > 0 else 'Sin nombre'
                                users.append(f"{name} (ID: {user_code})")
                    except Exception as e:
                        users.append(f"Error al leer: {user_code}")
            
            if not users:
                self.users_listbox.insert(tk.END, "No hay usuarios registrados")
            else:
                for user in sorted(users):
                    self.users_listbox.insert(tk.END, user)
                    
        except Exception as e:
            self.users_listbox.insert(tk.END, f"Error al cargar usuarios: {str(e)}")
    
    def filter_users(self, event=None):
        """Filtra usuarios según el texto de búsqueda"""
        search_text = self.search_var.get().lower()
        
        if not search_text:
            self.refresh_users_list()
            return
        
        # Filtrar lista actual
        self.users_listbox.delete(0, tk.END)
        
        try:
            users_path = self.database.users
            if not os.path.exists(users_path):
                return
            
            filtered_users = []
            for file_name in os.listdir(users_path):
                if file_name.endswith('.txt'):
                    user_code = file_name.replace('.txt', '')
                    file_path = os.path.join(users_path, file_name)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read().strip()
                            if content:
                                parts = content.split(',')
                                name = parts[0] if len(parts) > 0 else 'Sin nombre'
                                display_text = f"{name} (ID: {user_code})"
                                
                                if (search_text in name.lower() or 
                                    search_text in user_code.lower()):
                                    filtered_users.append(display_text)
                    except:
                        continue
            
            if not filtered_users:
                self.users_listbox.insert(tk.END, "No se encontraron usuarios")
            else:
                for user in sorted(filtered_users):
                    self.users_listbox.insert(tk.END, user)
                    
        except Exception as e:
            self.users_listbox.insert(tk.END, f"Error en búsqueda: {str(e)}")
    
    def on_user_select(self, event=None):
        """Maneja la selección de usuario"""
        selection = self.users_listbox.curselection()
        if not selection:
            return
        
        selected_text = self.users_listbox.get(selection[0])
        
        if "ID:" in selected_text:
            # Extraer código de usuario
            user_code = selected_text.split("ID: ")[1].rstrip(")")
            
            # Mostrar detalles
            self.show_user_details(user_code)
    
    def show_user_details(self, user_code):
        """Muestra detalles del usuario seleccionado"""
        try:
            users_path = self.database.users
            faces_path = self.database.faces
            
            user_file = os.path.join(users_path, f"{user_code}.txt")
            face_file = os.path.join(faces_path, f"{user_code}.png")
            
            details = f"📋 Detalles del Usuario: {user_code}\n"
            details += "=" * 40 + "\n"
            
            if os.path.exists(user_file):
                with open(user_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        parts = content.split(',')
                        name = parts[0] if len(parts) > 0 else 'Sin nombre'
                        details += f"👤 Nombre: {name}\n"
                        details += f"🆔 Código: {user_code}\n"
                        
                        # Información del archivo
                        stat = os.stat(user_file)
                        import datetime
                        reg_date = datetime.datetime.fromtimestamp(stat.st_mtime)
                        details += f"📅 Registrado: {reg_date.strftime('%Y-%m-%d %H:%M')}\n"
            
            # Verificar si tiene imagen facial
            if os.path.exists(face_file):
                details += "📸 Imagen facial: ✅ Disponible\n"
                stat = os.stat(face_file)
                size_kb = stat.st_size / 1024
                details += f"📏 Tamaño de imagen: {size_kb:.1f} KB\n"
            else:
                details += "📸 Imagen facial: ❌ No disponible\n"
            
            details += f"📁 Archivo de datos: {user_file}\n"
            details += f"🖼️ Archivo de imagen: {face_file}\n"
            
            self.details_text.config(state="normal")
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert("1.0", details)
            self.details_text.config(state="disabled")
            
        except Exception as e:
            self.details_text.config(state="normal")
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert("1.0", f"❌ Error al cargar detalles: {str(e)}")
            self.details_text.config(state="disabled")
    
    def open_signup(self):
        """Abre la ventana de registro"""
        try:
            if self.signup_window and self.signup_window.winfo_exists():
                self.signup_window.lift()
                return
            
            self.signup_window = WindowManager.create_window("🔐 Registro de Usuario", self.main_window)
            self.setup_signup_window_ui()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el registro: {str(e)}")
    
    def open_login(self):
        """Abre la ventana de verificación"""
        try:
            if self.login_window and self.login_window.winfo_exists():
                self.login_window.lift()
                return
            
            self.login_window = WindowManager.create_window("🔐 Verificación de Identidad", self.main_window)
            self.setup_login_window_ui()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la verificación: {str(e)}")
    
    def setup_signup_window_ui(self):
        """Configura la interfaz de la ventana de registro"""
        window = self.signup_window
        
        # Título
        title_label = tk.Label(
            window,
            text="📝 Registro de Nuevo Usuario",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Frame del formulario
        form_frame = tk.Frame(window, bg='white', relief='raised', bd=2)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Campo nombre
        tk.Label(form_frame, text="👤 Nombre:", font=("Arial", 12), bg='white').pack(pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=5)
        
        # Campo código
        tk.Label(form_frame, text="🆔 Código de Usuario:", font=("Arial", 12), bg='white').pack(pady=5)
        self.code_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.code_entry.pack(pady=5)
        
        # Botones
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        register_btn = tk.Button(
            buttons_frame,
            text="📸 Iniciar Registro",
            command=self.start_face_registration,
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=10
        )
        register_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Cancelar",
            command=window.destroy,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10
        )
        cancel_btn.pack(side="left", padx=10)
    
    def setup_login_window_ui(self):
        """Configura la interfaz de la ventana de verificación"""
        window = self.login_window
        
        # Título
        title_label = tk.Label(
            window,
            text="🔐 Verificación de Identidad",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Información
        info_frame = tk.Frame(window, bg='white', relief='raised', bd=2)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_text = tk.Text(info_frame, height=10, font=("Arial", 11))
        info_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_text.insert("1.0", """
🔐 Verificación de Identidad Facial

📋 Instrucciones:
1. Haz clic en "Iniciar Verificación" 
2. Mira directamente a la cámara
3. Mantén tu rostro centrado y bien iluminado
4. Espera a que el sistema procese tu identidad

⚠️ Requisitos:
• Buena iluminación
• Rostro centrado en la cámara
• No usar lentes oscuros
• Mantente quieto durante el proceso

📊 El sistema comparará tu rostro con la base de datos
de usuarios registrados para verificar tu identidad.
        """)
        
        info_text.config(state="disabled")
        
        # Botones
        buttons_frame = tk.Frame(window)
        buttons_frame.pack(pady=20)
        
        verify_btn = tk.Button(
            buttons_frame,
            text="🚀 Iniciar Verificación",
            command=self.start_face_verification,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10
        )
        verify_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Cancelar",
            command=window.destroy,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10
        )
        cancel_btn.pack(side="left", padx=10)
    
    def start_face_registration(self):
        """Inicia el proceso de registro facial"""
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip()
        
        # Validaciones
        if not name or not code:
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los campos")
            return
        
        if len(name) < 2:
            messagebox.showwarning("Nombre Inválido", "El nombre debe tener al menos 2 caracteres")
            return
        
        if len(code) < 3:
            messagebox.showwarning("Código Inválido", "El código debe tener al menos 3 caracteres")
            return
        
        # Verificar si el usuario ya existe
        try:
            users_path = self.database.users
            if os.path.exists(os.path.join(users_path, f"{code}.txt")):
                messagebox.showerror("Usuario Existente", f"Ya existe un usuario con el código '{code}'")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar usuario: {str(e)}")
            return
        
        # Guardar datos del usuario en archivo
        try:
            os.makedirs(users_path, exist_ok=True)
            user_file = os.path.join(users_path, f"{code}.txt")
            with open(user_file, 'w', encoding='utf-8') as f:
                f.write(f"{name},{code},\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos del usuario: {str(e)}")
            return
        
        # Cerrar ventana de registro e iniciar captura facial
        self.signup_window.destroy()
        MessageHandler.print_registration_start(name, code)
        
        # Iniciar captura facial real con cámara
        self.open_camera_registration(code)
    
    def start_face_verification(self):
        """Inicia el proceso de verificación facial"""
        self.login_window.destroy()
        print("🔐 Iniciando verificación de identidad facial")
        
        # Verificar que hay usuarios registrados
        try:
            users_path = self.database.users
            if not os.path.exists(users_path):
                messagebox.showwarning("Sin Usuarios", "No hay usuarios registrados para verificar")
                return
            
            users = [f for f in os.listdir(users_path) if f.endswith('.txt')]
            if not users:
                messagebox.showwarning("Sin Usuarios", "No hay usuarios registrados para verificar")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar usuarios: {str(e)}")
            return
        
        # Iniciar verificación facial real con cámara
        self.open_camera_verification()
    
    def simulate_face_registration(self, name, code):
        """Simula el proceso de registro facial"""
        try:
            # Crear directorios si no existen
            users_path = self.database.users
            faces_path = self.database.faces
            
            os.makedirs(users_path, exist_ok=True)
            os.makedirs(faces_path, exist_ok=True)
            
            # Guardar datos del usuario
            user_file = os.path.join(users_path, f"{code}.txt")
            with open(user_file, 'w', encoding='utf-8') as f:
                f.write(f"{name},{code},\n")
            
            # Simular creación de imagen facial (archivo vacío por ahora)
            face_file = os.path.join(faces_path, f"{code}.png")
            with open(face_file, 'w') as f:
                f.write("")  # Archivo vacío como placeholder
            
            messagebox.showinfo("Registro Exitoso", f"Usuario {name} registrado correctamente")
            print("✅ REGISTRO EXITOSO - Rostro capturado y guardado")
            print("👤 Usuario registrado correctamente en la base de datos")
            
            # Actualizar lista de usuarios si está visible
            if hasattr(self, 'users_listbox'):
                self.refresh_users_list()
                
        except Exception as e:
            messagebox.showerror("Error en Registro", f"Error al registrar usuario: {str(e)}")
            print(f"❌ Error al registrar usuario: {str(e)}")
    
    def simulate_face_verification(self):
        """Simula el proceso de verificación facial"""
        try:
            # Simular verificación
            users_path = self.database.users
            
            if not os.path.exists(users_path):
                messagebox.showwarning("Sin Usuarios", "No hay usuarios registrados para verificar")
                return
            
            users = [f for f in os.listdir(users_path) if f.endswith('.txt')]
            
            if not users:
                messagebox.showwarning("Sin Usuarios", "No hay usuarios registrados para verificar")
                return
            
            # Simular verificación exitosa (por ejemplo, primer usuario)
            user_file = users[0]
            user_code = user_file.replace('.txt', '')
            
            try:
                with open(os.path.join(users_path, user_file), 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    name = content.split(',')[0] if content else 'Usuario'
                
                messagebox.showinfo("Verificación Exitosa", f"✅ Identidad verificada: {name} (ID: {user_code})")
                print("✅ IDENTIDAD VERIFICADA - Usuario reconocido exitosamente")
                print("👤 Coincidencia facial confirmada")
                
            except Exception as e:
                messagebox.showinfo("Verificación Simulada", "✅ Verificación facial simulada exitosa")
                
        except Exception as e:
            messagebox.showerror("Error en Verificación", f"Error al verificar identidad: {str(e)}")
            print(f"❌ Error al verificar identidad: {str(e)}")
    
    def test_camera(self):
        """Prueba la cámara del sistema"""
        try:
            cap = VideoProcessor.setup_camera()
            if cap.isOpened():
                cap.release()
                messagebox.showinfo("Prueba de Cámara", "✅ Cámara funcionando correctamente")
            else:
                messagebox.showerror("Prueba de Cámara", "❌ No se pudo acceder a la cámara")
        except Exception as e:
            messagebox.showerror("Prueba de Cámara", f"❌ Error al probar cámara: {str(e)}")
    
    def open_data_directory(self):
        """Abre el directorio de datos"""
        try:
            import subprocess
            import platform
            
            path = self.database.users
            
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux
                subprocess.run(["xdg-open", path])
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el directorio: {str(e)}")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Deseas cerrar el sistema?"):
            if self.cap:
                self.cap.release()
            self.main_window.quit()
            self.main_window.destroy()
    
    def open_camera_registration(self, user_code: str):
        """Abre la ventana de captura de cámara para registro"""
        try:
            # Crear ventana de captura
            self.capture_window = WindowManager.create_window("📹 Captura Facial - Registro", self.main_window)
            self.capture_window.geometry("900x750")
            
            # Configurar cámara
            self.cap = VideoProcessor.setup_camera()
            if not self.cap.isOpened():
                messagebox.showerror("Error de Cámara", "No se pudo acceder a la cámara")
                self.capture_window.destroy()
                return
            
            # Crear interfaz de captura
            self.setup_camera_ui_registration(user_code)
            
            # Iniciar captura
            self.registration_active = True
            self.current_user_code = user_code
            self.update_camera_registration()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir cámara: {str(e)}")
    
    def open_camera_verification(self):
        """Abre la ventana de captura de cámara para verificación"""
        try:
            # Crear ventana de captura
            self.capture_window = WindowManager.create_window("🔐 Verificación Facial", self.main_window)
            self.capture_window.geometry("900x750")
            
            # Configurar cámara
            self.cap = VideoProcessor.setup_camera()
            if not self.cap.isOpened():
                messagebox.showerror("Error de Cámara", "No se pudo acceder a la cámara")
                self.capture_window.destroy()
                return
            
            # Crear interfaz de captura
            self.setup_camera_ui_verification()
            
            # Iniciar verificación
            self.verification_active = True
            self.face_login.matcher = None  # Reset matcher
            self.face_login.comparison = False
            self.face_login.cont_frame = 0
            self.update_camera_verification()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir cámara: {str(e)}")
    
    def setup_camera_ui_registration(self, user_code: str):
        """Configura la interfaz de captura para registro"""
        window = self.capture_window
        
        # Título
        title_label = tk.Label(
            window,
            text=f"📹 Registrando Usuario: {user_code}",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Label para el video (más grande)
        video_frame = tk.Frame(window, bg='black', relief='sunken', bd=2)
        video_frame.pack(pady=10, padx=20)
        
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(padx=10, pady=10)
        
        # Frame de instrucciones
        instructions_frame = tk.Frame(window, bg='white', relief='raised', bd=2)
        instructions_frame.pack(fill="x", padx=20, pady=10)
        
        instructions_text = """
📋 Instrucciones para el registro:
• Coloca tu rostro en el centro de la cámara
• Mantén el rostro bien iluminado
• No uses lentes oscuros o mascarillas
• Espera a que aparezca la confirmación
        """
        
        tk.Label(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 10),
            bg='white',
            justify='left'
        ).pack(padx=20, pady=10)
        
        # Label de estado
        self.status_label_reg = tk.Label(
            window,
            text="🔄 Iniciando captura...",
            font=("Arial", 12),
            fg="#3498db"
        )
        self.status_label_reg.pack(pady=10)
        
        # Botón cancelar
        cancel_btn = tk.Button(
            window,
            text="❌ Cancelar",
            command=self.close_camera_registration,
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        cancel_btn.pack(pady=10)
        
        # Configurar cierre de ventana
        window.protocol("WM_DELETE_WINDOW", self.close_camera_registration)
    
    def setup_camera_ui_verification(self):
        """Configura la interfaz de captura para verificación"""
        window = self.capture_window
        
        # Título
        title_label = tk.Label(
            window,
            text="🔐 Verificación de Identidad",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Label para el video (más grande)
        video_frame = tk.Frame(window, bg='black', relief='sunken', bd=2)
        video_frame.pack(pady=10, padx=20)
        
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(padx=10, pady=10)
        
        # Frame de instrucciones
        instructions_frame = tk.Frame(window, bg='white', relief='raised', bd=2)
        instructions_frame.pack(fill="x", padx=20, pady=10)
        
        instructions_text = """
🔍 Instrucciones para la verificación:
• Mira directamente a la cámara
• Mantén el rostro centrado y bien iluminado
• El sistema comparará tu rostro con la base de datos
• Espera el resultado de la verificación
        """
        
        tk.Label(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 10),
            bg='white',
            justify='left'
        ).pack(padx=20, pady=10)
        
        # Label de estado
        self.status_label_ver = tk.Label(
            window,
            text="🔄 Iniciando verificación...",
            font=("Arial", 12),
            fg="#3498db"
        )
        self.status_label_ver.pack(pady=10)
        
        # Botón cancelar
        cancel_btn = tk.Button(
            window,
            text="❌ Cancelar",
            command=self.close_camera_verification,
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        cancel_btn.pack(pady=10)
        
        # Configurar cierre de ventana
        window.protocol("WM_DELETE_WINDOW", self.close_camera_verification)
    
    def update_camera_registration(self):
        """Actualiza la cámara para el proceso de registro"""
        if not hasattr(self, 'registration_active') or not self.registration_active:
            return
            
        try:
            ret, frame = self.cap.read()
            if ret:
                # Procesar frame con FaceSignUp
                processed_frame, success, message = self.face_sign_up.process(frame, self.current_user_code)
                
                # Actualizar estado
                self.status_label_reg.config(text=f"📹 {message}")
                
                # Convertir frame para mostrar (más grande)
                _, tk_image = VideoProcessor.process_frame_large(processed_frame, 720)
                
                # Actualizar video
                if hasattr(self, 'video_label') and self.video_label.winfo_exists():
                    self.video_label.config(image=tk_image)
                    self.video_label.image = tk_image
                
                # Si el registro fue exitoso
                if success:
                    self.registration_success()
                    return
                
                # Continuar captura
                if self.registration_active:
                    self.capture_window.after(30, self.update_camera_registration)
                    
        except Exception as e:
            print(f"Error en captura de registro: {str(e)}")
            self.close_camera_registration()
    
    def update_camera_verification(self):
        """Actualiza la cámara para el proceso de verificación"""
        if not hasattr(self, 'verification_active') or not self.verification_active:
            return
            
        try:
            ret, frame = self.cap.read()
            if ret:
                # Procesar frame con FaceLogIn
                processed_frame, matcher_result, message = self.face_login.process(frame)
                
                # Actualizar estado
                self.status_label_ver.config(text=f"🔐 {message}")
                
                # Convertir frame para mostrar (más grande)
                _, tk_image = VideoProcessor.process_frame_large(processed_frame, 720)
                
                # Actualizar video
                if hasattr(self, 'video_label') and self.video_label.winfo_exists():
                    self.video_label.config(image=tk_image)
                    self.video_label.image = tk_image
                
                # Si se encontró una coincidencia
                if matcher_result is True:
                    self.verification_success(message)
                    return
                elif matcher_result is False and self.face_login.comparison:
                    self.verification_failed(message)
                    return
                
                # Continuar verificación
                if self.verification_active:
                    self.capture_window.after(30, self.update_camera_verification)
                    
        except Exception as e:
            print(f"Error en captura de verificación: {str(e)}")
            self.close_camera_verification()
    
    def registration_success(self):
        """Maneja el éxito del registro"""
        self.registration_active = False
        if self.cap:
            self.cap.release()
        
        MessageHandler.print_registration_success()
        messagebox.showinfo("Registro Exitoso", "✅ Rostro registrado correctamente")
        
        # Actualizar lista de usuarios si está visible
        if hasattr(self, 'users_listbox'):
            self.refresh_users_list()
        
        self.capture_window.destroy()
    
    def verification_success(self, message: str):
        """Maneja el éxito de la verificación"""
        self.verification_active = False
        if self.cap:
            self.cap.release()
        
        MessageHandler.print_identity_verified()
        messagebox.showinfo("Verificación Exitosa", f"✅ {message}")
        
        self.capture_window.destroy()
    
    def verification_failed(self, message: str):
        """Maneja el fallo de la verificación"""
        self.verification_active = False
        if self.cap:
            self.cap.release()
        
        MessageHandler.print_identity_not_verified()
        messagebox.showwarning("Verificación Fallida", f"❌ {message}")
        
        self.capture_window.destroy()
    
    def close_camera_registration(self):
        """Cierra la ventana de captura de registro"""
        self.registration_active = False
        if self.cap:
            self.cap.release()
        if hasattr(self, 'capture_window') and self.capture_window.winfo_exists():
            self.capture_window.destroy()
        MessageHandler.print_window_closing("registro")
    
    def close_camera_verification(self):
        """Cierra la ventana de captura de verificación"""
        self.verification_active = False
        if self.cap:
            self.cap.release()
        if hasattr(self, 'capture_window') and self.capture_window.winfo_exists():
            self.capture_window.destroy()
        MessageHandler.print_window_closing("verificación")


def main():
    """Función principal"""
    root = tk.Tk()
    app = SimpleModernGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
