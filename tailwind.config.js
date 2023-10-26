/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');
module.exports = {
  content: ["templates/**/*.html"],
  theme: {
    fontFamily: {
      'brand': ['Roboto', 'system-ui'],
    },
    extend: {
      colors: {
        'accent': colors.yellow,
        'brand': colors.emerald,
        'gs': colors.slate,
      },
      lineHeight: {
        '12': '3.75rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

