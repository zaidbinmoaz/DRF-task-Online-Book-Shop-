from api.models import Book, CustomUser, Favourite, Cart
from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "password", "is_author"]
        extra_kwargs = {"password": {"write_only": True}}


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password", "password2", "is_author"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and confirm password does not match"
            )
        return attrs

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "is_author"]


class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user_id = self.context["request"].user.id
        queryset = CustomUser.objects.filter(id=user_id)
        return queryset


class BookAuthorDetail(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "cover_img",
            "publisher",
            "author",
            "in_stock",
            "created",
            "is_favourite",
            "price",
        ]


class BookSerializer(BookAuthorDetail):
    author = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ["user", "book"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["user", "book"]
