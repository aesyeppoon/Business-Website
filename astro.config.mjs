import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://adaptiveelectricalsolutions.com.au",
  output: "static",
  integrations: [react()],
  build: {
    format: "directory",
  },
});
