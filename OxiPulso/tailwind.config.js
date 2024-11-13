/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Analiza todos los archivos HTML en el directorio templates y sus subdirectorios
    "./static/js/**/*.js" // Analiza todos los archivos JS en el directorio static/js y sus subdirectorios
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
