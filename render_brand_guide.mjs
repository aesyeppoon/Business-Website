import fs from "node:fs";
import path from "node:path";
import sharp from "file:///C:/Users/Nick_/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/lib/index.js";

const input = String.raw`C:\Users\Nick_\Documents\Business Website\brand-guide\Adaptive_Electrical_Solutions_Brand_Guide.pdf`;
const output = String.raw`C:\Users\Nick_\Documents\Business Website\brand-guide\qa`;

fs.mkdirSync(output, { recursive: true });
const metadata = await sharp(input, { density: 150 }).metadata();
const pageCount = metadata.pages ?? 1;

for (let page = 0; page < pageCount; page += 1) {
  await sharp(input, { density: 150, page })
    .png()
    .toFile(path.join(output, `page-${page + 1}.png`));
}

console.log(`Rendered ${pageCount} pages to ${output}`);
