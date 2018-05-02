# Download images from tumblr blogs with Python/Scrapy

The tool is intended for Machine Learning scientists to
facilitate image dataset creation.

If you find useful Tumblr blog with images of one type
(cats, dogs, cars, people etc.) just fill in blogs' urls
and wait until Scrapy finishes downloading. 

#### Requirements

Python 2.x/3.x
```bash
pip install scrapy
```

#### Usage

Fill in `start_urls.txt` with start pages of Tumblr blogs.

Run:
```bash
scrapy crawl tumblr_spider
```

Images from each blog will be saved into `images/blogname.tumblr.com/`.

Images are saved to a single folder.

Re-run will not download images twice.