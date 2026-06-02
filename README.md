# MetaStrip

**See what your photos secretly reveal about you — then erase it. 100% in your browser.**

Every photo you take quietly carries hidden data: the **exact GPS coordinates** where it was shot, your **camera and lens**, **timestamps**, and the **software** you edited it with. Post it online and that travels with it.

MetaStrip reads all of it locally, shows you exactly what's exposed, and removes it **losslessly** — it surgically drops the metadata blocks without re-compressing your image, so quality is untouched.

### Why it's different
- **Nothing is uploaded.** No server, no account, no analytics, no upstream API. The entire tool is one static HTML file. Turn off your wifi — it still works.
- **Lossless strip.** JPEGs are not re-encoded. The metadata segments are removed byte-for-byte; the image data is preserved exactly.
- **Honest.** It's open source. Read the source and confirm there's no network call.

### Supports
- **JPEG** — full EXIF/GPS/MakerNote/XMP/IPTC reveal and removal
- **PNG** — text chunks, embedded EXIF, timestamps
- WebP / HEIC — coming

### Use it
👉 **https://thefinalmilkman.github.io/metastrip/**

Or clone and open `index.html` directly. No build step, no dependencies.

### Support
MetaStrip is free forever and harvests nothing. If it kept your location out of a photo and you want to throw something back, you can tip any amount in **USDC (or ETH) on Base**:

`0x0eAFF975a4823c823cfE0c77E9110Ba47291E72A`

Non-custodial — it goes straight to the builder and funds more privacy tools like this.

---

Built by **Arc** · MIT licensed · privacy tools that don't harvest you.
