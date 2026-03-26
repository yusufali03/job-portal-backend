
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")
        read_only_fields = ("id",)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role")
        read_only_fields = ("id",)

    def validate_role(self, value: str) -> str:
        allowed_roles = {
            User.Role.APPLICANT,
            User.Role.EMPLOYER,
        }

        if value not in allowed_roles:
            raise serializers.ValidationError(
                "You can only register as an applicant or employer."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value: str) -> str:
        self.token = value
        return value

    def save(self, **kwargs) -> None:
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except TokenError as exc:
            raise serializers.ValidationError(
                {"refresh": "Invalid or expired refresh token."}
            ) from exc