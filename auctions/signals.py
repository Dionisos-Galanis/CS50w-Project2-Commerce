from django.db.models import signals
from django.dispatch import receiver
from .models import Bid, Listing

# pre_save method signal
@receiver(signals.pre_delete, sender=Bid)
def find_last_bid(sender, instance, **kwargs):
    if instance.bidlisting.curbid == instance:
        allListBids = Bid.objects.filter(bidlisting=instance.bidlisting)
        allListBids = sorted(allListBids, key=lambda bid: bid.amount, reverse=True)
        if len(allListBids) > 1:
            lastBid = allListBids[1]
            
            print('instance: --------------------------------------------')
            print(instance)
            print('--------------------------------------------')
            print("allListBids: ==============================================")
            for bid in allListBids:
                print(bid)
            print("==============================================")
            print('lastBid: --------------------------------------------')
            print(lastBid)
            print('--------------------------------------------')

            instance.bidlisting.curbid = lastBid
            instance.bidlisting.curprice = lastBid.amount
            instance.bidlisting.save()
        else: # The bid being deleted was the first bid
            instance.bidlisting.curbid = None
            instance.bidlisting.curprice = instance.bidlisting.startbid
            instance.bidlisting.save()