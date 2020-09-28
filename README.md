# sitemap-generator
A template Python script responsible for generating sitemap files automatically using information from production database.

## Sitemap
As an SEO specialist, you want all your important website/webapp pages (URLs) to be indexed by search engines, especially Google. Search engines crawlers need to see them somewhere, for example an external link from other websites can lead the crawlers to find one of your important pages and index it. In the other hand, when a search engine crawler visits a page in your site, it will traverse (and maybe index) all its internal links. If a page is rendered in a server in advance (server-side rendering), it usually contains internal links that can be found and indexed by search engines. However, if the page is going to be rendered in users browser (client-side rendering), like when you have a single-page application (SPA), there is no any pre-exist internal link and URL changes only when the user interacts with webapp (dynamic pages).

[Sitemap](https://en.wikipedia.org/wiki/Site_map), a structured pages (URLs) listings intended for web crawlers such as search engines, can be useful to introduce undiscoverable links, their importance, their last modification times and also their canonical URLs, to web crawlers. You can create a full map of your site or just put the important URLs in some XML sitemap files and upload them to [Google Search Console](https://search.google.com/search-console/about) in order to be crawled by Google.

If you care about other search engines and crawlers, you can instead serve the XML sitemap files from the site domain and reference to their address from `robots.xml` file as bellow.

```
User-agent: *
Disallow: /*/404
Disallow: /*/error
Disallow: /admin/*

Sitemap: https://example.com/sitemap.xml
```
If you only have one sitemap file, `https://example.com/sitemap.xml` is the address of that file although  you have to know that each sitemap file should be less that `50MB` in size and it should have `50000` urls at last. So you may need more than just one sitemap file. In this case, `https://example.com/sitemap.xml` refers to an index XML file including all sitemaps addresses.

## A sample of index XML file
``` 
<?xml version="1.0" encoding="UTF-8"?>

    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    
        <sitemap>
            <loc>https://www.example.com/important-pages-sitemap.xml</loc>
            <lastmod>2020-09-29</lastmod>
        </sitemap>
        
        <sitemap>
            <loc>https://www.example.com/daily-available-products-sitemap.xml</loc>
            <lastmod>2020-09-29</lastmod>
        </sitemap>
        
    </sitemapindex>
```
