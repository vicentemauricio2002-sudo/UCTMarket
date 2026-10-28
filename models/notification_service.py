"""Notificaciones locales. Si el sistema no las soporta, la app sigue funcionando."""
def show_notification(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name="UCTMarket", timeout=4)
        return True
    except Exception as exc:
        # Fallback útil para equipos donde plyer o el backend no esté disponible.
        print(f"[Notificación no disponible] {title}: {message} ({exc})")
        return False
