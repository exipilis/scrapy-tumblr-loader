### Loader of Tumblr blogs' images

#### Requirements

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

Re-run will not download images twice.