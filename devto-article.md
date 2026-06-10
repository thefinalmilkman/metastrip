Last week I dropped a photo from my phone into a hex editor, scrolled about 30 bytes in, and found the exact latitude and longitude of the room I was standing in. Six decimal places. Accurate to a few meters.

I had not tagged a location. I had not posted anything. The camera just *wrote it down*, the way it does for every photo, on every phone, by default.

Here is how that works, why "just crop it" does nothing, and how to actually remove it — including a tiny tool I built that does it entirely in your browser with zero uploads.

## Where the data hides

A JPEG is not one blob. It is a stream of **segments**, each introduced by a marker byte `0xFF` followed by a type byte. The image you see lives in the scan data after the `Start of Scan` marker (`0xFFDA`). Everything before it is metadata.

The interesting one is **APP1** (`0xFFE1`). It holds an Exif block, which is really a little-endian or big-endian TIFF structure with its own image file directories (IFDs). Walk the IFD entries and you get tags like:

- `0x010F` Make, `0x0110` Model — your exact camera/phone
- `0x9003` DateTimeOriginal — when, in your local time
- `0xA434` LensModel — even the lens
- `0x8825` — a pointer to the **GPS IFD**

Follow that GPS pointer and you find `GPSLatitude` and `GPSLongitude`, each stored as three RATIONAL values — degrees, minutes, seconds — plus a `GPSLatitudeRef` of `N`/`S` and `GPSLongitudeRef` of `E`/`W`. Convert it:

```js
const dd = deg + min/60 + sec/3600;
const signed = (ref === "S" || ref === "W") ? -dd : dd;
```

That's your home, rendered as a number, riding inside a picture of your cat.

## Why cropping and editing don't save you

This is the part most people get wrong. The metadata is **structurally separate** from the pixels. When you crop, rotate, or draw on a photo in most apps, you change the scan data — the APP1 block comes along untouched. Plenty of "edited" screenshots online still carry the original capture's GPS.

Worse: some workflows that *do* strip metadata do it by **re-encoding** the whole image through a canvas. That drops the metadata, yes — but it also re-compresses your JPEG, throwing away real image quality every time. You traded your privacy fix for visible artifacts.

## The clean way: surgical removal

You don't need to re-encode anything. You walk the segment list and copy every byte **except** the metadata segments:

```js
// keep everything; drop APP1(Exif/XMP), APP13(IPTC), APP14(Adobe), COM
while (p < d.length - 1) {
  if (d[p] !== 0xFF) { p++; continue; }
  const marker = d[p + 1];
  if (marker === 0xDA) break;            // start of scan: image data follows
  const len = (d[p+2] << 8) | d[p+3];    // segment length
  const isMeta = marker === 0xE1 || marker === 0xED ||
                 marker === 0xEE || marker === 0xFE;
  if (!isMeta) keepRange(p, p + 2 + len);
  p += 2 + len;
}
// then append from the scan marker to EOF unchanged
```

The output is byte-for-byte identical in the parts that matter. The pixels are never touched. PNG works the same way — its metadata lives in `tEXt`, `zTXt`, `iTXt`, `tIME`, and `eXIf` chunks that you simply don't copy forward.

## A tool that does exactly this, locally

I packaged the parser and the lossless stripper into a single static page. Drop photos in, it shows you everything they're leaking — GPS on a map link, device, lens, timestamps, editing trail — and gives you a clean copy with the metadata surgically removed.

The important part: **nothing is uploaded.** There is no server and no analytics. The whole thing is one HTML file; you can turn off your wifi and it still works, and you can read every line of the source.

👉 **[MetaStrip — see what your photos reveal, then erase it](https://thefinalmilkman.github.io/metastrip/)**
Source: <https://github.com/thefinalmilkman/metastrip>

It's free and open source (MIT). If it kept your address out of a photo and you want to throw something back, there's a USDC-on-Base tip address on the page — but the tool is yours regardless.

## Takeaways for builders

- Treat EXIF as untrusted user data you are *removing*, not displaying — MakerNotes in particular are a junk drawer of vendor-specific identifiers.
- If you handle user image uploads, strip metadata **server-side on ingest**. Don't trust the client, and don't assume your image library does it for you — many preserve EXIF by default.
- When you strip, prefer segment removal over re-encoding so you don't degrade the image.

Your photos have been narrating your life in the background. Now you know where the script is written, and how to delete it.
