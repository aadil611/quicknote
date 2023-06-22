from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Note
from .serializers import NoteSerializer


class NoteModelViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    
    def get_queryset(self):
        # only return notes that belong to the user making the request
        queryset = super().get_queryset().filter(owner=self.request.user)

        # filtering based on content type and notes title
        content_type = self.request.query_params.get('content_type', None)
        if content_type is not None:
            queryset = queryset.filter(content_type=content_type)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)
            
        return queryset



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shared_with_me(request):
    # only return notes that are shared with the user making the request
    queryset = Note.objects.filter(shared_with=request.user)
    serializer = NoteSerializer(queryset, many=True)
    data = serializer.data
    # hide who else the note is shared with
    for note in data:
        note.pop('shared_with')
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share(request):
    note_id = request.data.get('note_id', None)
    if note_id is None:
        return Response({"message": "note_id is required"}, status=400)

    username = request.data.get('username', None)
    if username is None:
        return Response({"message": "recipient username is required to share the notes"}, status=400)
    
    # checking if the note exists and belongs to the user who is sharing it
    try:
        note = Note.objects.get(id=note_id, owner=request.user)
    except Note.DoesNotExist:
        return Response({"message": "Note not found"}, status=404)

    # checking if the user exists
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
    note.shared_with.add(user)
    return Response({"message": "Note shared successfully"})