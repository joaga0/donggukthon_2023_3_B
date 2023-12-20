from django.db import models
from badge.models import Badge
from fishbread.models import Fishbread
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

def create_superuser(self, email=None, password=None, **extra_fields):
    """
    주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
    단, 최상위 사용자이므로 권한을 부여
    """
    superuser = self.create_user(
        email=email,
        password=password,
    )
    
    superuser.is_staff = True
    superuser.is_superuser = True
    superuser.is_active = True
    
    superuser.save(using=self._db)
    return superuser

# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    # name = models.CharField(max_length=100, null=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    # holder = models.CharField(max_length=20, null=True)
    # bankname = models.CharField(max_length=20, null=True)
    # account_num = models.CharField(max_length=100, null=True)
#     # date_list = ArrayField(models.CharField(max_length=20), blank=True)
#     # date_list = models.CharField(max_length=30)
    # date = models.CharField(max_length=30, null=True)
    # badge = models.ManyToManyField(Badge, blank=True)
    # fishbread = models.ManyToManyField(Fishbread, blank=True)

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'email'


# class UserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """

#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)
    
# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, max_length=255)
#     name = models.CharField(max_length=100)
#     holder = models.CharField(max_length=20)
#     bankname = models.CharField(max_length=20)
#     account_num = models.CharField(max_length=100)
#     # date_list = ArrayField(models.CharField(max_length=20), blank=True)
#     # date_list = models.CharField(max_length=30)
#     date = models.CharField(max_length=30)
#     badge = models.ManyToManyField(Badge, blank=True)
#     fishbread = models.ManyToManyField(Fishbread, blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def __str__(self):
#         return self.email





# class UserManager(BaseUserManager):
#     # 일반 user 생성
#     def create_user(self, email, name, password=None, **extra_fields):
#         if not email:
#             raise ValueError('must have user email')
#         if not name:
#             raise ValueError('must have user name')
#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     # 관리자 user 생성
#     def create_superuser(self, email, name, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, name, password, **extra_fields)

# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     def has_module_perms(self, app_label):
#         return self.is_staff

#     def has_perm(self, perm, obj=None):
#         return self.is_staff

#     def __str__(self):
#         return self.email