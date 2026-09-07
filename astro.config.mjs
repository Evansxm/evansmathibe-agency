import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import preact from '@astrojs/preact';

export default defineConfig({
  site: 'https://evansxm.github.io',
  base: '/evansmathibe-agency',
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    mdx(),
    preact({ compat: true }),
  ],
  output: 'static',
});
