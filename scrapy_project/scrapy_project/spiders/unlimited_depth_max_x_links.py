# -*- coding: utf-8 -*-
import os
import random

import scrapy


def load_ranked_seed_list(seed_list_arg):
    site_list = os.path.join(os.getcwd(), seed_list_arg)
    if not os.path.isfile(site_list):
        print("%s does not exist." % site_list)
        exit(-1)
    else:
        with open(site_list, 'rb') as f:
            contents = f.read()
    return [tuple(x.split(',')) for x in contents.decode('utf8').strip().split('\n')]


class UnlimitedDepthMaxXLinksSpider(scrapy.Spider):
    name = 'unlimited_depth_max_x_links'

    def start_requests(self):
        ranked_seed_list_csv = getattr(self, 'ranked_seed_list_csv', None)
        if ranked_seed_list_csv is None:
            raise ValueError("ranked_seed_list_csv needs to be supplied")
        ranked_sites = load_ranked_seed_list(ranked_seed_list_csv)
        for rank, site in ranked_sites:
            if "://" not in site:
                site = "http://" + site
            yield scrapy.Request(site, self.parse, cb_kwargs={"seed_url": site})

    def parse(self,
              response,
              seed_url=None,
              seed_url_after_redirects=None,
              links_followed_to_arrive_on_current_url=None,
              gathered_links_for_this_seed_url=None
              ):
        current_url = response.url
        if seed_url_after_redirects is None:
            seed_url_after_redirects = current_url
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
                    yield response.follow(href, callback=self.save_successfully_followed_url, cb_kwargs={
                        'href': href,
                        'current_url': current_url,
                        'total_links_found_on_current_url': len(links),
                        'depth': len(links_followed_to_arrive_on_current_url) + 1,
                        'seed_url': seed_url,
                        'seed_url_after_redirects': seed_url_after_redirects,
                    })

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

    def save_successfully_followed_url(self,
                                       response,
                                       href=None,
                                       current_url=None,
                                       total_links_found_on_current_url=None,
                                       depth=None,
                                       seed_url=None,
                                       seed_url_after_redirects=None,
                                       ):
        yield {
            'parsed_href': response.url,
            'href': href,
            'current_url': current_url,
            'total_links_found_on_current_url': total_links_found_on_current_url,
            'depth': depth,
            'seed_url': seed_url,
            'seed_url_after_redirects': seed_url_after_redirects,
        }
