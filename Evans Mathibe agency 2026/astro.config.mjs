// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcssVite from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://evansxm.github.io',
  base: '/EvansMathibe',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcssVite()],
    build: {
      cssMinify: true,
    },
  },
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
  },
  build: {
    assets: '_assets',
  },
});
