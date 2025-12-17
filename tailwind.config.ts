import type { Config } from "tailwindcss";

// Generated color palettes
const accent = {
  200: "#fcf7f6ff",
  600: "#c64533ff",
  900: "#a93d2fff",
  950: "#3e1610ff",
};
const gray = {
  100: "#f5f6f8",
  200: "#eceef2",
  300: "#c0c2c7",
  400: "#888b96",
  500: "#545861",
  700: "#353841",
  800: "#24272f",
  900: "#17181c",
};

const config: Config = {
  content: [
    "./src/**/*.{astro,html,js,ts,jsx,tsx,md,mdx}",
    "./node_modules/@astrojs/starlight/components/**/*.{astro,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        accent,
        gray,
        "tc-primary": "#dc4e3bff",
      },
    },
  },
  plugins: [],
};

export default config;
