from ella import newman

from ella_attachments.models import Attachment, Type


class AttachmentAdmin(newman.NewmanModelAdmin):
    list_display = ('name', 'type', 'created',)
    list_filter = ('type',)
    prepopulated_fields = {'slug' : ('name',)}
    rich_text_fields = {'small': ('description',)}
    raw_id_fields = ('photo',)
    suggest_fields = {'publishables': ('__unicode__', 'title', 'slug',),}


class TypeAdmin(newman.NewmanModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


newman.site.register(Attachment, AttachmentAdmin)
newman.site.register(Type, TypeAdmin)
