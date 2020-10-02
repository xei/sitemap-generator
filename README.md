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
If you only have one sitemap file, `https://example.com/sitemap.xml` is the address of that file although  you have to know that each sitemap file should be less that `50MB` in size and it should have `50000` urls at last. So you may need more than just one sitemap file. In this case, `https://example.com/sitemap.xml` refers to a sitemap index file including all sitemaps addresses.

### A sample of sitemap index file
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
`sitemap.xml` file in the repository is quite simiar to the above, but because `daily-available-products-sitemap.xml` file is going to be generated/updated automatically, `lastmod` attribute in the second index is replaced by a variable named `${LAST_MODIFICATION_DATE_DAILY_AVAILABLE_PRODUCTS}`. We can use this variable to inject the **modification time** when updating the `daily-available-products-sitemap.xml` file automatically.

`important-pages-sitemap.xml` file however is a static sitemap file that does not change regularly, so a fix date is used for it. We should update it manually when it is updating.

### A sample of sitemap XML file
Each site XML file which is indexed in the `sitemap.xml` has a structure like bellow:
```
<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

	<url>
		<loc>https://www.example.com/mag</loc>
	</url>

	<url>
		<loc>https://www.example.com/about-us.html</loc>
		<lastmod>2020-09-29</lastmod>
        	<changefreq>monthly</changefreq>
        	<priority>0.8</priority>
	</url>
	
	<url>
		<loc>https://www.example.com/faq.html</loc>
		<lastmod>2020-09-29</lastmod>
        	<changefreq>daily</changefreq>
		<priority>0.4</priority>
	</url>
	
	<url>
		<loc>https://www.inpinapp.com/jobs.html</loc>
		<lastmod>2020-09-29</lastmod>
        	<changefreq>monthly</changefreq>
        	<priority>0.5</priority>
	</url>
	
</urlset>
```
`loc` is a mandatory attribute but `lastmod`, `changefreq` and `priority` are optional attributes which are not important for Google at the time. However, some web crawlers might use them.

In addition, some XHTML tags can be used to introduce [canonical urls](https://support.google.com/webmasters/answer/189077?hl=en) (e.g. localized versions of a page):
```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
	xmlns:xhtml="http://www.w3.org/1999/xhtml">
    
	<url>
		<loc>https://www.example.com/fa/product/1234</loc>
		<lastmod>2020-09-29</lastmod>
		<xhtml:link
			rel="alternate"
			hreflang="fa"
			href="https://www.inpinapp.com/fa/product/1234"/>
		<xhtml:link
			rel="alternate"
			hreflang="en"
			href="https://www.inpinapp.com/en/product/1234"/>
	</url>
    
</urlset>
```

## Generate a sitemap file automatically from database
Sometimes we need to generate/update a sitemap file automatically and regularly (e.g. daily) using information from production database. A python script template named `generate_available_products_sitemap.py` is provided in order to do this. Tailor it to your need and your usecase, then run it to retrieve data from database and generate the updated sitemap file.
```
$ git clone https://github.com/xei/sitemap-generator.git
$ cd sitemap-generator

$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt

$ python generate_available_products_sitemap.py $DB_USER_NAME '$DB_PASSWORD'
```
Database password is wrapped inside quote marks because in may be tailed with especial characters like '&'.

The script can be invoked from a manual/automatic `CI/CD job` or a `cron job`. A `gitlab-ci.yml` file is included to the repository in order to be used in a Gitlab CI/CD pipeline.

### Ping Google to know about a change in sitemap files
When a new sitemap XML file is generated, it must be serving from the site domain and also Google should be notified about this change. To ask Google to crawl the new sitemap files call the following API:
```
$ curl --location --request GET 'http://www.google.com/ping?sitemap=https://example.com/sitemap.xml'
```
Note: don't call the above API like a spammer!
