"""A sitemap is an XML file that tells search engines the pages of your website, their relevance,
and how frequently they are updated. Using a sitemap will make your site more visible in search engine rankings:
sitemaps help crawlers to index your website's content."""
from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    # Both the changefreq and priority attributes can be either methods or attributes.

    def items(self):
        return Post.published.all()
    # The items() method returns the QuerySet of objects to include in this sitemap.

    def lastmod(self, obj):
        return obj.updated
    # The lastmod method receives each object returned by items() and returns the last time the object was modified

