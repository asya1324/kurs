from django.urls import path, include

# ---------------------------------------------------------
# ADMIN DISABLED:
# We removed "path('admin/', admin.site.urls)" 
# because Django Admin does not work with MongoDB/MongoEngine.
# ---------------------------------------------------------

urlpatterns = [
    path('', include('main.urls')),
]


