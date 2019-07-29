# -*- coding: utf-8 -*-
import random

import scrapy


class UnlimitedDepthMaxXLinksSpider(scrapy.Spider):
    name = 'unlimited_depth_max_x_links'
    start_urls = ['http://example.com/']

    def parse(self,
              response,
              seed_url=None,
              links_followed_to_arrive_on_current_url=None,
              gathered_links_for_this_seed_url=None
              ):
        current_url = response.url
        if seed_url is None:
            seed_url = current_url
        if links_followed_to_arrive_on_current_url is None:
            links_followed_to_arrive_on_current_url = []
        if gathered_links_for_this_seed_url is None:
            gathered_links_for_this_seed_url = []

        links = response.css('a')
        self.logger.info("Found %s links on %s" % (len(links), current_url))

        if len(links) > 0:

            # collect at most 10 random links
            if len(links) < 10:
                n = len(links)
            else:
                n = 10
            at_most_10_random_links = random.sample(links, n)
            self.logger.info("At most 10 random links: %s" %
                             at_most_10_random_links)
            for link in at_most_10_random_links:
                if len(gathered_links_for_this_seed_url) < 10:
                    href = response.urljoin(link.css('a::attr(href)').get())
                    gathered_links_for_this_seed_url.append(href)
                    yield {
                        'href': href,
                        'current_url': current_url,
                        'total_links_found_on_current_url': len(links),
                        'depth': len(links_followed_to_arrive_on_current_url)+1,
                        'seed_url': seed_url,
                    }

            # if less than 10 links gathered so far... randomly visit a link to get more
            if len(gathered_links_for_this_seed_url) < 10:
                if len(links) > 0:
                    random_link = random.choice(links)
                    links_followed_to_arrive_on_current_url.append(
                        response.urljoin(random_link.css('a::attr(href)').get()))
                    yield response.follow(random_link, callback=self.parse, cb_kwargs=dict(
                        seed_url=seed_url,
                        links_followed_to_arrive_on_current_url=links_followed_to_arrive_on_current_url,
                        gathered_links_for_this_seed_url=gathered_links_for_this_seed_url,
                    ))
            else:
                self.logger.info(
                    "We have gathered 10 links for: %s. Ending crawl for that particular seed url" % seed_url)

        else:
            self.logger.info("No links to follow on: %s " % (current_url))
            # TODO: Step up one level of links followed and attempt to find more links?
            # Or do a breadth first from the top instead of depth first?
