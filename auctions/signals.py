from django.db.models import signals
from django.dispatch import receiver
from .models import Bid, Listing

# pre_save method signal
@receiver(signals.pre_delete, sender=Bid)
def find_last_bid(sender, instance, **kwargs):
    if instance.bidlisting.curbid == instance:
        allListBids = Bids.objects.filter(listing=instance.listing)
        allListBids = sorted(allListBids, key=lambda bid: bid.ammount, reverse=True)
        lastBid = allListBids[1]
        instance.listing.curbid = lastBid