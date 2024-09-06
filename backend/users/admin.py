from django.contrib import admin
from .models.block_user import BlockedUser
from .models.users import Users


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    pass
