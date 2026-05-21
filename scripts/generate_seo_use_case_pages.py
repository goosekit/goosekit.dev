#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import html

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()

PAGES = [
    {
        "slug": "json-formatter-api-responses",
        "title": "JSON Formatter for API Responses",
        "description": "Format, validate, and inspect API JSON responses in your browser. Use Goosekit's free JSON formatter for debugging payloads, nested objects, and API errors.",
        "h1": "JSON formatter for API responses",
        "eyebrow": "API debugging",
        "problem": "Raw API responses are hard to scan when you are debugging nested payloads, failed requests, webhooks, or copied logs from a backend console.",
        "primary_tool": {"name": "Open the JSON Formatter", "url": "/json/"},
        "tools": [("JSON Formatter", "/json/"), ("JSON to TypeScript", "/json-to-typescript/"), ("JSON to CSV", "/json-csv/"), ("JSON to YAML", "/json-yaml/"), ("JWT Decoder", "/jwt/")],
        "steps": ["Paste the raw JSON response from your API client, logs, webhook dashboard, or browser console.", "Format it into an indented tree so nested objects and arrays are easier to inspect.", "Check for invalid JSON before blaming your API client or frontend parsing code.", "Use adjacent converters when you need TypeScript types, CSV export, or YAML config."],
        "cases": ["Inspecting webhook payloads before writing handlers", "Debugging a failed REST API response", "Checking nested auth/user objects returned by Supabase, Stripe, or Auth.js"],
        "faq": [("Is the JSON sent to a server?", "No. Goosekit's browser tools are designed for quick client-side utility work."), ("Can I use this for private API payloads?", "For highly sensitive production data, prefer sanitized samples. For everyday debugging, the browser-based workflow avoids account creation and upload friction."), ("What should I do after formatting JSON?", "If the payload becomes part of app code, convert it to TypeScript types or document the fields in your API contract.")],
        "related": ["api-error-response-debugging", "jwt-decoder-authjs", "base64-decoder-api-debugging"],
    },
    {
        "slug": "jwt-decoder-authjs",
        "title": "JWT Decoder for Auth.js, Supabase, and API Tokens",
        "description": "Decode JWT headers and payloads while debugging Auth.js, Supabase, and API token claims. Free browser-based JWT decoder, no signup.",
        "h1": "JWT decoder for Auth.js and API token debugging",
        "eyebrow": "Auth debugging",
        "problem": "Auth bugs often hide inside token claims: wrong audience, expired token, missing role, unexpected issuer, or a stale session value.",
        "primary_tool": {"name": "Open the JWT Decoder", "url": "/jwt/"},
        "tools": [("JWT Decoder", "/jwt/"), ("JSON Formatter", "/json/"), ("Base64 Decoder", "/base64/"), ("Timestamp Converter", "/timestamp/"), ("Hash Generator", "/hash/")],
        "steps": ["Paste a JWT from a cookie, Authorization header, or test request.", "Read the header and payload without changing the token.", "Check common claims like exp, iat, aud, iss, sub, role, and provider-specific metadata.", "Use the timestamp converter for Unix expiry values and JSON formatter for copied claims."],
        "cases": ["Debugging Auth.js session tokens", "Checking Supabase JWT role claims", "Inspecting API tokens before testing a protected endpoint"],
        "faq": [("Does decoding verify the signature?", "No. Decoding helps inspect token contents; signature verification requires the appropriate secret or public key."), ("Is it safe to paste real JWTs?", "Prefer short-lived development tokens or sanitized examples. Never share production tokens in public threads or bug reports."), ("Why does my token look valid but fail?", "Check expiry, audience, issuer, and whether the backend expects a different signing key or algorithm.")],
        "related": ["json-formatter-api-responses", "timestamp-converter-unix", "base64-decoder-api-debugging"],
    },
    {
        "slug": "regex-tester-javascript",
        "title": "JavaScript Regex Tester for Frontend Validation",
        "description": "Test JavaScript regular expressions for forms, URLs, slugs, and validation rules. Free browser regex tester with quick examples and related dev tools.",
        "h1": "JavaScript regex tester for frontend validation",
        "eyebrow": "Frontend debugging",
        "problem": "Regex bugs are easy to miss when validation rules behave differently across form input, pasted data, URL slugs, or backend checks.",
        "primary_tool": {"name": "Open the Regex Tester", "url": "/regex/"},
        "tools": [("Regex Tester", "/regex/"), ("Text Case Converter", "/text-case/"), ("URL Encoder", "/url-encode/"), ("JSON Formatter", "/json/"), ("Diff Checker", "/diff/")],
        "steps": ["Paste the regex pattern and a set of realistic test strings.", "Include positive and negative examples before using the pattern in production.", "Check edge cases such as empty input, accents, whitespace, unicode, and URL-safe characters.", "Copy the final pattern into your frontend validation code and keep examples near the test."],
        "cases": ["Testing email or username validation", "Checking slug and URL patterns", "Debugging search/replace rules before touching content"],
        "faq": [("Should I use one huge regex for validation?", "Usually no. Keep validation readable and pair regex checks with clearer application logic when possible."), ("Can this replace unit tests?", "No. Use the tester to design the pattern, then add unit tests for the exact cases your app depends on."), ("Why do regexes behave differently in another language?", "Regex engines differ. This page is aimed at JavaScript-style frontend work." )],
        "related": ["url-encoder-api-requests", "json-formatter-api-responses", "base64-decoder-api-debugging"],
    },
    {
        "slug": "base64-decoder-api-debugging",
        "title": "Base64 Decoder for API Debugging",
        "description": "Decode Base64 strings while debugging API payloads, headers, images, and encoded config. Free browser-based Base64 encoder and decoder.",
        "h1": "Base64 decoder for API debugging",
        "eyebrow": "Payload debugging",
        "problem": "Base64 shows up in auth headers, API payloads, image data, webhook bodies, and config values, but raw strings are impossible to read directly.",
        "primary_tool": {"name": "Open the Base64 Tool", "url": "/base64/"},
        "tools": [("Base64 Encoder/Decoder", "/base64/"), ("JSON Formatter", "/json/"), ("JWT Decoder", "/jwt/"), ("URL Encoder", "/url-encode/"), ("Hash Generator", "/hash/")],
        "steps": ["Paste the encoded value from the payload, header, or config.", "Decode it and inspect whether the result is text, JSON, binary-looking data, or another encoded value.", "If the decoded result is JSON, send it to the formatter for easier inspection.", "Do not paste secrets into support tickets; decode locally and share only sanitized findings."],
        "cases": ["Reading encoded Basic Auth segments", "Inspecting Base64 JSON payloads", "Checking whether an API returned image data or plain text"],
        "faq": [("Is Base64 encryption?", "No. Base64 is encoding, not security. Anyone can decode it."), ("Why does decoded text look broken?", "The original value may be binary data, compressed content, or encoded with another charset."), ("Can Base64 hide secrets?", "No. Treat Base64 secrets as exposed if they leave your trusted environment." )],
        "related": ["jwt-decoder-authjs", "json-formatter-api-responses", "hash-generator-checksums"],
    },
    {
        "slug": "hash-generator-checksums",
        "title": "Hash Generator for Checksums and Debugging",
        "description": "Generate MD5, SHA-256, and SHA-512 hashes for checksums, payload comparison, and debugging. Free browser-based hash generator.",
        "h1": "Hash generator for checksums and debugging",
        "eyebrow": "Integrity checks",
        "problem": "Hashes are useful when you need to compare payloads, verify copied content, document checksums, or debug why two values that look similar are not actually identical.",
        "primary_tool": {"name": "Open the Hash Generator", "url": "/hash/"},
        "tools": [("Hash Generator", "/hash/"), ("Diff Checker", "/diff/"), ("Base64 Encoder/Decoder", "/base64/"), ("JSON Formatter", "/json/"), ("Password Generator", "/password/")],
        "steps": ["Paste the text or value you want to fingerprint.", "Generate the hash algorithm required by your workflow, commonly SHA-256 for modern checksums.", "Compare hashes when raw payloads are too large or sensitive to share directly.", "Use diff tools when hashes differ and you need to find the exact content change."],
        "cases": ["Verifying copied config values", "Comparing webhook payload samples", "Documenting downloadable file checksums"],
        "faq": [("Should I use MD5 for security?", "No. MD5 is useful for legacy checksums, not secure password or cryptographic workflows."), ("Which hash should I use?", "For modern integrity checks, SHA-256 is usually the safest default."), ("Can I reverse a hash?", "Cryptographic hashes are designed to be one-way, but weak inputs can still be guessed.")],
        "related": ["base64-decoder-api-debugging", "json-formatter-api-responses", "uuid-generator-test-data"],
    },
    {
        "slug": "url-encoder-api-requests",
        "title": "URL Encoder for API Requests and Query Strings",
        "description": "Encode and decode URLs, query strings, redirect URLs, and API parameters. Free browser-based URL encoder and decoder for developers.",
        "h1": "URL encoder for API requests and query strings",
        "eyebrow": "Request debugging",
        "problem": "Broken query strings, redirect URLs, callback parameters, and copied API URLs often come down to one missing or double-encoded character.",
        "primary_tool": {"name": "Open the URL Encoder", "url": "/url-encode/"},
        "tools": [("URL Encoder/Decoder", "/url-encode/"), ("JSON Formatter", "/json/"), ("cURL Converter", "/curl-converter/"), ("Base64 Tool", "/base64/"), ("Diff Checker", "/diff/")],
        "steps": ["Paste the URL, callback, or query parameter you need to inspect.", "Decode it to see the real target, nested redirect, or search parameters.", "Encode only the parameter value when building API URLs; avoid encoding the entire URL unless that is required.", "Use the diff checker if two URLs look identical but behave differently."],
        "cases": ["Debugging OAuth callback URLs", "Building API query strings", "Checking redirect URLs in email or checkout flows"],
        "faq": [("What is double encoding?", "It happens when an already encoded value is encoded again, often turning % into %25."), ("Should spaces be + or %20?", "It depends on context. Query form encoding often uses +, while general URL encoding uses %20."), ("Can I decode tracking links?", "Yes, but be careful not to open unknown targets you do not trust.")],
        "related": ["curl-converter-api-clients", "regex-tester-javascript", "json-formatter-api-responses"],
    },
    {
        "slug": "timestamp-converter-unix",
        "title": "Unix Timestamp Converter for Logs and Tokens",
        "description": "Convert Unix timestamps while debugging logs, JWT expiry, API responses, and scheduled jobs. Free browser timestamp converter.",
        "h1": "Unix timestamp converter for logs and tokens",
        "eyebrow": "Time debugging",
        "problem": "Unix timestamps show up in JWT claims, logs, API payloads, cron jobs, and database records, but raw numbers make time-zone mistakes easy.",
        "primary_tool": {"name": "Open the Timestamp Converter", "url": "/timestamp/"},
        "tools": [("Timestamp Converter", "/timestamp/"), ("JWT Decoder", "/jwt/"), ("Cron Expression Generator", "/cron/"), ("JSON Formatter", "/json/"), ("Diff Checker", "/diff/")],
        "steps": ["Copy the timestamp from your log, token, or payload.", "Convert it to a readable date and check the time zone assumptions.", "For JWTs, compare exp and iat values against the current time.", "For scheduling bugs, verify whether the system expects UTC or local time."],
        "cases": ["Checking JWT expiration", "Reading server logs", "Debugging scheduled jobs and webhook timestamps"],
        "faq": [("Seconds or milliseconds?", "Many APIs use seconds, while JavaScript Date values often use milliseconds. If the date looks wildly wrong, check the unit."), ("Why is the time off by one or two hours?", "Usually time zone or daylight-saving assumptions. Store UTC and display local time deliberately."), ("Can timestamps prove event order?", "They help, but distributed systems can have clock drift. Pair timestamps with IDs or logs when possible.")],
        "related": ["api-error-response-debugging", "jwt-decoder-authjs", "json-formatter-api-responses"],
    },
    {
        "slug": "curl-converter-api-clients",
        "title": "cURL Converter for API Clients and Debugging",
        "description": "Convert cURL requests into code while testing APIs, debugging headers, and sharing reproducible examples. Free browser cURL converter for developers.",
        "h1": "cURL converter for API clients and debugging",
        "eyebrow": "API clients",
        "problem": "cURL is great for reproducing bugs, but app code usually needs fetch, JavaScript, Python, or another client format with headers and body preserved.",
        "primary_tool": {"name": "Open the cURL Converter", "url": "/curl-converter/"},
        "tools": [("cURL Converter", "/curl-converter/"), ("JSON Formatter", "/json/"), ("URL Encoder", "/url-encode/"), ("JWT Decoder", "/jwt/"), ("HTTP Status Reference", "/http-status/")],
        "steps": ["Copy the cURL command from docs, DevTools, or an API client.", "Convert it into the code format you need for your app or debugging snippet.", "Check headers, auth tokens, content-type, and JSON body before pasting into production code.", "Remove secrets before sharing the converted example publicly."],
        "cases": ["Turning API docs into fetch examples", "Reproducing a failing request from DevTools", "Sharing bug reports without losing headers or body structure"],
        "faq": [("Should I paste production tokens?", "No. Replace secrets with placeholders before converting or sharing examples."), ("Why does converted code still fail?", "Check CORS, auth scopes, content-type, and environment-specific headers."), ("Is cURL enough for API testing?", "It is great for reproduction, but pair it with real tests for important flows.")],
        "related": ["api-error-response-debugging", "json-formatter-api-responses", "url-encoder-api-requests"],
    },
    {
        "slug": "webhook-payload-debugging",
        "title": "Webhook Payload Debugging Tools",
        "description": "Debug webhook payloads with browser tools for JSON formatting, timestamps, signatures, Base64 values, and reproducible API requests.",
        "h1": "Webhook payload debugging tools",
        "eyebrow": "Webhook debugging",
        "problem": "Webhook failures usually hide in one small detail: malformed JSON, a timestamp mismatch, a copied signature header, an encoded field, or a request body that changed between retries.",
        "primary_tool": {"name": "Open the JSON Formatter", "url": "/json/"},
        "tools": [("JSON Formatter", "/json/"), ("Timestamp Converter", "/timestamp/"), ("Hash Generator", "/hash/"), ("Base64 Encoder/Decoder", "/base64/"), ("cURL Converter", "/curl-converter/")],
        "steps": ["Copy the webhook body from your provider dashboard, local tunnel, server logs, or failed delivery view.", "Format the JSON first so nested event fields, customer IDs, object types, and error messages are easy to scan.", "Check event timestamps in UTC before assuming the delivery is stale or duplicated.", "Compare the raw body and signature-related values carefully; signature checks often fail when whitespace, encoding, or body parsing changes the original payload.", "Turn a sanitized retry request into a reproducible cURL or code snippet when you need to share the issue with a teammate."],
        "cases": ["Inspecting Stripe, Clerk, Supabase, or GitHub webhook bodies", "Debugging signature verification failures", "Checking whether a webhook retry sent a different payload", "Preparing a sanitized bug report without exposing customer data"],
        "faq": [("Should I format JSON before verifying a webhook signature?", "No. Verify signatures against the raw request body exactly as received. Use formatting only for human inspection after you preserve the original body."), ("What should I sanitize before sharing a webhook payload?", "Remove customer identifiers, emails, tokens, addresses, internal IDs, and any secret headers. Keep only the fields needed to reproduce the bug."), ("Why does a webhook work locally but fail in production?", "Common causes are different raw-body handling, wrong endpoint secret, clock skew, replay windows, missing headers, or middleware that parses the body before verification.")],
        "related": ["json-formatter-api-responses", "timestamp-converter-unix", "curl-converter-api-clients"],
    },

    {
        "slug": "api-error-response-debugging",
        "title": "API Error Response Debugging Workflow",
        "description": "Debug API error responses with JSON formatting, HTTP status lookup, cURL conversion, timestamps, and payload comparison. A practical browser workflow for failed requests.",
        "h1": "API error response debugging workflow",
        "eyebrow": "API debugging",
        "problem": "A failed API request rarely fails for just one reason. The status code, JSON body, auth header, timestamp, and reproduced request all need to line up before the bug becomes obvious.",
        "primary_tool": {"name": "Start with the JSON Formatter", "url": "/json/"},
        "tools": [("JSON Formatter", "/json/"), ("HTTP Status Reference", "/http-status/"), ("cURL Converter", "/curl-converter/"), ("Timestamp Converter", "/timestamp/"), ("Diff Checker", "/diff/")],
        "steps": ["Copy the raw response body, status code, and request details from DevTools, server logs, an API client, or a failed test.", "Format the JSON error body first so fields like code, message, details, validation errors, request_id, and retry_after are easy to scan.", "Look up the HTTP status code and check whether the failure is authentication, validation, rate limiting, conflict, or server-side behavior.", "Convert a sanitized cURL reproduction into the client code or snippet you need, keeping headers and body structure intact.", "Compare a working and failing payload with diff when the response looks similar but only one request fails."],
        "cases": ["Debugging 400 and 422 validation errors from REST APIs", "Checking 401 or 403 auth failures before changing backend code", "Investigating 409 conflicts, 429 rate limits, and retry behavior", "Preparing a sanitized API bug report with enough context to reproduce the issue"],
        "faq": [("What should I capture before debugging an API error?", "Capture the status code, response body, request method, URL, relevant headers, request body, timestamp, and a request ID if the API returns one."), ("Should I share the full failed request with support?", "No. Replace tokens, cookies, customer IDs, emails, addresses, and internal identifiers with placeholders before sharing."), ("Why does the same API call work in one client but fail in another?", "Common causes are missing headers, different content-type, stale auth tokens, encoded query parameters, CORS context, or environment-specific base URLs.")],
        "related": ["json-formatter-api-responses", "curl-converter-api-clients", "timestamp-converter-unix"],
    },
    {
        "slug": "sql-formatter-query-debugging",
        "title": "SQL Formatter for Query Debugging",
        "description": "Format SQL queries for debugging, reviews, logs, and database work. Free browser SQL formatter for developers working with messy queries.",
        "h1": "SQL formatter for query debugging",
        "eyebrow": "Database debugging",
        "problem": "Copied SQL from logs, ORMs, dashboards, and error reports is often compressed into one unreadable line, making joins and filters hard to review.",
        "primary_tool": {"name": "Open the SQL Formatter", "url": "/sql-formatter/"},
        "tools": [("SQL Formatter", "/sql-formatter/"), ("JSON Formatter", "/json/"), ("Diff Checker", "/diff/"), ("Timestamp Converter", "/timestamp/"), ("Text Case Converter", "/text-case/")],
        "steps": ["Paste a query from logs, an ORM output, or a database console.", "Format it so SELECT fields, joins, conditions, and ordering are readable.", "Check whether filters match the intended customer, tenant, workspace, or date range.", "Use diff when comparing two versions of a query."],
        "cases": ["Reviewing ORM-generated SQL", "Debugging tenant filters", "Comparing query changes before a migration"],
        "faq": [("Does formatting change the query?", "Formatting should only change whitespace and layout, but always review important queries before running them."), ("Can this optimize SQL?", "No. It makes SQL easier to read; optimization still requires understanding indexes and query plans."), ("Should I paste production data?", "Avoid sensitive data. Replace customer values with safe placeholders when possible.")],
        "related": ["json-formatter-api-responses", "timestamp-converter-unix", "hash-generator-checksums"],
    },
    {
        "slug": "uuid-generator-test-data",
        "title": "UUID Generator for Test Data and API Debugging",
        "description": "Generate UUIDs for test data, mock payloads, database rows, and API debugging. Free browser-based UUID generator, no signup.",
        "h1": "UUID generator for test data and API debugging",
        "eyebrow": "Test data",
        "problem": "Mock payloads, test users, database rows, and API examples often need realistic IDs that are unique enough for local development and documentation.",
        "primary_tool": {"name": "Open the UUID Generator", "url": "/uuid/"},
        "tools": [("UUID Generator", "/uuid/"), ("JSON Formatter", "/json/"), ("Password Generator", "/password/"), ("Hash Generator", "/hash/"), ("Timestamp Converter", "/timestamp/")],
        "steps": ["Generate one or several UUIDs for your test payloads.", "Use them in mock JSON, database seed data, or API examples.", "Keep real production IDs out of public docs and bug reports.", "Pair UUIDs with timestamps and sample JSON when building realistic test fixtures."],
        "cases": ["Creating mock API payloads", "Seeding local databases", "Replacing real IDs in bug reports"],
        "faq": [("Are generated UUIDs guaranteed unique?", "UUIDs are designed to make collisions extremely unlikely for normal development use."), ("Can I use these in production?", "Use your application or database UUID generation for production records. This tool is best for quick manual work and examples."), ("Why use UUIDs instead of incremental IDs?", "UUIDs are useful for distributed systems, public IDs, and sanitized examples where sequential IDs leak too much context.")],
        "related": ["json-formatter-api-responses", "timestamp-converter-unix", "hash-generator-checksums"],
    },
]

SLUG_TO_PAGE = {p["slug"]: p for p in PAGES}

CSS = """
*,*::before,*::after{box-sizing:border-box}body{margin:0;background:#0f0f19;color:#e8e8f2;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.7}a{color:#ff6a2a;text-decoration:none}a:hover{text-decoration:underline}.wrap{width:min(1080px,calc(100% - 40px));margin:0 auto}.hero{padding:72px 0 42px;background:radial-gradient(circle at 20% 0%,rgba(255,72,0,.18),transparent 34%),#0f0f19}.eyebrow{display:inline-flex;border:1px solid rgba(255,72,0,.28);background:rgba(255,72,0,.1);color:#ffb08a;border-radius:999px;padding:7px 11px;font-size:.83rem;font-weight:750;margin-bottom:16px}h1{font-size:clamp(2.25rem,5vw,4.35rem);line-height:1.02;letter-spacing:-.055em;margin:0 0 18px;color:#fff}.lead{font-size:clamp(1.04rem,2vw,1.24rem);color:#c9c9d8;max-width:760px;margin:0 0 24px}.cta-row{display:flex;gap:12px;flex-wrap:wrap}.btn{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:12px 17px;border-radius:12px;font-weight:780;border:1px solid rgba(255,255,255,.11);background:rgba(255,255,255,.045);color:#fff}.btn-primary{background:#ff4800;border-color:#ff4800;box-shadow:0 16px 34px rgba(255,72,0,.22)}main{padding:36px 0 70px}.grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:28px;align-items:start}.card{border:1px solid rgba(255,255,255,.09);background:#181825;border-radius:18px;padding:24px;margin-bottom:18px}.card h2{font-size:1.45rem;margin:0 0 12px;color:#fff}.card h3{font-size:1.05rem;margin:18px 0 8px;color:#fff}.card p,.card li{color:#bebed0}.tool-list{display:grid;gap:9px}.tool-list a,.related a{display:block;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.035);border-radius:12px;padding:10px 12px;color:#f4f4fb}.steps{counter-reset:step;list-style:none;padding:0;margin:0}.steps li{counter-increment:step;position:relative;padding-left:42px;margin:0 0 14px}.steps li::before{content:counter(step);position:absolute;left:0;top:0;width:28px;height:28px;display:grid;place-items:center;border-radius:999px;background:#ff4800;color:#fff;font-weight:800}.faq details{border-top:1px solid rgba(255,255,255,.08);padding:13px 0}.faq summary{cursor:pointer;color:#fff;font-weight:760}.muted{color:#9393a8;font-size:.94rem}.site-header{position:sticky;top:0;z-index:30;background:rgba(10,10,26,.78);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.06)}.site-header-inner{width:100%;min-height:56px;padding:8px 16px 8px 10px;display:flex;align-items:center;justify-content:space-between;gap:14px}.site-brand img{width:100px;height:auto;display:block}.site-nav{display:flex;align-items:center;justify-content:flex-end;flex-wrap:wrap;flex:1;gap:8px 14px}.site-nav a{color:#94a3b8;text-decoration:none;font-size:.9rem;font-weight:600;line-height:1}.site-nav a:hover{color:#e2e8f0}.site-nav .nav-cta{color:#fff;background:rgba(255,72,0,.95);border:1px solid rgba(255,72,0,.9);padding:8px 12px;border-radius:11px;box-shadow:0 8px 22px rgba(255,72,0,.16)}footer{border-top:1px solid rgba(255,255,255,.08);padding:26px 0;color:#7f7f97;text-align:center;background:#121222}@media(max-width:820px){.grid{grid-template-columns:1fr}.hero{padding-top:46px}.wrap{width:min(100% - 28px,1080px)}}
""".strip()

NAV = """<header class="site-header"><div class="site-header-inner"><a class="site-brand" href="/"><img src="/logo-dark.png" alt="Goosekit"></a><nav class="site-nav"><a href="/tools/">Tools</a><a href="/use-cases/">Use cases</a><a href="/compare/">Compare</a><a href="/blog/">Blog</a><a href="/ship-it-kit/" class="nav-cta">Ship It Kit</a></nav></div></header>"""

def esc(s): return html.escape(s, quote=True)

def page_html(page):
    related = [SLUG_TO_PAGE[s] for s in page.get("related", []) if s in SLUG_TO_PAGE]
    tool_items = "\n".join(f'<a href="{esc(url)}">{esc(name)} →</a>' for name, url in page["tools"])
    steps = "\n".join(f'<li>{esc(step)}</li>' for step in page["steps"])
    cases = "\n".join(f'<li>{esc(case)}</li>' for case in page["cases"])
    faq = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in page["faq"])
    related_links = "\n".join(f'<a href="/use-cases/{esc(r["slug"])}/">{esc(r["h1"])} →</a>' for r in related)
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page["h1"],
        "description": page["description"],
        "mainEntityOfPage": f"https://goosekit.dev/use-cases/{page['slug']}/",
        "publisher": {"@type": "Organization", "name": "Goosekit", "url": "https://goosekit.dev"},
        "dateModified": TODAY,
    }
    import json
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(page['title'])} | Goosekit</title>
  <meta name="description" content="{esc(page['description'])}">
  <link rel="canonical" href="https://goosekit.dev/use-cases/{esc(page['slug'])}/">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{esc(page['title'])}">
  <meta property="og:description" content="{esc(page['description'])}">
  <meta property="og:url" content="https://goosekit.dev/use-cases/{esc(page['slug'])}/">
  <meta property="og:site_name" content="Goosekit">
  <script defer src="/posthog.js"></script>
  <script defer src="/site-header-homefix.js?v=20260503-mobilemenu1"></script>
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  <style>{CSS}</style>
</head>
<body data-seo-use-case="{esc(page['slug'])}">
{NAV}
<section class="hero"><div class="wrap">
  <span class="eyebrow">{esc(page['eyebrow'])}</span>
  <h1>{esc(page['h1'])}</h1>
  <p class="lead">{esc(page['problem'])}</p>
  <div class="cta-row"><a class="btn btn-primary" href="{esc(page['primary_tool']['url'])}" data-use-case-tool-click="{esc(page['slug'])}">{esc(page['primary_tool']['name'])}</a><a class="btn" href="/use-cases/">Browse use cases</a></div>
</div></section>
<main><div class="wrap grid">
  <article>
    <section class="card"><h2>How to use this workflow</h2><ol class="steps">{steps}</ol></section>
    <section class="card"><h2>When this helps</h2><ul>{cases}</ul></section>
    <section class="card faq"><h2>Quick answers</h2>{faq}</section>
  </article>
  <aside>
    <section class="card"><h2>Tools in this workflow</h2><div class="tool-list">{tool_items}</div></section>
    <section class="card related"><h2>Related use cases</h2>{related_links}</section>
    <section class="card"><h2>Why Goosekit?</h2><p class="muted">Fast browser tools for everyday debugging: no account wall, no heavy dashboard, and clear links between related tasks.</p></section>
  </aside>
</div></main>
<footer><div class="wrap">Goosekit — free browser tools for developers, creators, and small teams.</div></footer>
<script>
(function() {{
  var slug = document.body.getAttribute('data-seo-use-case');
  function capture(name, props) {{
    if (window.posthog && typeof window.posthog.capture === 'function') window.posthog.capture(name, props || {{}});
  }}
  capture('seo_use_case_page_viewed', {{ slug: slug, page_type: 'seo_use_case' }});
  document.addEventListener('click', function(e) {{
    var link = e.target.closest('[data-use-case-tool-click]');
    if (!link) return;
    capture('seo_use_case_tool_clicked', {{ slug: slug, target_url: link.getAttribute('href'), link_text: link.textContent.trim() }});
  }});
}})();
</script>
</body>
</html>
'''

def hub_html():
    cards = "\n".join(f'''<a class="card" href="/use-cases/{esc(p['slug'])}/"><span class="eyebrow">{esc(p['eyebrow'])}</span><h2>{esc(p['h1'])}</h2><p>{esc(p['description'])}</p></a>''' for p in PAGES)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Developer Tool Use Cases | Goosekit</title><meta name="description" content="Practical Goosekit workflows for API debugging, auth tokens, JSON formatting, regex testing, Base64 decoding, checksums, and more."><link rel="canonical" href="https://goosekit.dev/use-cases/"><script defer src="/posthog.js"></script><script defer src="/site-header-homefix.js?v=20260503-mobilemenu1"></script><style>{CSS}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}.cards .card{{display:block;margin:0;color:inherit}}</style></head><body>{NAV}<section class="hero"><div class="wrap"><span class="eyebrow">Developer workflows</span><h1>Use Goosekit for real debugging jobs</h1><p class="lead">Focused workflows for the small tasks developers search for every day: formatting API JSON, decoding JWTs, testing regexes, checking timestamps, and cleaning up payloads.</p></div></section><main><div class="wrap"><div class="cards">{cards}</div></div></main><footer><div class="wrap">Goosekit — free browser tools for developers, creators, and small teams.</div></footer></body></html>'''

for page in PAGES:
    out = ROOT / "use-cases" / page["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_html(page), encoding="utf-8")

(ROOT / "use-cases" / "index.html").write_text(hub_html(), encoding="utf-8")

# Update sitemap with the hub and generated pages if missing.
sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
insert = []
urls = ["https://goosekit.dev/use-cases/"] + [f"https://goosekit.dev/use-cases/{p['slug']}/" for p in PAGES]
for url in urls:
    if url not in text:
        insert.append(f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>")
if insert:
    text = text.replace("</urlset>", "\n" + "\n".join(insert) + "\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")

print(f"Generated {len(PAGES)} use-case pages plus hub")
