## Aplicación Gestor de Tareas

### Descripción General

Esta Aplicación Gestor de Tareas, desarrollada en Python utilizando Tkinter y SQLite3, está diseñada para ayudar a los usuarios a gestionar sus tareas de manera efectiva. La aplicación permite a los usuarios crear listas de tareas, añadir tareas a estas listas, marcar tareas como completadas y eliminar tareas cuando sea necesario. Cada tarea puede incluir descripciones detalladas, fechas de vencimiento y el estado actual.

### Características

- **Listas de Tareas**: Los usuarios pueden crear múltiples listas de tareas, cada una capaz de contener una variedad de tareas.
- **Gestión de Tareas**: Añadir nuevas tareas con descripciones detalladas y fechas de vencimiento. Actualizar tareas con un nuevo estado ("Pendiente", "En progreso", "Completado") o modificar sus detalles según sea necesario.
- **Opciones de Visualización de Tareas**: Ver todas las tareas dentro de cualquier lista, mostradas con detalles esenciales como la fecha de creación, la fecha de vencimiento y el estado actual.
- **Interfaz Gráfica Interactiva**: Una interfaz gráfica amigable que incluye botones, entradas de texto y etiquetas para una fácil navegación e interacción.
- **Integración con Base de Datos**: Utiliza SQLite3 para la gestión de datos locales, almacenando todas las tareas y listas dentro de una robusta base de datos.

### Instalación

1. **Prerrequisitos**:
   - Asegúrese de que Python 3.x esté instalado en su sistema.
   - Biblioteca Tkinter, que generalmente está incluida con la instalación estándar de Python.
   - `tkcalendar` para el widget de selección de fecha, que se puede instalar a través de pip:
     ```
     pip install tkcalendar
     ```

2. **Ejecución de la Aplicación**:
   - Descargue el código fuente del repositorio.
   - Navegue al directorio que contiene el código.
   - Ejecute el script usando Python:
     ```
     python gestor_tareas_a_salgado.py
     ```

### Uso

- **Ventana Principal**: Comience creando una nueva lista de tareas usando el botón 'Nueva Lista'.
- **Agregar Tareas**: En la lista seleccionada, añada nuevas tareas usando el botón 'Agregar Tarea', donde puede especificar el nombre de la tarea, la descripción, la fecha de vencimiento y el estado.
- **Editar/Eliminar Tareas**: Cada tarea puede ser editada o eliminada seleccionando las opciones correspondientes junto a cada tarea.
- **Ver Tareas**: Cambie entre listas para ver las tareas asociadas con cada lista.

### Configuración

- La aplicación utiliza una base de datos SQLite local llamada `gestion_tareas.db` para almacenar todos los datos relacionados con las tareas. Esta base de datos se crea y gestiona automáticamente por la aplicación, sin necesidad de configuración manual.
