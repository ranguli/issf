from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

from issf_base.models import Country


class UserProfile(AbstractUser):
    """
    Custom model for User Profiles.
    """
    initials = models.CharField(blank=True, max_length=10)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    # # set true when creating user accounts on their behalf, so that they get prompted to
    # change password after verification

    class Meta:
        managed = True
        db_table = 'user_profile'
        ordering = ['username']

    def __str__(self) -> str:
        """
        Generates a string representation of this user profile.

        :return: The string representation.
        """
        return '%s (%s %s %s)' % (self.username, self.first_name, self.initials, self.last_name)
