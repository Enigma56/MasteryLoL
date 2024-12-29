/** @type {import('tailwindcss').Config} */
export default {
  content: [
      "./src/**/*.{html,js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        transparent: 'transparent',
        current: 'currentColor',
        hexmagic: {
          1: '#CDFAFA',
          2: '#0AC8B9',
          3: '#0397AB',
          4: '#005A82',
          5: '#0A323C',
          6: '#091428',
          7: '#0A1428',
        },
        hexmetal: {
          1: '#F0E6D2',
          2: '#C8AA6E',
          3: '#C89B3C',
          4: '#785A28',
          5: '#463714',
          6: '#32281E',
        },
        hextech: {
          1: '#A09B8C',
          2: '#5B5A56',
          3: '#3C3C41',
          cool: '#1E282D',
          black: '#010A13'
        },
      },
    },
  },
  plugins: [],
}

