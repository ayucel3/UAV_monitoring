module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}", // Adjust as necessary for your project structure
  ],
  theme: {
    extend: {
      colors:{
        "nav-text-color": "#0AA3A4",
        "nav-text-color-hover": "#0EC3C5",
        "nav-bg-color": "#CFF9F9",
        "primary-color": "#F3F6F6",
        "call-to-action": "#2FC1FF",
        "call-to-action-hover": "#3FC9FF",
        'positive-color': '#48bb78',
        'positive-color-hover': '#6dc993',
        'negative-color': '#ff6b6b',
        'negative-color-hover': '#ff8989',
        "warning-color": "#f39c12",
        "warning-color-hover": "#f7b731",
      }
    },
  },
  plugins: [],
}
