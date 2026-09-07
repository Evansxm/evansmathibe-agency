/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        paper: '#F1ECE2',
        ink: '#1B1712',
        ember: '#DE656D',
        'ember-deep': '#B13A42',
        brass: '#A8873F',
        slate: '#4B5A5E',
      },
      fontFamily: {
        display: ['"Clash Display"', 'sans-serif'],
        sans: ['"Switzer"', 'sans-serif'],
        serif: ['"Instrument Serif"', 'serif'],
      },
      letterSpacing: {
        tightest: '-0.04em',
        widest: '0.15em',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
