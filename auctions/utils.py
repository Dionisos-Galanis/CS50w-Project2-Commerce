# from .models import Bid, Listing, Category
# import mimetype
# VALID_IMAGE_MIMETYPES = [
#     "image"
# ]

# def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
#     # http://stackoverflow.com/a/10543969/396300
#     mimetype, encoding = mimetypes.guess_type(url)
#     if mimetype:
#         return any([mimetype.startswith(m) for m in mimetype_list])
#     else:
#         return False


# def findlastbid(lst):
#     maxbid = lst.listbids.all().aggregate(Max('amount'))
#     return lst.listbids.get(amount=maxbid)


# def catchoices():
#     cat_choices = {(None, "None")}
#     for cat in Category.objects.all():
#         cat_choices.add((cat.pk, cat.name))
#     return cat_choices