from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Account

from pdb import set_trace

# Register your models here.
# admin.site.register(Account)

class AccountCreationForm(forms.ModelForm):
    # A form for creating new users. It includes all the required fields, plus a repeated password.
    pw1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    pw2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username',)

    def clean_password2(self):
        pw1 = self.cleaned_data.get('pw1')
        pw2 = self.cleaned_data.get('pw2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError('Passwords don\'t match.')
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)  # "commit=False" means 최종 저장은 나중에
        user.set_password(self.cleaned_data['pw1'])  # cleaned_data: result of the validation
        if commit:
            user.save()
        return user

class AccountChangeForm(forms.ModelForm):
    pw = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'username', 'is_admin')

    def clean_password(self):
        print("worked at line 44")
        return self.initial['pw']

class AccountAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = ('email', 'username', 'is_admin',)
    list_filter = ('is_admin', )
    search_fields = ('email', 'username', )

    fieldsets = [
        # Shouldn't change these field names
        # (None, {'fields': ('email', 'password')}),
        (
            'Account Info',
            {'fields': ('email', )}  # Hide the password
            # {'fields': ('email', 'password',)}
        ),
        (
            'Personal Info',
            {'fields': ('username', )}
        ),
        (
            'Permissions',
            {'fields': ('is_admin',)}
        ),
    ]

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide', ),
                'fields': ('email', 'username', 'pw1', 'pw2'),
            }
        ),
    )
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)

# @admin.register(Account)
# class ClassAdmin(admin.ModelAdmin):
#     list_display = ('email', 'username', 'is_admin',)
#     search_fields = ('email', 'username', )