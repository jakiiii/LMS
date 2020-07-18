from .signals import user_logged_in


class UserViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(UserViewedMixin, self).get_context_data(*args, **kwargs)
        instance = context.get('user')
        if instance:
            user_logged_in.send(instance.__class__, instance=instance, request=self.request)
        return context
