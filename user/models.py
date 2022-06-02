from django.db import models

# from configs.base_model import BaseModel
from configs.base_manager import BaseManager
from user.managers import UserManager
from uuid import NAMESPACE_URL, uuid5
from pilkit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(AbstractUser):
    def user_directory_path(self, filename: str) -> str:
        folder_name = uuid5(NAMESPACE_URL, str(self.id))
        return f'{folder_name}/profile/{filename}'

    username_validator = ASCIIUsernameValidator()

    phone_number_regex = RegexValidator(regex=r'^(\+98|98|0)?(9\d{9})$', message='Enter a valid phone number.')
    national_code_regex = RegexValidator(regex='^.{10}$', message='Enter a valid national code. Length has to be 10.')

    id = models.BigAutoField(db_column='ID', primary_key=True)
    username = models.CharField(db_column='Username', max_length=31, unique=True, validators=[username_validator],
                                help_text=_('Required. 31 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _('A user with this username already exists.')})
    profile_picture = ProcessedImageField(db_column='ProfilePicture', upload_to=user_directory_path, max_length=255,
                                          blank=True, null=True,
                                          processors=[ResizeToFill(400, 400)], format='JPEG', options={'quality': 80})
    phone_number = models.CharField(db_column='PhoneNumber', blank=True, null=True, max_length=15, validators=[phone_number_regex])
    is_banned = models.BooleanField(db_column='IsBanned', default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_male = models.BooleanField(blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(db_column='IsStaff', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'User'

    def __str__(self):
        return f'User(id:{self.id}, username:{self.username})'

    @property
    def get_profile_picture(self):
        try:
            return self.profile_picture.url
        except ValueError:
            return None

