import django.dispatch

# dispatched when a donation is successfully charged to its payment method
donation_charged = django.dispatch.Signal(providing_args=["donation"])
