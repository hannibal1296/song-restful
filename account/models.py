from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Email Error')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        print("It worked.")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=email, password=password, username=username)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='이메일 주소', max_length=255, unique=True)
    username = models.CharField(max_length=20, unique=True)

    email_authenticated = models.BooleanField(default=False, help_text='이메일 인증을 했나요?')
    is_admin = models.BooleanField(default=False)
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def get_username(self):
        return self.username

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


'''
<AbstractBaseUser로 부터 상속받기 때문에 반드시 정의해야 할 규칙>
1. USERNAME_FIELD : 고유 식별자로 분류하는 필드가 존재해야함 ex)unique=True
2. REQUIRED_FIELDS : createsuperuser 명령을 통해 사용자를 작성할 때 프롬프트 될 필드 이름의 목록
3. is_active : 사용자가 활성상태로 있는지 구분하기 위함
4. get_full_name : 사용자를 식별하는 문자열
5. get_short_name : 사용자를 식별하는 문자열. 일반적으로 이름(firstname)을 뜻함
'''
