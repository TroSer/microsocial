from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#from person.forms import UserChangeForm, UserCreationForm
from person.models import User


# class CustomUserAdmin(UserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#     list_display = ('email', 'name', 'is_staff')
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'name', 'password1', 'password2')
#         }),
#     )
#     fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password')
#         }),
#         ('Personal info', {
#             'classes': ('wide',),
#             'fields': ('name', )
#         }),
#         ('Permissions', {
#             'classes': ('wide',),
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
#         }),
#         ('Important dates', {
#             'classes': ('wide',),
#             'fields': ('last_login', 'date_joined')
#         }),
#     )
#     search_fields = ('email', 'name')
#     ordering = ('email',)
#
# admin.site.register(User, CustomUserAdmin)

