from django.shortcuts import render
from iss.models import Image
from iss.serializers import ImageSerializer, UserSerializer
from django.contrib.auth.models import User  # for authentication and permissions
from rest_framework import permissions
from iss.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    Here we've used the ReadOnlyModelViewSet class to automatically provide the default 'read-only' operations.
    We're still setting the queryset and serializer_class attributes exactly as we did when we were using regular views,
    but we no longer need to provide the same information to two separate classes.
    """
    permission_classes = (permissions.IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'username')


class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.

    We're going to replace the SnippetList,
    SnippetDetail and SnippetHighlight view classes with a single class.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    # permission_classes = (permissions.AllowAny, IsOwnerOrReadOnly)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        if 'formData' in self.request.data:
            _ = self.request.data.get('formData', {})
            serializer.save(userId=_.get('userId'), fileUrl=_.get('fileUrl'),
                            des=_.get('des'))
        else:
            print('please check formData')
        serializer.save(owner=self.request.user)
