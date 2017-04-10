#coding:utf-8
from __future__ import unicode_literals

import re
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission, _user_get_all_permissions, _user_has_perm, \
    _user_has_module_perms
from django.contrib import auth
from starpro import settings


# Create your models here.



class PermissionsMixin2(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django's Group and Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'his/her group.'),
        related_name="user_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set", related_query_name="user")

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through his/her
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class AbstractUser2(AbstractBaseUser,PermissionsMixin2):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                              'invalid')
                                ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_cn_full_name(self):
        """
        Returns the last_name plus the first_name, with a space in between.
        """
        full_name = '%s%s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    # def get_profile(self):
    #     """
    #     Returns site-specific profile for this user. Raises
    #     SiteProfileNotAvailable if this site does not allow profiles.
    #     """
    #     warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
    #                   DeprecationWarning, stacklevel=2)
    #     if not hasattr(self, '_profile_cache'):
    #         from django.conf import settings
    #         if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
    #             raise SiteProfileNotAvailable(
    #                 'You need to set AUTH_PROFILE_MODULE in your project '
    #                 'settings')
    #         try:
    #             app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    #         except ValueError:
    #             raise SiteProfileNotAvailable(
    #                 'app_label and model_name should be separated by a dot in '
    #                 'the AUTH_PROFILE_MODULE setting')
    #         try:
    #             model = models.get_model(app_label, model_name)
    #             if model is None:
    #                 raise SiteProfileNotAvailable(
    #                     'Unable to load the profile model, check '
    #                     'AUTH_PROFILE_MODULE in your project settings')
    #             self._profile_cache = model._default_manager.using(
    #                 self._state.db).get(user__id__exact=self.id)
    #             self._profile_cache.user = self
    #         except (ImportError, ImproperlyConfigured):
    #             raise SiteProfileNotAvailable
    #     return self._profile_cache

class DefaultJurisdiction(models.Model):
    organize_id = models.IntegerField()
    role = models.IntegerField()
    jurisdiction_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'default_jurisdiction'

class Jurisdiction(models.Model):
    function_name = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_code = models.CharField(max_length=50, blank=True, null=True)
    parent_true_id = models.CharField(max_length=20)
    level = models.IntegerField()
    organize_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'jurisdiction'


class Organize(models.Model):
    organize_name = models.CharField(max_length=50, blank=True, null=True)
    level = models.IntegerField()
    parent_tree_id = models.CharField(max_length=50)
    parent_tree_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    create_user_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'organize'

    def get_obj_by_tree_id(self, tree_id):
        """
        根据parent_tree_id获取树最后字节点的数据
        """
        o_id = tree_id.split('>')[-1]
        obj = Organize.objects.get(id=o_id)
        return obj




class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    erp_username = models.CharField(max_length=200, blank=True, null=True)
    erp_password = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        managed = False
        db_table = 'profile'
        app_label = 'system'
    ###获取用户erp_id
    # def get_erpid(self):
    #     gateway = GateWayToERP(user=self.erp_username, password=self.erp_password)
    #     return gateway.get_connection()['uid']

class User(AbstractUser2):

    # 判断用户是否选择默认的服务方式1为使用，0为使用自己的账户，-1为未配置，默认为-1
    default_Ups = models.IntegerField(null=True, blank=True, default=-1)
    default_Usps = models.IntegerField(null=True, blank=True, default=-1)
    default_Fedex = models.IntegerField(null=True, blank=True, default=-1)
    #是否允许发送国际订单
    international = models.BooleanField(default = False)
    ##erp_id
    erp_id = models.IntegerField(default=0)
    organize_id = models.IntegerField(blank=True, null=True)
    organize_tree_id = models.CharField(max_length=20, blank=True, null=True)
    user_code = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    force_password = models.CharField(max_length=50)
    create_user_id = models.IntegerField(default=0)
    create_user_name = models.CharField(max_length=50)
    update_time = models.DateTimeField(blank=True, null=True)
    update_user_id = models.IntegerField(blank=True, null=True)
    update_user_name = models.CharField(max_length=50, blank=True, null=True)
    quit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        app_label = 'system'


    def get_profile(self):
        from profile import Profile
        try:
            profile = self.profile
        except:
            profile = Profile(user=self)

        return profile


class UserJurisdiction(models.Model):
    user_id = models.IntegerField()
    jurisdiction_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_jurisdiction'


class UserUpdateRecord(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=25)
    update_user_id = models.IntegerField()
    update_user_name = models.CharField(max_length=25)
    update_time = models.DateTimeField()
    update_type = models.IntegerField()
    details = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_update_record'