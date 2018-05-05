# Download images from tumblr blogs with Python/Scrapy

The tool is intended for Machine Learning scientists to
facilitate image dataset creation.

If you find useful Tumblr blog with images of one type
(cats, dogs, cars, people etc.) just fill in blogs' urls
and wait until Scrapy finishes downloading. 

#### Requirements

Python 3.x
```bash
pip install scrapy
```

#### Settings

You may want to tweak download speed, number of parallel threads and other options
in `spiders/settings.py`. The file is self-explanatory or consult Scrapy docs for
more information.

#### Usage

Fill in `start_urls.txt` with start pages of Tumblr blogs.

Run:
```bash
scrapy crawl tumblr_spider
```

Images from each blog will be saved into `images/blogname.tumblr.com/`.

Images are saved to a single folder.

Re-run will not download images twice.