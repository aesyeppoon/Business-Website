import { defineConfig } from "astro/config";
import react from "@astrojs/react";

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  site: "https://adaptiveelectricalsolutions.com.au",
  output: "static",
  integrations: [react()],

  build: {
    format: "directory",
  },

  adapter: cloudflare()
});