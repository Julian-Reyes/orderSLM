import preact from "@preact/preset-vite";
import { defineConfig } from "vite";

// `npm run dev` proxies the API to `make annotate-api` (127.0.0.1:8765).
export default defineConfig({
  plugins: [preact()],
  server: { host: "127.0.0.1", proxy: { "/api": "http://127.0.0.1:8765" } },
});
