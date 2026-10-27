def show_notification(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name='UCTMarket', timeout=4)
        return True
    except Exception:
        return False
