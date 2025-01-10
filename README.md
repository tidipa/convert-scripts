# convert-scripts
Scripts to convert various editions of the Tipiṭaka into Markdown

```sh
python scan_sc_html.py | sed "s/id='[^']*'/id='X'/g" | sed "s/data-counter='[^']*'/data-counter='X'/g" | sed "s/value='[^']*'/value='X'/g" | sort | uniq
```
