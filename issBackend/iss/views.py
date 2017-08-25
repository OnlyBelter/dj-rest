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
        """
        self.request.data contains all data (strings and files), QueryDict
        self.request.POST contains all strings, QueryDict
        self.request.FILES contains all files, MultiValueDict
        """
        strings_dic = dict(self.request.POST.iterlists())
        print(strings_dic)
        files_dic = dict(self.request.FILES)

        my_image = files_dic['localImage'][0]
        store_path = ''
        current_site = self.request.META['HTTP_HOST']
        print(current_site.domain)
        try:
            print(my_image.name)
            # print(settings.STATICFILES_DIRS)
            store_dir = settings.STATICFILES_DIRS[1][1]
            print(store_dir)
            store_path = os.path.join(store_dir, my_image.name)
            store_url = os.path.join(current_site, settings.STATIC_URL, settings.STATICFILES_DIRS[1][0], my_image.name)
            print(store_url)
        except:
            pass
        try:
            # https://stackoverflow.com/a/30195605/2803344
            with open(store_path, 'wb+') as f_handle:
                for chunk in my_image.chunks():
                    f_handle.write(chunk)
                print('======im f_handle====')
        except:
            print("out of f_handle")
        print(self.request.data.get('fileUrl'))
        if strings_dic:
            print(strings_dic)
            _ = strings_dic
            if my_image:
                serializer.save(userId=_.get('userId', '')[0], fileUrl=store_url,
                            des=_.get('des', '')[0], owner_id=_.get('userId', '')[0])
            else:
                serializer.save(userId=_.get('userId', '')[0], fileUrl=_.get('fileUrl')[0],
                            des=_.get('des', '')[0], owner_id=_.get('userId', '')[0])
        else:
            print('please check formData')
            serializer.save(owner=self.request.user)
