from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models.clan_user import ClanUser, ClanUserRoles
from .models.daily_quest import DailyQuest
from .models.diep_gamemode import DiepGamemode
from .models.diep_tank import DiepTank,DiepTankInheritance
from .models.discord_role_points import DiscordRolePoints
from .models.discord_roles import DiscordRole
from .models.discord_roles import SunKnightsBadgeRole
from .models.discord_server import DiscordServer
from .models.guildfight import GuildFight
from .models.guildfight import GuildFightParticipation
from .models.mastery import Mastery
from .models.point_submission import PointsManagerAction,OneOnOneFightSubmission,BasicUserPointSubmission
from .models.help_info import HelpInfo
from .models.points_info import PointsInfo
from .models.tournament import Tournament,TournamentFightConnector


# Register your models here.



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ClanUser
        fields = ('discord_id', 'discord_nickname')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ClanUser
        fields = ('discord_id', 'password', 'discord_nickname', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('discord_id', 'provider', 'discord_nickname', 'is_superuser','is_active')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('discord_id', 'provider', 'password')}),
        ('Personal info', {'fields': ('discord_nickname',)}),
        ('Permissions', {'fields': ('is_superuser','is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('discord_id', 'discord_nickname', 'password1', 'password2')}
         ),
    )
    search_fields = ('discord_id',)
    ordering = ('discord_id',)
    filter_horizontal = ()


class PointsInfoAdmin(admin.ModelAdmin):
    list_display = ('id','user','oldpoints','currentpoints','masterypoints','totalpoints','elo')
    ordering = ('id',)


class DiscordRolePointsAdmin(admin.ModelAdmin):
    list_display = ('discord_role','points')
    ordering = ('-points',)

class DiepTankAdmin(admin.ModelAdmin):
    list_display = ('name','diep_isDeleted','opness','tier')
    ordering = ('name',)

class DiepTankInheritanceAdmin(admin.ModelAdmin):
    list_display = ('me','parent')
    ordering = ('me',)

class DiscordRoleAdmin(admin.ModelAdmin):
    list_display = ('name','can_manage_points','can_manage_wars','is_admin','discord_isDeleted','guild_leader_role','is_clan_guild')
    ordering = ('name',)

class SunKnightsBadgeRoleAdmin(admin.ModelAdmin):
    list_display = ('name','tank')
    ordering = ('name',)

class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ('name','date','last_modifier','helpinfo')
    ordering = ('name',)


# Now register the new UserAdmin...
admin.site.register(ClanUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(DiscordServer)
admin.site.register(DiscordRole,DiscordRoleAdmin)
#admin.site.register(GuildFight)
#admin.site.register(GuildFightParticipation)
admin.site.register(PointsInfo,PointsInfoAdmin)
#admin.site.register(PointsManagerAction)
#admin.site.register(OneOnOneFightSubmission)
#admin.site.register(ClanUserRoles)
admin.site.register(Tournament)
admin.site.register(TournamentFightConnector)
admin.site.register(DiepTank,DiepTankAdmin)
admin.site.register(DiepTankInheritance,DiepTankInheritanceAdmin)
#admin.site.register(Mastery)
#admin.site.register(BasicUserPointSubmission)
admin.site.register(DiepGamemode)
admin.site.register(DailyQuest)
admin.site.register(DiscordRolePoints,DiscordRolePointsAdmin)
admin.site.register(SunKnightsBadgeRole,SunKnightsBadgeRoleAdmin)
admin.site.register(HelpInfo,HelpInfoAdmin)