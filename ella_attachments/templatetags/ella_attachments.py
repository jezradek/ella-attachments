from django import template
from django.utils.datastructures import MultiValueDict

from ella.core.models import Publishable


register = template.Library()


class PublishableDoesNotExist(Exception): pass


class AttachmentsNode(template.Node):

    def __init__(self, publishable, variable):
        self.publishable, self.variable = publishable, variable

    def get_publishable(self, context):
        try:
            publishable = template.Variable(self.publishable).resolve(context)
        except template.VariableDoesNotExist:
            raise PublishableDoesNotExist()
        if isinstance(publishable, Publishable):
            return publishable
        else:
            raise PublishableDoesNotExist()

    def get_attachments(self, context):
        attachments = self.get_publishable(context).attachment_set.select_related(depth=1).all()
        mimetypes_dict = self.get_mimetypes_dict(attachments)
        return {'all': attachments, 'type': mimetypes_dict}

    def get_mimetypes_dict(self, attachments):
        mimetypes = MultiValueDict()
        for attachment in attachments:
            mimetypes.appendlist(attachment.type.slug, attachment)
        return dict(mimetypes)

    def render(self, context):
        try:
            context[self.variable] = self.get_attachments(context)
        except PublishableDoesNotExist:
            pass
        return ''


@register.tag
def attachments(parser, token):
    bits = token.split_contents()

    # if len(bits) != 1 and (len(bits) != 3 or bits[1] != 'for'):
    #     raise template.TemplateSyntaxError(
    #         "{%% attachments %%} or {%% attachments for PUBLISHABLE %%}"
    #     )

    if len(bits) != 5 or bits[1] != 'for' or bits[3] != 'as':
        raise template.TemplateSyntaxError(
            "{%% attachments for PUBLISHABLE as VARIABLE %%}"
        )

    return AttachmentsNode(bits[2], bits[4])
