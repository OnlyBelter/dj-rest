from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User

"""
The first thing we need to get started on our Web API is to provide a way of 
serializing and deserializing the snippet instances into representations such as json. 
We can do this by declaring serializers that work very similar to Django's forms. 

A serializer class is very similar to a Django Form class, and includes similar validation flags on the various fields, 
such as required, max_length and default.
"""


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     file = serializers.FileField(required=False)
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.file = validated_data.get('file', instance.file)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

"""
In the same way that Django provides both Form classes and ModelForm classes, 
REST framework includes both Serializer classes, and ModelSerializer classes.
It's important to remember that ModelSerializer classes don't do anything particularly magical, 
they are simply a shortcut for creating serializer classes:
- An automatically determined set of fields;
- Simple default implementations for the create() and update() methods.
"""


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # add a new field
    owner = serializers.ReadOnlyField(source='owner.username')
    # Because we've included format suffixed URLs such as '.json',
    # we also need to indicate on the highlight field that any format suffixed hyperlinks
    # it returns should use the '.html' suffix.
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',
                                                     format='html')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'file', 'highlight',
                  'linenos', 'language', 'style', 'owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Because 'snippets' is a reverse relationship on the User model,
    it will not be included by default when using the ModelSerializer class,
    so we needed to add an explicit field for it.
    """
    snippets = serializers.HyperlinkedRelatedField(many=True,
                                                   view_name='snippet-detail',
                                                   read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
