import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  site: "https://www.adaptive-electrical.com.au",
  output: "static",
  integrations: [react()],
  build: {
    format: "directory",
  },
});
