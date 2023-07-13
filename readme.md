# Crawler core
It's a part of crawler project, for crawl content from website and build ebook.

# Message body structure
```
cmdEnum = {
  "CRAWL_BOOK",
  "CRAWL_CHAPTER",
  "EPUB_BUILD"
}

{
  "cmd": cmdEnum,
  "payload": {}
}
```

# Export env
```
pip list --format=freeze > requirements.txt
```

version: v1.0.0