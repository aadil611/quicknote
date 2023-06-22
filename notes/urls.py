from rest_framework.routers import DefaultRouter
from django.urls import path,include

from .views import NoteModelViewSet, shared_with_me, share

router = DefaultRouter()
router.register(r"notes", NoteModelViewSet, basename="notes")

urlpatterns = [
        path('notes/shared_with_me/', shared_with_me, name='shared_with_me' ),
        path('notes/share/', share, name='share'),
        path('', include(router.urls)),
    ]