from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser, FriendList, PointsLog


class UserCreationForm(forms.ModelForm):
    """New user creation form"""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["username"]

    def clean_password2(self):
        # Password match ?
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Update user form"""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["username", "password", "level", "experience_points", "shop_points", "title", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # Change and Add UserAdmin forms
    form = UserChangeForm
    add_form = UserCreationForm

    # UserAdmin displayed fields in admin view
    list_display = ["username", "id", "level", "experience_points", "shop_points", "title", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        ("Gamification Info", {"fields": ["level", "experience_points", "shop_points", "title"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # Admin fieldsets
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []


class FriendListInline(admin.TabularInline):
    model = FriendList.friends.through
    verbose_name = "friend"
    verbose_name_plural = "friends"


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [FriendListInline]
    list_display = ('username', 'email', 'location', 'points_accumulated', 'points_spendable')
    search_fields = ('username', 'location')


# Register user types
admin.site.register(CustomUser, UserAdmin)
# Unregister groups as they aren't used by the custom types
admin.site.unregister(Group)
admin.site.register(FriendList)
admin.site.register(PointsLog)
