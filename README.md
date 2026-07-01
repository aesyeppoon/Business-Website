# Adaptive Electrical Solutions

Astro website for Adaptive Electrical Solutions, built as a static site for GitHub and Cloudflare Pages.

## Local development

```sh
npm install
npm run dev
```

## Production build

```sh
npm run build
```

Cloudflare Pages settings:

- Build command: `npm run build`
- Build output directory: `dist`
- Node.js version: `22`

The contact form opens a pre-filled email in the visitor's email application. For direct form delivery later, replace the small client-side handler in `src/pages/contact.astro` with a Cloudflare Pages Function and email provider.
