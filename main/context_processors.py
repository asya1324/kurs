from .models import User, AnonymousUser

def current_user(request):
    """
    Injects the 'user' variable into templates based on the
    session 'user_id', fetching from MongoDB.
    """
    uid = request.session.get("user_id")
    
    if not uid:
        return {"user": AnonymousUser()}
    
    try:
        # Fetch the user from Mongo
        user = User.objects.get(id=uid)
        return {"user": user}
    except Exception:
        # If user not found or Mongo error, return AnonymousUser
        return {"user": AnonymousUser()}