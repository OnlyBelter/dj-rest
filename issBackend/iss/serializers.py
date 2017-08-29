from rest_framework import serializers
from iss.models import Image
from django.contrib.auth.models import User


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='owner.id')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Image
        fields = ('id', 'created', 'url',
                  'userId', 'des', 'fileUrl', 'owner', 'localImage')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Because 'snippets' is a reverse relationship on the User model,
    it will not be included by default when using the ModelSerializer class,
    so we needed to add an explicit field for it.
    """
    # add new filed to db User
    images = serializers.HyperlinkedRelatedField(many=True,
                                                 view_name='image-detail',
                                                 read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password',
                  'email', 'first_name', 'last_name', 'images')
        write_only_fields = ('password', )
        read_only_fields = ('id', )

    # register users in Django REST Framework:
    # https://stackoverflow.com/a/29867704/2803344

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
