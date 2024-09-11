/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors: {
        'bone': '#e2d4c1ff',
        'charcoal': '#36484eff',
        'copper': '#a77452ff',
        'light-blue': '#70abbdff',
        'dark-blue': '#2c6163ff',
      },
      backgroundImage: {
        'marble': "url('/marble.jpg')"
      }
    }
  }
}
