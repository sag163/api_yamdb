from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Category, Genre, Title, Review, Comment, User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

def create(self, validated_data):
        email = validated_data['email']
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        confirmation_code = encode(
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            )
        user = User.objects.create(
            email=email,
            is_active=False,
            confirmation_code=confirmation_code
        )
        send_mail(
            'Ваш код подтверждения',
            confirmation_code,
            'from@example.com',
            [f'{user.email}'],
            fail_silently=False,
        )       
        return self.data['email']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'bio', 'role')



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
     class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField()
        genre = serializers.ReadOnlyField()
        category = serializers.ReadOnlyField()
        class Meta:
                fields = ('id', 'name', 'year', 'genre', 'category')
                model = Title


class ReviewSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')
        class Meta:
                fields = ('title', 'text', 'author', 'score', 'pub_date')
                model = Review


class CommentSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source='author.username')
        class Meta:
                fields = ('review', 'text', 'author', 'pub_date')
                model = Comment

