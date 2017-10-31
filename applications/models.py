from django.db import models


class Application(models.Model):
    description = models.CharField(max_length=100)
    device = models.ForeignKey('devices.Device')

    def __str__(self):  # __unicode__ on Python 2
        return self.description


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'configfiles/{1}'.format(instance.id, filename)


class ConfigFile(models.Model):
    application = models.ForeignKey('Application')
    description = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_directory_path, blank=True)


class ConfigValue(models.Model):
    application = models.ForeignKey('Application')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name
