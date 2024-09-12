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
      minHeight: {
  			"aspect": "10vw"
			},
      backgroundImage: {
        'marble': "url('/marble.jpg')",
        'marble-fade': "linear-gradient(156deg, rgba(0,0,0,0) 10%, rgba(54,72,78,1) 15%, rgba(54,72,78,1) 85%, rgba(0,0,0,0) 90%), url('/marble.jpg')"
      }
    }
  }
}
