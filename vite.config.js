import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// CI_PAGES_URL is provided by GitLab CI when deploying to GitLab Pages.
// For GitHub Pages the repo lives at https://<user>.github.io/voc-analyse-sentiment/
const pagesUrl = process.env.CI_PAGES_URL          // e.g. https://group.gitlab.io/project
const base     = pagesUrl ? new URL(pagesUrl).pathname + '/' : '/voc-analyse-sentiment/'

export default defineConfig({
  base,
  plugins: [vue()],
})
