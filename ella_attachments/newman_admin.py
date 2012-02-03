from django.db import models

from ella import newman
from ella.core.models import Publishable

from ella_attachments.models import Attachment, Type


class AttachmentInlineAdmin(newman.NewmanTabularInline):
    model = Attachment.publishables.through
    extra = 0
    suggest_fields = {'attachment': ('name',)}


class AttachmentAdmin(newman.NewmanModelAdmin):
    list_display = ('name', 'type', 'created',)
    list_filter = ('type',)
    prepopulated_fields = {'slug' : ('name',)}
    rich_text_fields = {'small': ('description',)}
    raw_id_fields = ('photo',)
    suggest_fields = {'publishables': ('__unicode__', 'title', 'slug',),}


class TypeAdmin(newman.NewmanModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


def append_inlines():
    publishables = ['%s.%s' % (x._meta.app_label, x._meta.object_name)
                    for x in models.get_models() if issubclass(x, Publishable)]
    newman.site.append_inline(publishables, AttachmentInlineAdmin)


newman.site.register(Attachment, AttachmentAdmin)
newman.site.register(Type, TypeAdmin)

append_inlines()
