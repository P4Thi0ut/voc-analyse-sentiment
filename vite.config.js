import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// CI_PAGES_URL is provided by GitLab CI when deploying to GitLab Pages.
// We extract the pathname so the app works both locally (/) and on Pages (/repo-name/).
const pagesUrl = process.env.CI_PAGES_URL          // e.g. https://group.gitlab.io/project
const base     = pagesUrl ? new URL(pagesUrl).pathname + '/' : '/'

export default defineConfig({
  base,
  plugins: [vue()],
})

