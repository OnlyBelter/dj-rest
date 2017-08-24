from django.shortcuts import render
from iss.models import Image
from iss.serializers import ImageSerializer, UserSerializer
from django.contrib.auth.models import User  # for authentication and permissions
from rest_framework import permissions
from iss.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
import json
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

    print('outside of post')

    def perform_create(self, serializer):
        print('here has a post')
        print(dir(self.request))
        print(2)
        print(self.request.data, '==', self.request.POST, '==', self.request.FILES)
        print(3)
        print(type(self.request.data))
        my_dict = dict(self.request.data.iterlists())
        print('my_dict')
        print(my_dict)
        my_image = my_dict['localImage']
        try:
            print(type(my_image))
        except:
            pass
        try:
            with open('/home/xiongx/djcode/dj-rest/images/abc.png', 'wb+') as f_handle:
                for chunk in my_image.chunks():
                    f_handle.write(chunk)
                print('======im f_handle====')
        except:
            print("out of f_handle")
        print(self.request.data.get('fileUrl'))
        if 'formData' in self.request.data:
            _ = json.loads(self.request.data.get('formData', {}))
            serializer.save(userId=_.get('userId', ''), fileUrl=_.get('fileUrl'),
                            des=_.get('des', ''), owner_id=_.get('userId', ''))
        else:
            print('please check formData')
        serializer.save(owner=self.request.user)
