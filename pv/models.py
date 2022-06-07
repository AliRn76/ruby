from django.db import models
from django.db.models import Q

from configs.base_manager import BaseManager
from pv.exceptions import PVAlreadyExists
from user.models import User


class PV(models.Model):
    id                  = models.AutoField(db_column='ID', primary_key=True)
    user1_is_blocked    = models.BooleanField(db_column='User1IsBlocked', default=False)
    user2_is_blocked    = models.BooleanField(db_column='User2IsBlocked', default=False)
    user1_is_deleted    = models.BooleanField(db_column='User1IsDeleted', default=False)
    user2_is_deleted    = models.BooleanField(db_column='User2IsDeleted', default=False)
    user1_unread_count  = models.IntegerField(db_column='User1UnreadCount', default=0)
    user2_unread_count  = models.IntegerField(db_column='User2UnreadCount', default=0)
    user1_is_favorite   = models.BooleanField(db_column='User1IsFavorite', default=False)
    user2_is_favorite   = models.BooleanField(db_column='User2IsFavorite', default=False)

    date_created        = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    user1_id            = models.ForeignKey(User, models.DO_NOTHING, related_name='user1_id', db_column='User1ID')
    user2_id            = models.ForeignKey(User, models.DO_NOTHING, related_name='user2_id', db_column='User2ID')

    objects = BaseManager()

    class Meta:
        db_table = 'PV'
        unique_together = ('user1_id', 'user2_id')

    @classmethod
    def check_user_access(cls, user_id, pv_id):
        q = Q(user1_id=user_id) | Q(user2_id=user_id)
        return cls.objects.filter(q, id=pv_id).first()

    @classmethod
    def create_pv(cls, user1, user2):
        q = Q(user1_id=user1.id, user2_id=user2.id) | Q(user1_id=user2.id, user2_id=user1.id)
        pv = cls.objects.filter(q).first()
        if pv:
            raise PVAlreadyExists
        return cls.objects.create(user1_id=user1, user2_id=user2)


class PVMessage(models.Model):
    id              = models.AutoField(db_column='ID', primary_key=True)
    text            = models.TextField(db_column='Text', blank=True, null=True)
    image           = models.CharField(db_column='Image', max_length=255, blank=True, null=True)
    is_reply        = models.BooleanField(db_column='IsReply', default=False)
    date_added      = models.DateTimeField(db_column='DateAdded', auto_now_add=True)
    date_updated    = models.DateTimeField(db_column='DateUpdated', auto_now=True)
    pv_id           = models.ForeignKey(PV, models.DO_NOTHING, db_column='PVID', blank=True, null=True)
    user_id         = models.ForeignKey(User, models.DO_NOTHING, db_column='UserID')
    pv_message_id   = models.ForeignKey('self', models.DO_NOTHING, db_column='PvMessageID', blank=True, null=True)

    objects = BaseManager()

    def dict(self):
        _dict = dict()
        for field in self.__dict__:
            if not field.startswith('_'):
                if field.startswith('date') or field == 'timestamp':
                    _dict[field] = self.__dict__[field].isoformat()
                else:
                    _dict[field] = self.__dict__[field]
        return _dict

    class Meta:
        db_table = 'PVMessage'
        indexes = [
            models.Index(fields=['user_id', 'pv_id']),
        ]



