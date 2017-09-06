from django.shortcuts import render
from iss.models import Image
from iss.serializers import ImageSerializer, UserSerializer
from django.contrib.auth.models import User  # for authentication and permissions
from rest_framework import permissions
from iss.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from django.core.files.storage import default_storage
from django.conf import settings
import json
import os
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    Here we've used the ReadOnlyModelViewSet class to automatically provide the default 'read-only' operations.
    We're still setting the queryset and serializer_class attributes exactly as we did when we were using regular views,
    but we no longer need to provide the same information to two separate classes.
    """

    # permission_classes = (permissions.IsAdminUser, )
    permission_classes = (permissions.AllowAny, )
    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        if self.request.user.is_superuser:
            queryset = User.objects.all()
        return queryset
    # get_queryset(queryset)
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

    print('outside of post')

    def perform_create(self, serializer):
        print('here has a post')
        """
        self.request.data contains all data (strings and files), QueryDict
        self.request.POST contains all strings, QueryDict
        self.request.FILES contains all files, MultiValueDict
        """
        strings_dic = dict(self.request.POST.iterlists())
        print(strings_dic)
        files_dic = dict(self.request.FILES)
        my_image = files_dic['localImage'][0]
        if strings_dic:
            _ = strings_dic
            serializer.save(userId=_.get('userId', '')[0],
                            fileUrl=_.get('fileUrl')[0],
                            des=_.get('des', '')[0],
                            owner_id=_.get('userId', '')[0],
                            localImage=my_image)
        else:
            print('please check formData')
            serializer.save(owner=self.request.user)
