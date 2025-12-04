/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-blue': '#0f172a',
        'gold': '#fbbf24',
        'increase-green': {
          400: '#10b981',
          600: '#047857'
        },
        'decrease-red': {
          400: '#ef4444',
          600: '#b91c1c'
        },
        'oscillation-gray': '#64748b'
      },
      animation: {
        'pulse-gold': 'pulse-gold 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'flash-red': 'flash-red 1s ease-in-out infinite alternate'
      },
      keyframes: {
        'pulse-gold': {
          '0%, 100%': { 
            'box-shadow': '0 0 0 0 rgba(251, 191, 36, 0.7)'
          },
          '50%': { 
            'box-shadow': '0 0 0 10px rgba(251, 191, 36, 0)'
          }
        },
        'flash-red': {
          '0%': { 
            'box-shadow': '0 0 0 0 rgba(239, 68, 68, 0.7)'
          },
          '100%': { 
            'box-shadow': '0 0 0 10px rgba(239, 68, 68, 0)'
          }
        }
      }
    },
  },
  plugins: [],
}