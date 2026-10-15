# KOREA — Cloudflare Pages Deployment

Repository: https://github.com/thiepn/korea
Planned later custom domain: korea.thiepn.dev (**NOT configured during initial release**).

## Cloudflare Pages Git integration (free tier)

- Cloudflare account: Junsosmart@gmail.com's Account
- Pages project name: `korea`
- Git provider: GitHub repository `thiepn/korea`
- Production branch: `main`
- Framework preset: None (static HTML)
- Root directory: `/`
- Build command: `python3 scripts/build_release.py`
- Build output directory: `dist`

Only the explicitly allowlisted public runtime files are copied to `dist`.
`canonical/`, `scripts/`, `tests/`, `PHASE1_QA.md`, and editable `data/articles/` never appear in the published artifact.

## Local checks

```bash
python3 scripts/validate.py
node --check app.js
python3 scripts/build_release.py
python3 -m http.server 8000 --directory dist
```

The source repository intentionally retains all original canonical files unchanged.
Local browser progress and bookmarks are device/browser-local.
No paid services, R2 or D1 databases, or API keys are required.
