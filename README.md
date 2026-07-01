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

Cloudflare settings:

- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`
- Build output directory: `dist`
- Node.js version: `22`

## Contact form

The quote form posts to `/api/contact` and sends through Resend from the Cloudflare Worker.

Set these Cloudflare environment variables before going live:

- `RESEND_API_KEY` - secret Resend API key.
- `CONTACT_TO_EMAIL` - destination inbox, defaults to `aes.yeppoon@gmail.com`.
- `RESEND_FROM_EMAIL` - verified Resend sender, defaults to `Adaptive Electrical Solutions <noreply@adaptive-electrical.com.au>`.
