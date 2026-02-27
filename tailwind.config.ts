import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef2ff",
          100: "#dde4ff",
          200: "#c3ceff",
          300: "#99abff",
          400: "#6e7fff",
          500: "#1a237e",
          600: "#161d6b",
          700: "#121858",
          800: "#0e1245",
          900: "#0a0d32",
        },
        accent: {
          50: "#fff8e1",
          100: "#ffecb3",
          200: "#ffe082",
          300: "#ffd54f",
          400: "#ffca28",
          500: "#ff9800",
          600: "#f57c00",
          700: "#ef6c00",
          800: "#e65100",
          900: "#bf360c",
        },
      },
      animation: {
        "pulse-ring": "pulse-ring 1.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite",
        "voice-wave": "voice-wave 1s ease-in-out infinite",
      },
      keyframes: {
        "pulse-ring": {
          "0%": { transform: "scale(0.8)", opacity: "1" },
          "100%": { transform: "scale(2)", opacity: "0" },
        },
        "voice-wave": {
          "0%, 100%": { height: "8px" },
          "50%": { height: "24px" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
