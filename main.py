import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
from db_connection import get_conn
from Usuario import Usuario
from Cliente import Cliente
from Administrador import Administrador
from Vuelo import Vuelo
from Hotel import Hotel
from Reserva import Reserva 

ROLE_MAP = {1: 'Cliente', 2: 'Administrador'}
current_user = None 

def get_user_role(email, password):
    """
    Busca el usuario por email/password y devuelve un OBJETO Cliente o Administrador.
    Utiliza un cursor de diccionario para mapear las columnas a las propiedades del objeto.
    """
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True) 
        query = "SELECT id, nombre, email, password, tipo FROM usuarios WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        user_data = cursor.fetchone()
        
        if user_data:
            if user_data['tipo'] == 2:
                return Administrador(
                    id=user_data['id'], 
                    nombre=user_data['nombre'], 
                    email=user_data['email'], 
                    password=user_data['password'], 
                    tipo=user_data['tipo']
                )
            else:
                return Cliente(
                    id=user_data['id'], 
                    nombre=user_data['nombre'], 
                    email=user_data['email'], 
                    password=user_data['password'], 
                    tipo=user_data['tipo']
                )
        return None
    except Exception as e:
        messagebox.showerror("Error DB", f"Error al autenticar:\n{e}")
        return None
    finally:
        if conn: conn.close()

def db_execute(query, params=None, commit=False, fetchone=False, fetchall=False, dictionary=False):
    """Función helper para ejecutar consultas."""
    conn = None
    result = None
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=dictionary) 
        cursor.execute(query, params or ())
        
        if commit:
            conn.commit()
            return True  
            
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        return result
        
    except Exception as e:
        messagebox.showerror("Error DB", f"Error de Base de Datos:\n{e}")
        if conn and commit:
            conn.rollback()
        return None
    finally:
        if conn: conn.close()


def registrar_usuario_db(nombre, email, password, tipo):
    """Guarda un nuevo usuario en la DB."""
    query = "INSERT INTO usuarios (nombre, email, password, tipo) VALUES (%s, %s, %s, %s)"
    return db_execute(query, (nombre, email, password, tipo), commit=True)


def requiere_rol(required_role):
    """Decorador para funciones que requieren un rol específico (2=Admin, 1=Cliente)."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            global current_user
            if current_user is None:
                messagebox.showerror("Permisos", "Debe iniciar sesión para realizar esta acción.")
                return
            if current_user.get_tipo() != required_role: 
                messagebox.showerror("Permisos", f"Acción restringida: se requiere rol {ROLE_MAP.get(required_role, 'Desconocido')}.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator

def salir():
    """Cierra la aplicación."""
    root.destroy()
    sys.exit(0)

def login_inicial():
    """Solicita login o registro al iniciar la aplicación."""
    global current_user

    while True:
        choice = messagebox.askyesno("Bienvenido al Sistema de Viajes", "¿Tienes una cuenta en el sistema?")
        if choice is None:
            salir()
            return
        
        if choice: 
            email = simpledialog.askstring("Inicio de sesión", "Email:", parent=root)
            if email is None: continue 
            password = simpledialog.askstring("Inicio de sesión", "Contraseña:", show='*', parent=root)
            if password is None: continue 

            user_object = get_user_role(email.strip(), password) 

            if user_object:
                current_user = user_object
                lbl_help.config(text=f"Conectado: {current_user.get_nombre()} ({ROLE_MAP[current_user.get_tipo()]})")
                ajustar_menu_por_rol()
                listar_vuelos()
                return
            else:
                retry = messagebox.askretrycancel("Error", "Credenciales incorrectas. ¿Deseas intentar de nuevo?")
                if not retry:
                    want_reg = messagebox.askyesno("Registro", "¿Deseas registrarte ahora?")
                    if not want_reg:
                        messagebox.showerror("Error", "Saliendo del sistema.")
                        salir()
                        return

        if not choice or (choice and not user_object): 
            nombre = simpledialog.askstring("Registrar usuario", "Nombre:", parent=root)
            if not nombre: continue
            email = simpledialog.askstring("Registrar usuario", "Email:", parent=root)
            if not email: continue
            password = simpledialog.askstring("Registrar usuario", "Contraseña:", show='*', parent=root)
            if not password: continue
            
            role_type = simpledialog.askinteger("Registrar usuario", "Tipo de usuario (1=Cliente, 2=Administrador):", minvalue=1, maxvalue=2, parent=root)
            if role_type is None: continue
            
            if registrar_usuario_db(nombre.strip(), email.strip(), password, role_type) is not None:
                messagebox.showinfo("OK", f"Usuario registrado: {nombre} ({ROLE_MAP[role_type]})")
                
                user_object = get_user_role(email.strip(), password)
                if user_object:
                    current_user = user_object
                    lbl_help.config(text=f"Conectado: {current_user.get_nombre()} ({ROLE_MAP[current_user.get_tipo()]})")
                    ajustar_menu_por_rol()
                    listar_vuelos()
                    return
                else:
                    messagebox.showerror("Error", "Fallo al iniciar sesión después del registro.")
                    return
            else:
                messagebox.showerror("Error", "Fallo al registrar usuario.")


def ajustar_menu_por_rol():
    """Habilita/deshabilita opciones del menú según el rol del usuario actual."""
    is_admin = current_user is not None and current_user.get_tipo() == 2
    is_client = current_user is not None and current_user.get_tipo() == 1

    admin_menu.entryconfig("Crear Vuelo", state="normal" if is_admin else "disabled")
    admin_menu.entryconfig("Crear Hotel", state="normal" if is_admin else "disabled")
    cliente_menu.entryconfig("Reservar Paquete", state="normal" if is_client or is_admin else "disabled")
    cliente_menu.entryconfig("Ver Historial de Reservas", state="normal" if is_client or is_admin else "disabled")
    consulta_menu.entryconfig("Ver Vuelos Disponibles", state="normal" if current_user else "disabled")
    consulta_menu.entryconfig("Ver Hoteles Disponibles", state="normal" if current_user else "disabled")

@requiere_rol(2)
def crear_vuelo():
    """Permite al Admin crear un nuevo vuelo."""
    try:
        origen = simpledialog.askstring("Crear Vuelo", "Origen:", parent=root)
        if not origen: return
        destino = simpledialog.askstring("Crear Vuelo", "Destino:", parent=root)
        if not destino: return
        fecha_str = simpledialog.askstring("Crear Vuelo", "Fecha (YYYY-MM-DD):", parent=root)
        if not fecha_str: return
        datetime.strptime(fecha_str, '%Y-%m-%d')
        
        precio = simpledialog.askfloat("Crear Vuelo", "Precio:", parent=root)
        if precio is None: return
        
        query = "INSERT INTO vuelos (origen, destino, fecha, precio) VALUES (%s, %s, %s, %s)"
        if db_execute(query, (origen.strip(), destino.strip(), fecha_str, precio), commit=True) is not None:
            messagebox.showinfo("OK", "Vuelo agregado exitosamente.")
            listar_vuelos()
        else:
            messagebox.showerror("Error", "No se pudo crear el vuelo.")
    except ValueError:
        messagebox.showerror("Error de formato", "Formato de fecha o precio inválido. Use YYYY-MM-DD para la fecha.")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{e}")

@requiere_rol(2)
def crear_hotel():
    """Permite al Admin crear un nuevo hotel."""
    try:
        nombre = simpledialog.askstring("Crear Hotel", "Nombre del hotel:", parent=root)
        if not nombre: return
        ubicacion = simpledialog.askstring("Crear Hotel", "Ubicación:", parent=root)
        if not ubicacion: return
        precio = simpledialog.askfloat("Crear Hotel", "Precio por noche:", parent=root)
        if precio is None: return

        query = "INSERT INTO hoteles (nombre, ubicacion, precio_por_noche) VALUES (%s, %s, %s)"
        if db_execute(query, (nombre.strip(), ubicacion.strip(), precio), commit=True) is not None:
            messagebox.showinfo("OK", "Hotel agregado exitosamente.")
            listar_hoteles()
        else:
            messagebox.showerror("Error", "No se pudo crear el hotel.")
    except ValueError:
        messagebox.showerror("Error de formato", "Precio por noche inválido.")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado:\n{e}")

def listar_vuelos():
    """Muestra todos los vuelos disponibles y devuelve una lista de objetos Vuelo."""
    vuelos_data = db_execute("SELECT id, origen, destino, fecha, precio FROM vuelos ORDER BY fecha DESC", fetchall=True)
    
    vuelos_objects = []
    
    lb_output.delete(0, tk.END)
    lb_output.insert(tk.END, "✈️ VUELOS DISPONIBLES:")
    lb_output.insert(tk.END, "---")
    
    if not vuelos_data:
        lb_output.insert(tk.END, "(No hay vuelos registrados.)")
        return []
    
    for v_data in vuelos_data:
        vuelo_obj = Vuelo(id=v_data[0], origen=v_data[1], destino=v_data[2], fecha=v_data[3], precio=v_data[4])
        vuelos_objects.append(vuelo_obj)
        
        fecha_obj = vuelo_obj.get_fecha()
        fecha_str = fecha_obj.strftime('%Y-%m-%d') if isinstance(fecha_obj, date) else str(fecha_obj)
        
        lb_output.insert(tk.END, f"  [ID {vuelo_obj.get_id()}] {vuelo_obj.get_origen()} -> {vuelo_obj.get_destino()} | Fecha: {fecha_str} | Precio: ${vuelo_obj.get_precio():.2f}")
        
    return vuelos_objects

def listar_hoteles():
    """Muestra todos los hoteles disponibles y devuelve una lista de objetos Hotel."""
    hoteles_data = db_execute("SELECT id, nombre, ubicacion, precio_por_noche FROM hoteles", fetchall=True)
    
    hoteles_objects = []
    
    lb_output.delete(0, tk.END)
    lb_output.insert(tk.END, "🏨 HOTELES DISPONIBLES:")
    lb_output.insert(tk.END, "---")
    if not hoteles_data:
        lb_output.insert(tk.END, "(No hay hoteles registrados.)")
        return []

    for h_data in hoteles_data:
        hotel_obj = Hotel(id=h_data[0], nombre=h_data[1], ubicacion=h_data[2], precio_noche=h_data[3])
        hoteles_objects.append(hotel_obj)
        
        lb_output.insert(tk.END, f"  [ID {hotel_obj.get_id()}] {hotel_obj.get_nombre()} ({hotel_obj.get_ubicacion()}) | Precio/Noche: ${hotel_obj.get_precio_noche():.2f}")
        
    return hoteles_objects

@requiere_rol(1)
def reservar_paquete():
    """Permite al Cliente seleccionar un vuelo y un hotel para reservar."""
    
    o = simpledialog.askstring("Reservar", "Origen del vuelo:", parent=root)
    if not o: return
    d = simpledialog.askstring("Reservar", "Destino del vuelo:", parent=root)
    if not d: return
    
    vuelos_data_encontrados = db_execute(
        "SELECT id, origen, destino, fecha, precio FROM vuelos WHERE origen=%s AND destino=%s",
        (o.strip(), d.strip()), fetchall=True
    )
    
    if not vuelos_data_encontrados:
        messagebox.showinfo("Sin resultados", "No se encontraron vuelos para esa ruta.")
        return

    vuelo_str = "Vuelos encontrados:\n"
    vuelo_map = {}
    
    for i, v_data in enumerate(vuelos_data_encontrados):
        vuelo_obj = Vuelo(id=v_data[0], origen=v_data[1], destino=v_data[2], fecha=v_data[3], precio=v_data[4])
        vuelo_map[vuelo_obj.get_id()] = vuelo_obj
        
        fecha_obj = vuelo_obj.get_fecha()
        fecha_str = fecha_obj.strftime('%Y-%m-%d') if isinstance(fecha_obj, date) else str(fecha_obj)
        vuelo_str += f"{i+1}. ID {vuelo_obj.get_id()} - {vuelo_obj.get_origen()} -> {vuelo_obj.get_destino()}, {fecha_str} - ${vuelo_obj.get_precio():.2f}\n"

    vuelo_id_input = simpledialog.askinteger("Seleccionar Vuelo", f"{vuelo_str}\nIngrese el ID del vuelo a reservar:", parent=root)
    
    vuelo_seleccionado_obj = vuelo_map.get(vuelo_id_input)
    if not vuelo_seleccionado_obj:
        messagebox.showerror("Error", "ID de vuelo inválido o no seleccionado.")
        return
        
    vuelo_id = vuelo_seleccionado_obj.get_id()
    precio_vuelo = vuelo_seleccionado_obj.get_precio()

    hoteles_objects = listar_hoteles() 
    if not hoteles_objects:
        return
        
    hotel_str = "Hoteles disponibles:\n"
    hotel_map = {}
    for h_obj in hoteles_objects:
        hotel_map[h_obj.get_id()] = h_obj
        hotel_str += f"[ID {h_obj.get_id()}] {h_obj.get_nombre()} ({h_obj.get_ubicacion()}) - ${h_obj.get_precio_noche():.2f}/noche\n"
        
    hotel_id_input = simpledialog.askinteger("Seleccionar Hotel", f"{hotel_str}\nIngrese el ID del hotel a reservar:", parent=root)

    hotel_seleccionado_obj = hotel_map.get(hotel_id_input)
    if not hotel_seleccionado_obj:
        messagebox.showerror("Error", "ID de hotel inválido o no seleccionado.")
        return
    
    hotel_id = hotel_seleccionado_obj.get_id()
    precio_hotel = hotel_seleccionado_obj.get_precio_noche()

    total = precio_vuelo + precio_hotel
    
    if messagebox.askyesno("Confirmar Reserva", f"Total a pagar: ${total:.2f}. ¿Confirmar reserva?"):
        query = "INSERT INTO reservaciones (usuario_id, vuelo_id, hotel_id, total) VALUES (%s, %s, %s, %s)"
        if db_execute(query, (current_user.get_id(), vuelo_id, hotel_id, total), commit=True) is not None:
            messagebox.showinfo("Éxito", f"🎉 Reserva creada exitosamente. Total: ${total:.2f}")
            mostrar_historial()
        else:
            messagebox.showerror("Error", "No se pudo guardar la reserva.")

@requiere_rol(1)
def mostrar_historial():
    """Muestra el historial de reservaciones del usuario actual."""
    user_id = current_user.get_id()
    
    query = """
        SELECT r.id, v.origen, v.destino, h.nombre, r.total
        FROM reservaciones r
        LEFT JOIN vuelos v ON r.vuelo_id = v.id
        LEFT JOIN hoteles h ON r.hotel_id = h.id
        WHERE r.usuario_id = %s
    """
    reservas_data = db_execute(query, (user_id,), fetchall=True)

    lb_output.delete(0, tk.END)
    lb_output.insert(tk.END, f"📅 HISTORIAL DE RESERVAS para {current_user.get_nombre()}:")
    lb_output.insert(tk.END, "---")

    if not reservas_data:
        lb_output.insert(tk.END, "No tienes reservas registradas.")
        return

    for r_data in reservas_data:
        lb_output.insert(tk.END, f"- Reserva #{r_data[0]}: Vuelo {r_data[1]}->{r_data[2]}, Hotel {r_data[3]}, Total ${r_data[4]:.2f}")


root = tk.Tk()
root.title("✈️ Sistema de Reservaciones de Viajes")
root.geometry("800x500")
root.minsize(700, 420)

menubar = tk.Menu(root)
cliente_menu = tk.Menu(menubar, tearoff=0)
cliente_menu.add_command(label="Reservar Paquete", command=reservar_paquete)
cliente_menu.add_command(label="Ver Historial de Reservas", command=mostrar_historial)
menubar.add_cascade(label="Reservar", menu=cliente_menu)

admin_menu = tk.Menu(menubar, tearoff=0)
admin_menu.add_command(label="Crear Vuelo", command=crear_vuelo)
admin_menu.add_command(label="Crear Hotel", command=crear_hotel)
menubar.add_cascade(label="Administración", menu=admin_menu)

consulta_menu = tk.Menu(menubar, tearoff=0)
consulta_menu.add_command(label="Ver Vuelos Disponibles", command=listar_vuelos)
consulta_menu.add_command(label="Ver Hoteles Disponibles", command=listar_hoteles)
menubar.add_cascade(label="Consultas", menu=consulta_menu)

archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_command(label="Salir", command=salir)
menubar.add_cascade(label="Archivo", menu=archivo_menu)

root.config(menu=menubar)

frame_output = ttk.Frame(root, padding=(12, 12))
frame_output.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

lbl_output = ttk.Label(frame_output, text="Salida de Resultados", font=("Segoe UI", 12, "bold"))
lbl_output.pack(anchor="w")

frame_list = ttk.Frame(frame_output)
frame_list.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

sb = ttk.Scrollbar(frame_list, orient=tk.VERTICAL)
lb_output = tk.Listbox(frame_list, yscrollcommand=sb.set, font=("Consolas", 10))
sb.config(command=lb_output.yview)
sb.pack(side=tk.RIGHT, fill=tk.Y)
lb_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
lbl_help = ttk.Label(frame_output, text="Iniciando...", font=("Segoe UI", 9))
lbl_help.pack(anchor="w", pady=(8, 0))
root.after(100, login_inicial)

root.mainloop()