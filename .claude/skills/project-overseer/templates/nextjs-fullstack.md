# Next.js Full-Stack Project Standards (Project Type — Layered)

> Stacked with the TS/JS language template + React frontend template. Only Next.js-specific file structure conventions are listed here.

## Project Structure (App Router File Conventions)

```text
app/
  layout.tsx          # Root layout (required)
  page.tsx            # Home page
  loading.tsx         # Loading state (optional)
  error.tsx           # Error boundary (optional)
  not-found.tsx       # 404 page (optional)
  api/                # API routes
    route.ts
  (group)/            # Route groups (does not affect URL)
  blog/
    [slug]/
      page.tsx        # Dynamic route
  _components/        # Private components (underscore prefix, not routed)
  _lib/               # Private utility functions
```

### Directory & File Conventions

- **Underscore `_` prefix marks private directories**: App Router will not treat `_components`, `_lib` as routes
- **layout.tsx is persistent**: switching pages under the same layout does not remount the layout. Do not put page-level data fetching in layout
- **error.tsx must include 'use client'** (it's an interactive component)
- **loading.tsx automatically wraps page.tsx and child layouts** — no manual Suspense needed; but manual Suspense gives finer control when needed

## Data Fetching

- **Server Components by default** — fetch data directly in async components, no useEffect needed
- **Use `fetch()` with `cache: 'no-store'` or `next: { revalidate }`** for dynamic data
- **Route Handlers (API routes) for external consumption**, not internal data passing
- **Server Actions for mutations** (form submissions, data writes) — keep them alongside the component or in a `_actions/` directory

## Performance & SEO

- **Metadata API** for SEO: export `metadata` or `generateMetadata` from page/layout files
- **Image Optimization**: use `next/image`, specify `width`/`height` or `fill`, always provide `alt`
- **Font Optimization**: use `next/font` to load fonts with zero layout shift
- **Streaming**: wrap slow data-fetching sections in `<Suspense>` — loading.tsx handles top-level streaming automatically

## Testing

- Framework: Vitest + React Testing Library + MSW (for API mocking)
- E2E: Playwright or Cypress for critical user flows
- File naming: co-locate tests with the component or page
