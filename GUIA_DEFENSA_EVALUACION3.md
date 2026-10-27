# Guía rápida de defensa

- **Login:** `Main.py` → `LoginScreen.ingresar()`.
- **JSON:** `services/json_service.py` guarda usuarios y tareas en `data/usuarios.json`.
- **Notificación:** `services/notification_service.py`, llamada después del login y al guardar una tarea.
- **Valor remoto:** `services/remote_config.py`. Aquí el equipo conectará su API/servicio.
- **Sin valor remoto:** se utiliza `DEFAULT_WELCOME_MESSAGE` como respaldo.

## Demo
1. Ingresar un nombre.
2. Mostrar la notificación.
3. Agregar una tarea y guardarla.
4. Mostrar `data/usuarios.json`.
5. Cerrar/reabrir y comprobar persistencia.
6. Conectar/probar el servicio remoto.
7. Provocar un fallo controlado y mostrar el valor por defecto.

## Modificación en vivo
Cambiar el texto de `DEFAULT_WELCOME_MESSAGE` o de una notificación, ejecutar y comprobar el resultado.
