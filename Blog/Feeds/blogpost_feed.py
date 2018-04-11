from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from Blog.models import Post


class LatestPostsFeed(Feed):
    feed_type = Atom1Feed
    subtitle = "Updates on new blogposts"
    title = "DIY Blog - Django"
    link = reverse_lazy('index')

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
