from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ella.core.models import Publishable
from ella.photos.models import Photo


UPLOAD_TO = getattr(settings, 'ATTACHMENTS_UPLOAD_TO', 'attachments/%Y/%m/%d')


class Type(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    mimetype = models.CharField(_('Mime type'), max_length=100,
            help_text=_('consult http://www.sfsu.edu/training/mimetype.htm'))

    class Meta:
        ordering=('name',)
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __unicode__(self):
        return self.name

class Attachment(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)

    photo = models.ForeignKey(Photo, blank=True, null=True, verbose_name=_('Photo'), related_name='photos')
    publishables = models.ManyToManyField(Publishable, blank=True, null=True,
                                          verbose_name=_('Publishables'))

    description = models.TextField(_('Description'))

    created = models.DateTimeField(_('Created'), default=datetime.now, editable=False)

    attachment = models.FileField(_('Attachment'), upload_to=UPLOAD_TO)

    type = models.ForeignKey(Type, verbose_name=_('Attachment type'))

    class Meta:
        ordering=('created',)
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __unicode__(self):
        return self.name
