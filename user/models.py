from django.db import models
from django.utils import timezone

from configs.base_manager import BaseManager
from configs.settings import BASE_URL
from user.managers import UserManager
from uuid import NAMESPACE_URL, uuid5
from pilkit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(AbstractBaseUser):
    def user_directory_path(self, filename: str) -> str:
        folder_name = uuid5(NAMESPACE_URL, str(self.id))
        return f'{folder_name}/profile/{filename}'

    username_validator = ASCIIUsernameValidator()

    phone_number_regex = RegexValidator(regex=r'^(\+98|98|0)?(9\d{9})$', message='Enter a valid phone number.')

    id = models.BigAutoField(db_column='ID', primary_key=True)
    username = models.CharField(db_column='Username', max_length=15, unique=True, validators=[username_validator],
                                help_text=_('Required. 31 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={'unique': _('A user with this username already exists.')})
    first_name = models.CharField(db_column='FirstName', max_length=15, blank=True)
    last_name = models.CharField(db_column='LastName', max_length=15, blank=True)
    profile_picture = ProcessedImageField(db_column='ProfilePicture', upload_to=user_directory_path, max_length=255,
                                          blank=True, null=True,
                                          processors=[ResizeToFill(400, 400)], format='JPEG', options={'quality': 90})
    phone_number = models.CharField(db_column='PhoneNumber', blank=True, null=True, max_length=15, validators=[phone_number_regex])
    is_banned = models.BooleanField(db_column='IsBanned', default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_male = models.BooleanField(blank=True, null=True)
    bio = models.CharField(max_length=127, default='')
    is_staff = models.BooleanField(db_column='IsStaff', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'User'
        indexes = [
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f'User(id={self.id}, username={self.username})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_profile_picture(self):
        try:
            return f'{BASE_URL}{self.profile_picture.url}'
        except ValueError:
            return None

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


class UserRoom(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    is_pv   = models.BooleanField(db_column='IsPV')
    room_id = models.PositiveBigIntegerField(db_column='RoomID')
    last_message = models.TextField(db_column='LastMessage', blank=True, null=True)
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)
    is_pinned = models.BooleanField(db_column='IsPinned', default=False)
    is_muted = models.BooleanField(db_column='IsMuted', default=False)
    name = models.CharField(db_column='Name', max_length=31)  # TODO
    avatar = models.ImageField(db_column='Avatar', max_length=255)  # TODO
    is_last_from_me = models.BooleanField(db_column='IsLastFromMe', null=True)  # TODO
    # is_unread = models.BooleanField(db_column='IsUnread')  # TODO
    user_id = models.ForeignKey(User, models.CASCADE, db_column='UserID')

    objects = BaseManager()

    class Meta:
        db_table = 'UserRoom'
        indexes = [
            models.Index(fields=['is_pv', 'user_id', 'room_id']),
            models.Index(fields=['last_message', 'user_id']),
            models.Index(fields=['last_message', 'id']),
        ]
        unique_together = ['room_id', 'user_id']

    def __str__(self):
        return f'UserRoom(id={self.id}, user_id={self.user_id.id}, room_id={self.room_id}, is_pv={self.is_pv}, last_message={self.last_message})'

    def update_last_message(self, text: str, is_from_me: bool):
        self.last_message = text
        self.is_last_from_me = is_from_me
        self.timestamp = timezone.now()
        self.save(update_fields=['last_message', 'timestamp', 'is_last_from_me'])
