from django.dispatch import Signal


# Create custom signal
object_viewed_signals = Signal(providing_args=['instance', 'request'])
