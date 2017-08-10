# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers

# 序列化
# Notice that we're using hyperlinked relations in this case, with HyperlinkedModelSerializer.
# You can also use primary key and various other relationships, but hyperlinking is good RESTful design.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        # 这里相当于数据库的名称及其字段
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('ure', 'name')

