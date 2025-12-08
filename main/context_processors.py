from .models import User, AnonymousUser

def current_user(request):
    """
    Fetches the MongoDB user based on the session ID
    and makes it available as {{ user }} in templates.
    """
    uid = request.session.get("user_id")
    if not uid:
        return {"user": AnonymousUser()}
    
    try:
        user = User.objects.get(id=uid)
        return {"user": user}
    except Exception:
        return {"user": AnonymousUser()}