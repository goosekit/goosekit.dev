# PDF Editor — Distribution Package

Ready-to-post snippets for sharing the Goosekit PDF Editor (`/pdf-editor/`).
All copy is honest about what the tool does and does NOT do, so it survives
scrutiny in technical communities.

## What the tool actually is (read first)

- Browser-based PDF editor at `https://goosekit.dev/pdf-editor/`
- Built on `pdf.js` (rendering) + `pdf-lib` (export)
- Runs entirely client-side. The PDF never leaves the user's device.
- Lets you: add text, draw freehand, highlight, place rectangles, stamp images,
  sign (draw or upload PNG/JPG), reorder pages, rotate pages, delete pages.
- On export, annotations are flattened into the page content.
- It does NOT rewrite existing embedded text in a PDF (it is not Acrobat).
- It does NOT do OCR on scanned PDFs.
- It does NOT support password-protected PDFs.
- It does NOT edit AcroForm fields as fields.

Keep these constraints visible in any post — that is the point of being honest.

## Hacker News (Show HN)

### Title (≤80 chars)
```
Show HN: A free browser-based PDF editor that flattens edits on export
```

### Body
```
I kept reaching for an online PDF editor for small things — signing a contract,
deleting a cover page, rotating a sideways scan — and almost every option
either uploaded the file, asked me to sign up, or stuck a watermark on the
output.

So I built one that runs entirely in the browser:

  https://goosekit.dev/pdf-editor/

What it does:
- Add text, draw freehand, highlight, draw rectangles
- Stamp images and signatures (draw with the mouse or upload a PNG/JPG)
- Reorder, rotate, and delete pages from a left-side page strip
- Flatten everything on export so the result opens cleanly in any reader

What it does NOT do (on purpose, because I'd rather be honest than oversell):
- Rewrite the existing embedded text in a PDF — that's still Acrobat territory
- OCR scanned PDFs
- Open password-protected PDFs
- Edit AcroForm fields as fields

Stack is `pdf.js` for rendering and `pdf-lib` for the export. No backend,
no upload, no signup, no per-file limit. Source for the page is plain HTML/JS.

Curious whether the page-strip + flatten-on-export model is the right tradeoff
for casual editing, or if people would rather have it preserve annotations as
real PDF annotation objects. Feedback welcome.
```

### Notes
- Do not crosspost while the HN post is hot.
- If asked about the business: it is part of Goosekit, a set of free
  browser-based tools. There is a paid product (Ship It Kit) elsewhere on the
  site but not on this page.
- If asked about telemetry: PostHog is loaded site-wide for traffic stats.
  The PDF itself is not sent anywhere.

## Reddit

### r/InternetIsBeautiful

Title:
```
Free browser-based PDF editor — add text, sign, reorder pages, no signup, no upload
```

Body:
```
Found myself reaching for a quick online PDF editor too often, so I made one
that doesn't upload your file or ask you to sign up.

  https://goosekit.dev/pdf-editor/

You can:
- add text, draw, highlight, draw rectangles
- stamp images and signatures (draw with the mouse or upload PNG/JPG)
- reorder, rotate, and delete pages
- download a flattened PDF

It's a practical browser editor — not desktop Acrobat. It does not rewrite
the existing embedded text in a PDF and it does not OCR scans.

It runs in the tab using pdf.js + pdf-lib. Close the tab and the file is gone.
```

### r/webdev or r/SideProject

Title:
```
I built a client-side PDF editor with pdf.js + pdf-lib (no upload, no signup)
```

Body:
```
Wanted to share a small thing I built and explain the tradeoffs, in case
anyone is doing something similar.

Goal: a free PDF editor that is genuinely client-side and does not pretend
to be Acrobat.

Live: https://goosekit.dev/pdf-editor/

Stack:
- pdf.js renders pages onto a canvas
- a DOM/SVG overlay handles annotations (text, draw, highlight, rect, image)
- pdf-lib copies original pages into a new doc, applies user rotation, and
  draws each annotation in the correct PDF coordinate system, then flattens

Things I learned along the way:
- Mapping screen coordinates to PDF coordinates with rotation is the
  fiddliest part (PDF origin is bottom-left; the DOM origin is top-left).
- "Edit the existing text" expectations are strong. I decided to be very
  upfront that this is overlay + flatten, not text re-flow.
- Browser memory pressure is the real ceiling. Hundreds of image-heavy
  pages can become slow.

Honest about what it does NOT do:
- No rewriting of existing embedded text
- No OCR
- No password-protected PDFs
- No interactive form-field editing

Happy to answer implementation questions.
```

## LinkedIn

```
Most online PDF editors either upload your file, ask for a signup, or paste a
watermark on the output.

So I shipped a small free alternative: a browser-based PDF editor that runs
entirely in the tab.

→ https://goosekit.dev/pdf-editor/

You can:
• Add text, draw, highlight, and shape
• Sign with the mouse, trackpad, or an uploaded image
• Reorder, rotate, and delete pages
• Download a flattened PDF

To stay honest: this is a practical editor for annotations, signatures, and
page changes. It does not rewrite the underlying text in an existing PDF —
that is still desktop-Acrobat territory.

If "I just need to sign this and send it back" describes a meaningful chunk
of your week, this might save you a few minutes each time.
```

## X / Twitter

### Single-tweet version
```
Free PDF editor that runs in the browser:
- add text, draw, highlight
- sign by drawing or uploading
- reorder, rotate, delete pages
- flatten on export

No upload. No signup. No watermark.

It's not Acrobat — it doesn't rewrite existing text — but for sign + edit + page changes, it's quick.

https://goosekit.dev/pdf-editor/
```

### Thread version (3 tweets)

Tweet 1:
```
Built a free, client-side PDF editor.

You can add text, draw, highlight, sign,
and reorder/rotate/delete pages — then download a flattened PDF.

No upload, no signup, no watermark.

https://goosekit.dev/pdf-editor/
```

Tweet 2:
```
Stack:
- pdf.js for rendering pages
- pdf-lib for the export
- DOM + SVG overlay for annotations

Everything runs in the tab. Close the tab and your PDF is gone.
```

Tweet 3:
```
Honest about what it doesn't do:
- doesn't rewrite the existing embedded text in a PDF (that's Acrobat's job)
- doesn't OCR scans
- doesn't open password-protected PDFs
- doesn't edit AcroForm fields as fields

For "sign this, fix page order, ship it" — it's quick.
```

## Plain product description (for directories like SaaSHub, AlternativeTo)

### One-liner
```
Free browser-based PDF editor — add text, sign, reorder pages, no upload, no signup.
```

### Short description
```
Goosekit PDF Editor is a free, browser-based PDF editor. It lets you add
text, draw, highlight, place images, and sign — and reorder, rotate or
delete pages. The PDF never leaves your device. Annotations are flattened
into the exported file. It's not a full desktop replacement: it does not
rewrite existing embedded text and does not OCR scanned PDFs.
```

### Long description
```
Goosekit PDF Editor is a free PDF editor that runs entirely in your browser.

What you can do:
- Add text boxes anywhere on a page, with custom font size and color
- Draw freehand with a pen tool, with adjustable stroke width
- Highlight regions with translucent rectangles
- Place solid rectangles for redaction-style cover blocks
- Stamp PNG or JPG images onto a page
- Sign by drawing with the mouse or trackpad, or by uploading a signature image
- Reorder pages with up/down controls
- Rotate pages 90° at a time
- Delete pages you do not want in the final document

How it works:
The page is rendered with pdf.js. Annotations live as DOM and SVG overlays
on top of the rendered canvas. On export, pdf-lib copies the original pages
into a new document, applies your rotation and reordering, and flattens each
annotation into the page content. The output is a clean, standard PDF.

Privacy:
The PDF is processed entirely in the browser. Nothing is uploaded.
You can verify with DevTools → Network: no request goes out when you load
or edit a file.

Limitations (so you know what to expect):
- Does not rewrite existing embedded text in a PDF
- No OCR for scanned PDFs
- No password-protected PDFs
- No interactive form-field editing
- Very large PDFs can be slow because everything runs locally
```

## Where to send people from this page

- /pdf-merge/ — combine several PDFs first, then edit
- /image-to-pdf/ — turn photos into a PDF, then edit
- /all-tools/ — the full Goosekit catalog
