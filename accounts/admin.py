from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from accounts.models import *
from datetime import datetime
# Register your models here.
csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

from social_django.models import Association, Nonce, UserSocialAuth
from core.models import *
from django.utils.html import format_html
from accounts.forms import *
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources

admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)


class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password', 'contact_no')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','gender')}),  
        (_('Proofs'), {'fields': ('proof_liability', 'proof_nonprofit_status')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',
                                       'groups', 'user_permissions', 'type_id')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email','contact_no','first_name', 'last_name', 'type_id','is_active','is_superuser','email_verified'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('user_link', 'email', 'first_name', 'last_name', 'is_active','is_superuser', 'type_id')
    list_display_links = None
    list_filter = ('is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    def user_link(self, obj):
        return format_html('<a href="/admin/accounts/user/{}">{}</a>'.format(obj.id,obj.username))
    
    
    user_link.short_description = 'Username'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            url(r'^(.+)/password/$', self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change'),
        ] + super(UserAdmin, self).get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url,
                                               extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(id))
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(
                    request, form, None)
                self.log_change(request, user, change_message)
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(admin.site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request,
                                self.change_user_password_template or
                                'admin/auth/user/change_password.html',
                                context)


admin.site.register(User, UserAdmin)

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price')
    list_filter = ('description','price')
    search_fields = ('description',)
    ordering = ('price',)

    
@admin.register(EventTypeModel)
class EventTypeModelAdmin(admin.ModelAdmin):
    list_display = ('eventtype', 'eventype_image')

@admin.register(SubscriptionUser)
class SubscriptionUserAdmin(admin.ModelAdmin):
    list_display = ('amount', 'txnid', 'user_subscribe')
    
        
@admin.register(FeedbackPageForm)
class FeedbackPageFormAdmin(admin.ModelAdmin):
    
    def screenshot_image(self, obj):
        return format_html('<a href="/media/{}" target="_blank"><img src="/media/{}"  width="150" height="150" /></a>'.format(obj.feedback_image,obj.feedback_image))
    
    screenshot_image.short_description = 'Screenshot'
    
    list_display = ('user_subscribe', 'note','screenshot_image')

@admin.register(BookingUser)
class BookingUsersAdmin(admin.ModelAdmin):
    list_display = ('room_book', 'start_date', 'end_date', 'amount','status')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('room_book', 'start_date', 'end_date','amount','user_subscribe'),
        }),
    )
     
 
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(BookingUsersAdmin, self).get_fieldsets(request, obj)
    
