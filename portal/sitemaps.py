from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return [
            'home',
            'courses',
            'placements',
            'services',
            'service_it',
            'service_bpo',
            'service_csr',
            'service_gov',
            'about',
            'contact',
            'career',
            'verify_certificate',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'home': 1.0,
            'courses': 0.95,
            'placements': 0.9,
            'services': 0.85,
            'service_it': 0.8,
            'service_bpo': 0.8,
            'service_csr': 0.8,
            'service_gov': 0.8,
            'about': 0.8,
            'contact': 0.8,
            'career': 0.75,
            'verify_certificate': 0.6,
        }
        return priorities.get(item, 0.5)

    def changefreq(self, item):
        freqs = {
            'home': 'daily',
            'courses': 'weekly',
            'placements': 'weekly',
            'career': 'weekly',
            'services': 'monthly',
            'service_it': 'monthly',
            'service_bpo': 'monthly',
            'service_csr': 'monthly',
            'service_gov': 'monthly',
            'about': 'monthly',
            'contact': 'monthly',
            'verify_certificate': 'monthly',
        }
        return freqs.get(item, 'monthly')
