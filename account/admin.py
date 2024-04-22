from django.contrib import admin

from .models import User,AuthorizationCode,InviteCode


class InviteCodeInline(admin.StackedInline):
    model = InviteCode
    extra = 0

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [InviteCodeInline]
# Register your models here.

@admin.register(AuthorizationCode)
class AuthorizationCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    pass