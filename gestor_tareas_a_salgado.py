import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3

#Variables y funciones generales
fuente = "Segoe UI Variable Display"
def color_estado(estado):
        if estado == "Pendiente":
            return "red"
        elif estado == "En progreso":
            return "yellow"
        elif estado == "Completado":
            return "green"
        else:
            return "white"

##################### Base de Datos ######################
class BaseDatos:
    def __init__(self):
        self.nombre_base = "gestion_tareas.db"
        self.conn = sqlite3.connect(self.nombre_base)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS listas_tareas (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, fecha TEXT DEFAULT CURRENT_DATE )")
        self.conn.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, nombre_lista TEXT NOT NULL, nombre_tarea TEXT NOT NULL, descripcion TEXT , fecha_creacion TEXT DEFAULT CURRENT_DATE, fecha_vencimiento TEXT, estado TEXT )")
        self.conn.commit()

    def listar_listas_tareas(self):
        self.cursor.execute("SELECT * FROM listas_tareas")
        return self.cursor.fetchall()
    
    def crear_lista_tareas(self,nombre_lista):
        self.cursor.execute("INSERT INTO listas_tareas (nombre) VALUES (?)", (nombre_lista,))
        self.conn.commit()

    def eliminar_lista(self,nombre_lista):
        self.cursor.execute("DELETE FROM tareas WHERE nombre_lista = ?", (nombre_lista,))
        self.cursor.execute("DELETE FROM listas_tareas WHERE nombre = ?",(nombre_lista,))
        self.conn.commit()
    
    def crear_tarea(self, nombre_lista, nombre_tarea, descripcion, fecha_vencimiento, estado):
        try:
            self.cursor.execute("INSERT INTO tareas (nombre_lista, nombre_tarea, descripcion, fecha_vencimiento, estado) VALUES (?, ?, ?, ?, ?)", (nombre_lista, nombre_tarea, descripcion, fecha_vencimiento, estado))
            self.conn.commit()
            print("Tarea creada correctamente.")
        except Exception as e:
            print("Error al crear la tarea:", e)

    def listar_tareas(self, lista):
        self.cursor.execute("SELECT * FROM tareas WHERE nombre_lista = ? ORDER BY fecha_creacion, id DESC",(lista,))
        return self.cursor.fetchall()
    
    def eliminar_tarea(self,id_tarea):
        self.cursor.execute("DELETE FROM tareas WHERE id = ?",(id_tarea,))
        self.conn.commit()

    def editar_estado(self,id_tarea,estado):
        self.cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?",(estado,id_tarea))
        self.conn.commit()

    def editar_tarea(self,id,nombre_tarea,descripcion,fecha_vencimiento,estado):
        self.cursor.execute("UPDATE tareas SET nombre_tarea = ?, descripcion = ?, fecha_vencimiento = ?, estado = ? WHERE id = ?",(nombre_tarea,descripcion,fecha_vencimiento,estado,id))
        self.conn.commit()

##################### APP ######################

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor Tareas - Alejandro Salgado")
        self.pack_propagate(False)
        self.geometry("950x576")
        self.config(bg="black")
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=3)
        self.rowconfigure(0,weight=1)
        self.ListasFrame = ListasFrame(self)
        self.ListasFrame.grid(column=0,row=0,sticky="nsew")
    
    def mostrar_tareas_frame(self,lista):
        if hasattr(self,"TareasFrame"):
            self.TareasFrame.destroy()
        self.TareasFrame = TareasFrame(self,lista)
        self.TareasFrame.grid(column=1,row=0,sticky="snew")

##################### Listas de Tareas ######################

class ListaBoton(tk.Frame):
    def __init__(self,parent,lista,listar):
        super().__init__(parent)
        self.lista = lista
        self.listar = listar
        self.db = db
        tk.Button(self,text=lista,bg="#171717",fg="white",command=lambda: self.mostrar_tareas(lista)).pack(expand=True,fill="x",side="left")
        tk.Button(self,text="X",width=2,bg="#171717",fg="red",command=self.eliminar_lista).pack(side="right")
        self.pack(pady=5,fill="x",padx=10)
    
    def eliminar_lista(self):
        self.db.eliminar_lista(self.lista)
        self.listar()
        master = self.master.master.master
        if hasattr(master, 'TareasFrame'):
            tareas_frame = getattr(master, 'TareasFrame', None)
            if tareas_frame is not None:
                tareas_frame.destroy()
    
    def mostrar_tareas(self,lista):
        self.master.master.master.mostrar_tareas_frame(lista)

class ListarListasTareasFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.db = db
        self.config(bg="#171717")
        self.pack_propagate(False)
        self.listar_listas()
        
    def listar_listas(self):
        for widget in self.winfo_children():
            widget.destroy()
        listas = self.db.listar_listas_tareas()
        for lista in listas:
            self.ListaBoton = ListaBoton(self,lista=lista[1],listar=self.listar_listas)

class NuevaListaFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.db = db
        self.config(bg="#171717")
        self.pack_propagate(False)
        tk.Label(self,text="Lista de Tareas",font=(fuente,20,"bold"),anchor="w",bg="#171717",fg="white").pack(fill="x")
        tk.Label(self,text="Agregar nueva lista",font=(fuente,12),anchor="w",bg="#171717",fg="white").pack(fill="x")
        self.nueva_lista_entry = tk.Entry(self,font=(fuente,12),bg="#171717",fg="white")
        self.nueva_lista_entry.pack(fill="x")
        tk.Button(self,text="Agregar",width=10,bg="#171717",fg="white",command=self.crear_lista).pack(pady=10)

    def crear_lista(self):
        nombre_lista = self.nueva_lista_entry.get()
        if nombre_lista:
            self.db.crear_lista_tareas(nombre_lista=nombre_lista)
            self.nueva_lista_entry.delete(0, 'end')   
            self.master.ListarListasTareasFrame.listar_listas()
        else:
            messagebox.showerror("Error","Debe indicar un nombre de lista.")

class ListasFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg="#171717")
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)
        self.columnconfigure(0,weight=1)
        self.NuevaListaFrame = NuevaListaFrame(self)
        self.NuevaListaFrame.grid(row=0,column=0,sticky="nsew",padx=10)
        self.ListarListasTareasFrame = ListarListasTareasFrame(self)
        self.ListarListasTareasFrame.grid(row=1,column=0,sticky="nsew")

##################### Tareas ######################

class CrearTareaWindow(tk.Toplevel):
    def __init__(self,parent,lista):
        super().__init__(parent)
        self.lista = lista
        self.focus_set()
        #self.grab_set()
        self.pack_propagate(False)
        self.db = db
        self.title("Agregar Tarea")
        self.geometry("400x400")
        self.config(bg="#212121")
        self.rowconfigure((0,4),weight=1)
        self.rowconfigure((5,6),weight=2)
        self.rowconfigure(7,weight=1)
        self.columnconfigure((0,1),weight=2)
        
        tk.Label(self,text="Nueva Tarea",font=(fuente,15,"bold"),anchor="w",bg="#212121",fg="white").grid(column=0,row=0,columnspan=2,padx=5,pady=5)
        tk.Label(self,text="Lista",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=1,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Tarea",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=2,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Fecha de Vencimiento",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=3,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Estado",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=4,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Descripción",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=5,rowspan=2,padx=5,pady=5,sticky="ew")
        
        self.lista_opciones = [lista,]
        self.valor_lista = tk.StringVar(self)
        self.valor_lista.set(lista)
        self.lista_menu = tk.OptionMenu(self,self.valor_lista,*self.lista_opciones)
        self.lista_menu.config(font=(fuente,10),bg="#212121",fg="white",activebackground="#212121",activeforeground="white",borderwidth=0,width=25)
        self.lista_menu.grid(column=1,row=1,padx=5,pady=5)

        self.tarea = tk.Entry(self,text="Tarea",font=(fuente,10),bg="#212121",fg="white",width=30)
        self.tarea.grid(column=1,row=2,padx=5,pady=5)

        self.fecha_vencimiento = DateEntry(self,bg="#212121",fg="white",width=30)
        self.fecha_vencimiento.grid(column=1,row=3,padx=5,pady=5)
        
        self.estado_opciones = ["Pendiente","En progreso","Completado"]
        self.estado_valor = tk.StringVar(self)
        self.estado_valor.set("Pendiente")
        self.estado = tk.OptionMenu(self,self.estado_valor,*self.estado_opciones)
        self.estado.config(font=(fuente,10),bg="#212121",fg="white",activebackground="#212121",activeforeground="white",border=0,width=25)
        self.estado.grid(column=1,row=4,padx=5,pady=5)

        self.descripcion = tk.Text(self,font=(fuente,10),bg="#212121",fg="white",height=2,width=30)
        self.descripcion.grid(column=1,row=5,rowspan=2,padx=5,pady=5)

        tk.Button(self,text="Agregar Tarea",font=(fuente,10),anchor="center",bg="#212121",fg="white",width=15,command=self.crear_tarea_btn).grid(column=0,row=7,columnspan=2,padx=5,pady=5)

    def crear_tarea_btn(self):
        lista = self.lista
        tarea = self.tarea.get()
        descripcion = self.descripcion.get("1.0","end").strip()
        fecha_vencimiento = self.fecha_vencimiento.get_date()
        fecha_vencimiento = fecha_vencimiento.strftime("%Y-%m-%d")
        estado = self.estado_valor.get()
        print(descripcion)
        try:
            self.db.crear_tarea(nombre_lista=lista,nombre_tarea=tarea,descripcion=descripcion,fecha_vencimiento=fecha_vencimiento,estado=estado)
            messagebox.showinfo("Tarea Creada","La tarea se creó con éxito")
        except Exception as e:
            messagebox.showerror(f"Error","La tarea no se pudo crear. Reinicie la aplicación\n{e}")
        self.tarea.delete(0,"end")
        self.master.master.ListarTareasFrame.listar_tareas_f(lista)
        self.destroy()

class NuevaTareaFrame(tk.Frame):
    def __init__(self,parent,lista):
        super().__init__(parent)
        self.lista = lista
        self.db = db
        self.config(bg="#212121")
        self.pack_propagate(False)
        tk.Label(self,text="Tareas",font=(fuente,20,"bold"),anchor="w",bg="#212121",fg="white").pack(fill="x")
        tk.Label(self,text=f"{lista}",font=(fuente,15),anchor="w",bg="#212121",fg="white",width=5).pack(fill="x")
        tk.Button(self,text="Nueva Tarea",bg="#212121",fg="white",anchor="center",width=20,command=lambda: self.crear_tarea(lista)).pack(side="left")

    def crear_tarea(self,lista):
        self.CrearTareaWindow = CrearTareaWindow(self,lista=lista)
        self.wait_window(self.CrearTareaWindow)

class EditarEstadoFrame(tk.Toplevel):
    def __init__(self, parent, tarea):
        super().__init__(parent)
        self.tarea = tarea
        self.title("Cambiar Estado")
        self.geometry("300x200")
        self.focus_set()
        self.db = db
        self.config(bg="#212121")
        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure(0, weight=1)
        
        tk.Label(self, text="Editar Estado", font=(fuente, 15, "bold"), anchor="w", bg="#212121", fg="white").grid(row=0, column=0, sticky="nsew",padx=10)

        self.opc_frame = tk.Frame(self)
        self.opc_frame.grid(row=1, column=0, sticky="nsew")
        
        self.r = tk.StringVar()
        self.r.set("Pendiente")

        tk.Radiobutton(self.opc_frame, text="Pendiente", variable=self.r, value="Pendiente", bg="#212121",fg="white",activebackground="#212121",activeforeground="white",selectcolor="black").pack(anchor="w",fill="x")
        tk.Radiobutton(self.opc_frame, text="En progreso", variable=self.r, value="En progreso", bg="#212121",fg="white",activebackground="#212121",activeforeground="white",selectcolor="black").pack(anchor="w",fill="x")
        tk.Radiobutton(self.opc_frame, text="Completado", variable=self.r, value="Completado", bg="#212121",fg="white",activebackground="#212121",activeforeground="white",selectcolor="black").pack(anchor="w",fill="x")
        tk.Button(self, text="Guardar",bg="#212121",fg="white",activebackground="#212121",activeforeground="white",command=lambda: self.guardar_estado(self.r.get(),tarea)).grid(row=2, column=0, pady=10)

    def guardar_estado(self,estado,tarea):
        try:
            self.db.editar_estado(tarea[0],estado)
            messagebox.showinfo("Estado editado","El estado se editó con éxito")
        except Exception as e:
            messagebox.showerror(f"Error","El estado no se pudo editar. Reinicie la aplicación\n{e}")
        self.master.master.master.master.listar_tareas_f(tarea[1])
        self.destroy()

class EditarTareaFrame(tk.Toplevel):
    def __init__(self,parent,tarea):
        super().__init__(parent)
        self.focus_set()
        self.pack_propagate(False)
        self.id_tarea = tarea[0]
        self.lista = tarea[1]
        self.tarea = tarea
        self.db = db
        self.title("Editar Tarea")
        self.geometry("400x400")
        self.config(bg="#212121")
        self.rowconfigure((0,4),weight=1)
        self.rowconfigure((5,6),weight=2)
        self.rowconfigure(7,weight=1)
        self.columnconfigure((0,1),weight=2)
        
        tk.Label(self,text="Editar Tarea",font=(fuente,15,"bold"),anchor="w",bg="#212121",fg="white").grid(column=0,row=0,columnspan=2,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Lista",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=1,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Tarea",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=2,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Fecha de Vencimiento",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=3,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Estado",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=4,padx=5,pady=5,sticky="ew")
        tk.Label(self,text="Descripción",font=(fuente,10),anchor="w",bg="#212121",fg="white").grid(column=0,row=5,rowspan=2,padx=5,pady=5,sticky="ew")
        
        self.lista_opciones = [tarea[1],]
        self.valor_lista = tk.StringVar(self)
        self.valor_lista.set(tarea[1])
        self.lista_menu = tk.OptionMenu(self,self.valor_lista,*self.lista_opciones)
        self.lista_menu.config(font=(fuente,10),bg="#212121",fg="white",activebackground="#212121",activeforeground="white",borderwidth=0,width=25)
        self.lista_menu.grid(column=1,row=1,padx=5,pady=5)

        self.nombre_tarea = tk.Entry(self,text="Tarea",font=(fuente,10),bg="#212121",fg="white",width=30)
        self.nombre_tarea.grid(column=1,row=2,padx=5,pady=5)
        self.nombre_tarea.insert(0,tarea[2])

        self.fecha_vencimiento = DateEntry(self,bg="#212121",fg="white",width=30,date_pattern='yyyy-mm-dd')
        self.fecha_vencimiento.grid(column=1,row=3,padx=5,pady=5)
        self.fecha_vencimiento.set_date(tarea[5])
        
        self.estado_opciones = ["Pendiente","En progreso","Completado"]
        self.estado_valor = tk.StringVar(self)
        self.estado_valor.set(tarea[6])
        self.estado = tk.OptionMenu(self,self.estado_valor,*self.estado_opciones)
        self.estado.config(font=(fuente,10),bg="#212121",fg="white",activebackground="#212121",activeforeground="white",border=0,width=25)
        self.estado.grid(column=1,row=4,padx=5,pady=5)

        self.descripcion = tk.Text(self,font=(fuente,10),bg="#212121",fg="white",height=2,width=30)
        self.descripcion.grid(column=1,row=5,rowspan=2,padx=5,pady=5)
        self.descripcion.insert("1.0",tarea[3])

        tk.Button(self,text="Editar Tarea",font=(fuente,10),anchor="center",bg="#212121",fg="white",width=15,command=self.editar_tarea_btn).grid(column=0,row=7,columnspan=2,padx=5,pady=5)

    def editar_tarea_btn(self):
        id = self.id_tarea
        lista = self.lista
        nombre_tarea = self.nombre_tarea.get()
        descripcion = self.descripcion.get("1.0","end").strip()
        fecha_vencimiento = self.fecha_vencimiento.get_date()
        fecha_vencimiento = fecha_vencimiento.strftime("%Y-%m-%d")
        estado = self.estado_valor.get()
        print(descripcion)
        try:
            self.db.editar_tarea(id,nombre_tarea,descripcion,fecha_vencimiento,estado)
            messagebox.showinfo("Tarea Editada","La tarea se editó con éxito")
        except Exception as e:
            messagebox.showerror(f"Error","La tarea no se pudo editar. Reinicie la aplicación\n{e}")
        self.nombre_tarea.delete(0,"end")
        self.master.master.master.master.listar_tareas_f(lista)
        self.destroy()

class TareaFrame(tk.Frame):
    def __init__(self,parent,tarea):
        super().__init__(parent,bg="#000000")
        self.tarea = tarea
        self.db = db
        self.rowconfigure((0,2),weight=1)
        self.columnconfigure((0,2),weight=1)
        #tarea
        tk.Label(self,text=tarea[2],font=(fuente,12,"bold"),fg="white",anchor="w",bg="#000000").grid(column=0,row=0,sticky="ew",padx=5)
        #descripcion
        tk.Label(self,text=tarea[3],font=(fuente,10,),fg="white",anchor="w",bg="#000000").grid(column=0,row=1,columnspan=2,sticky="ew",padx=5)
        #fecha_creacion
        tk.Label(self,text=f"📅 {tarea[4]}",font=(fuente,8,),fg="white",anchor="w",bg="#000000").grid(column=0,row=2,sticky="ew",padx=5)
        #fecha_vencimiento
        tk.Label(self,text=f"⏰ {tarea[5]}",font=(fuente,8,),fg="white",anchor="w",bg="#000000").grid(column=1,row=2,sticky="ew",padx=5)
        #estado
        tk.Label(self,text=f"{tarea[6]}",font=(fuente,8,"bold"),fg=color_estado(tarea[6]),anchor="w",bg="#000000").grid(column=1,row=0,sticky="ew",padx=5)
        
        self.eliminar = tk.Label(self,text="Eliminar Tarea",font=(fuente,8),fg="white",anchor="e",bg="#000000")
        self.eliminar.grid(column=2,row=1,sticky="ew",padx=5)
        self.eliminar.bind("<Button-1>",func=lambda e: self.eliminar_tarea_f(tarea))

        self.editar = tk.Label(self,text="Editar Tarea",font=(fuente,8),fg="white",anchor="e",bg="#000000")
        self.editar.grid(column=2,row=2,sticky="ew",padx=5)
        self.editar.bind("<Button-1>",func=lambda e: self.editar_tarea_f(tarea))

        self.editar_estado = tk.Label(self,text=f"{tarea[6]}",font=(fuente,8,"bold"),fg=color_estado(tarea[6]),anchor="w",bg="#000000")
        self.editar_estado.grid(column=1,row=0,sticky="ew",padx=5)
        self.editar_estado.bind("<Button-1>",func=lambda e: self.cambiar_estado(tarea))

    def eliminar_tarea_f(self,tarea):
        respuesta = messagebox.askokcancel("Eliminar tarea","La tarea se eliminará permanentemente")
        if respuesta:
            self.db.eliminar_tarea(tarea[0])
            self.master.master.master.master.ListarTareasFrame.listar_tareas_f(tarea[1])
    
    def cambiar_estado(self,tarea):
        self.EditarEstadoFrame = EditarEstadoFrame(self,tarea)

    def editar_tarea_f(self,tarea):
        self.EditarTareaFrame = EditarTareaFrame(self,tarea)

class ListarTareasFrame(tk.Frame):
    def __init__(self, parent, lista):
        super().__init__(parent,bg="#212121")
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self,bg="#212121", relief="sunken", highlightthickness=0, highlightbackground="red")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas,bg="#212121", highlightthickness=0)

        def set_scroll_frame_width(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)

        self.canvas.bind("<Configure>", set_scroll_frame_width)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.listar_tareas_f(lista)

    def listar_tareas_f(self,lista):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.tareas = db.listar_tareas(lista)
        for tarea in self.tareas:
            TareaFrame(self.scroll_frame, tarea).pack(pady=5, fill="both", padx=10)

class TareasFrame(tk.Frame):
    def __init__(self,parent,lista):
        super().__init__(parent,bg="#212121")
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=4)
        self.columnconfigure(0,weight=1)
        self.lista = lista
        self.pack_propagate(False)
        self.TareasFrame = NuevaTareaFrame(self,lista)
        self.TareasFrame.grid(row=0,column=0,sticky="nsew",padx=10)
        self.ListarTareasFrame = ListarTareasFrame(self,lista=lista)
        self.ListarTareasFrame.grid(row=1,column=0,sticky="nsew",padx=10)


if __name__ == "__main__":
    db = BaseDatos()
    app = App()
    app.mainloop()
