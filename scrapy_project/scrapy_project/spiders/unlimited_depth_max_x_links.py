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
            yield scrapy.Request(site, self.parse, cb_kwargs={"seed_url": site, "seed_rank": rank})

    def parse(self,
              response,
              href_before_redirects=None,
              href_containing_url=None,
              seed_rank=None,
              seed_url=None,
              seed_url_after_redirects=None,
              http_hrefs_followed_to_arrive_on_current_url=None,
              gathered_http_hrefs_for_this_seed_url=None
              ):
        current_url = response.url
        if seed_url_after_redirects is None:
            seed_url_after_redirects = current_url
        if http_hrefs_followed_to_arrive_on_current_url is None:
            http_hrefs_followed_to_arrive_on_current_url = []
        if gathered_http_hrefs_for_this_seed_url is None:
            gathered_http_hrefs_for_this_seed_url = []

        href_anchors = response.css('a')
        total_href_anchors_found_on_current_url = len(href_anchors)
        self.logger.info("Found %s href_anchors on %s" %
                         (total_href_anchors_found_on_current_url, current_url))

        # check which href_anchors have href attributes and starts with "http"
        # (this gets rid of links to javascript:, mailto:, tel:, #foo etc)
        http_hrefs = []
        for href_anchor in href_anchors:
            href = response.urljoin(
                href_anchor.css('a::attr(href)').get())
            if href.startswith('http'):
                http_hrefs.append(href)

        total_http_hrefs_found_on_current_url = len(http_hrefs)

        # add this visited url to the results
        yield {
            'href_after_redirects': current_url,
            'href_before_redirects': href_before_redirects,
            'href_containing_url': href_containing_url,
            'total_href_anchors_found_on_current_url': total_href_anchors_found_on_current_url,
            'total_http_hrefs_found_on_current_url': total_http_hrefs_found_on_current_url,
            'depth': len(http_hrefs_followed_to_arrive_on_current_url),
            'seed_rank': seed_rank,
            'seed_url': seed_url,
            'seed_url_after_redirects': seed_url_after_redirects,
        }

        if len(http_hrefs) > 0:

            # collect at most 10 random http_hrefs
            if len(http_hrefs) < 10:
                n = len(http_hrefs)
            else:
                n = 10
            at_most_10_random_http_hrefs = random.sample(http_hrefs, n)
            self.logger.info("At most 10 random http_hrefs: %s" %
                             at_most_10_random_http_hrefs)
            for http_href in at_most_10_random_http_hrefs:
                if len(gathered_http_hrefs_for_this_seed_url) < 10:
                    gathered_http_hrefs_for_this_seed_url.append(http_href)
                    yield response.follow(http_href, callback=self.save_successfully_followed_url, cb_kwargs={
                        'href_before_redirects': http_href,
                        'href_containing_url': current_url,
                        'total_href_anchors_found_on_current_url': total_href_anchors_found_on_current_url,
                        'total_http_hrefs_found_on_current_url': total_http_hrefs_found_on_current_url,
                        'depth': len(http_hrefs_followed_to_arrive_on_current_url) + 1,
                        'seed_rank': seed_rank,
                        'seed_url': seed_url,
                        'seed_url_after_redirects': seed_url_after_redirects,
                    })

            # if less than 10 http_hrefs gathered so far... randomly visit a http_href to get more
            if len(gathered_http_hrefs_for_this_seed_url) < 10:
                if len(http_hrefs) > 0:
                    random_http_href = random.choice(http_hrefs)
                    http_hrefs_followed_to_arrive_on_current_url.append(
                        random_http_href)
                    yield response.follow(random_http_href, callback=self.parse, cb_kwargs=dict(
                        href=random_http_href,
                        seed_url=seed_url,
                        http_hrefs_followed_to_arrive_on_current_url=http_hrefs_followed_to_arrive_on_current_url,
                        gathered_http_hrefs_for_this_seed_url=gathered_http_hrefs_for_this_seed_url,
                    ))
            else:
                self.logger.info(
                    "We have gathered 10 http_hrefs for: %s. Ending crawl for that particular seed url" % seed_url)

        else:
            self.logger.info("No http_hrefs to follow on: %s " % (current_url))
            # TODO: Step up one level of http_hrefs followed and attempt to find more http_hrefs?
            # Or do a breadth first from the top instead of depth first?

    def save_successfully_followed_url(self,
                                       response,
                                       href_before_redirects=None,
                                       href_containing_url=None,
                                       total_href_anchors_found_on_current_url=None,
                                       total_http_hrefs_found_on_current_url=None,
                                       depth=None,
                                       seed_rank=None,
                                       seed_url=None,
                                       seed_url_after_redirects=None,
                                       ):
        yield {
            'href_after_redirects': response.url,
            'href_before_redirects': href_before_redirects,
            'href_containing_url': href_containing_url,
            'total_href_anchors_found_on_current_url': total_href_anchors_found_on_current_url,
            'total_http_hrefs_found_on_current_url': total_http_hrefs_found_on_current_url,
            'depth': depth,
            'seed_rank': seed_rank,
            'seed_url': seed_url,
            'seed_url_after_redirects': seed_url_after_redirects,
        }
