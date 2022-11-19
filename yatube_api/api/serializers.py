from posts.models import Comment, Follow, Group, Post, User
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        )

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        return value
