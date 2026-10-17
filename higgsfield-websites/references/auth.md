# Skill: Auth Boundary

Use this when a website needs signed-in user state, login, logout, account-gated
pages, profile loading, or protected file downloads. This template does not
implement its own identity provider. The platform owns auth and exposes a small
contract to the website.

## Contract

- Browser code must call app-local endpoints only.
- Server code may call `https://fnf.internal/*`.
- Do not send auth headers to `fnf.internal`; identity is attached by the
  platform/runtime automatically.
- Do not call `https://fnf.internal/*` from the browser. It is not reachable
  there and would be a security bug even if it were.

Endpoints:

| Purpose | Endpoint | Caller |
|---|---|---|
| Current user profile | `GET https://fnf.internal/user` | server only |
| Browser-safe user proxy | `GET /api/user` | frontend/browser |
| Start login | `GET /__auth/login?return=<path>` | browser navigation |
| Start logout | `GET /__auth/logout?return=<path>` | browser navigation |

`GET https://fnf.internal/user` returns the current user's profile JSON and
returns `401` when the visitor is not signed in.

`GET /api/user` must call `https://fnf.internal/user` server-side and return the
same status code and JSON body unchanged. This endpoint is the only user-profile
endpoint browser components should fetch.

## Choose The Correct Auth Mode

There are two different auth concepts. Pick intentionally:

| Website need | Auth mode | Required behavior |
|---|---|---|
| Higgsfield SDK/model generation, media upload, cost preview, and feed/history | Higgsfield platform auth | Use `/api/user`, a signed-out login link, and server-side `https://fnf.internal` guards; platform chrome owns logout, account, and wallet UI |
| The generated website's own product accounts, for example todos, notes, CRM records, dashboards, memberships | In-app auth | Build app-local auth/session/storage. Do not call `fnf.internal/user` unless the website also uses Higgsfield SDK features |
| Both generation and product accounts | Both, kept separate | Gate SDK routes with Higgsfield auth and product data with in-app auth. Label UI clearly and never mix identities |

Higgsfield platform auth is implicit when the product's end-user functionality
actually uses Higgsfield SDK-backed services (for example generation,
Higgsfield media upload, workspace selection, or generation history), even if
the user did not say "add sign in." Mentioning a provider, listing supplied
assets, or authorizing build-time asset work does not by itself make a
standalone website an SDK app; route by product behavior as defined in
`references/website-flow.md` and `references/app-flow.md`.

If the prompt only asks for "sign in" for a normal generated product and does not
use Higgsfield generation/profile/credits, default to in-app sign in. Do not use
`/__auth/login` as the product's account system unless the prompt specifically
asks for Higgsfield account sign-in.

## Required `/api/user` Route

Create a TanStack Start server route, not a separate Hono/Express API:

```ts
// app/src/routes/api/user.ts
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/api/user')({
  server: {
    handlers: {
      GET: async () => {
        const upstream = await fetch('https://fnf.internal/user')
        const body = await upstream.text()

        return new Response(body, {
          status: upstream.status,
          headers: {
            'content-type': upstream.headers.get('content-type') ?? 'application/json',
            'cache-control': 'no-store',
          },
        })
      },
    },
  },
})
```

Notes:

- Preserve upstream status. A `401` from `fnf.internal/user` must remain `401`
  at `/api/user`.
- Preserve upstream JSON body unchanged. Do not reshape fields in the proxy.
- Add `cache-control: no-store`; user identity is per request.
- Do not add `Authorization`, cookies, service secrets, `hf-user-id`, or
  marketplace headers. The platform injects identity on server egress.
- Do not expose raw fnf internal URLs to the UI.

## Frontend User Loader Pattern

Use `/api/user` from browser-only queries, effects, or client components. This
relative-fetch helper must not run during SSR:

```ts
export async function fetchCurrentUser() {
  const response = await fetch('/api/user', { credentials: 'include' })
  if (response.status === 401)
    return null
  if (!response.ok)
    throw new Error('Failed to load user')
  return response.json()
}
```

For a loader that can run during SSR, call a server function that delegates to
`requireCurrentUser()` from `auth.server.ts`; do not call the browser-relative
fetch helper or statically import server-only auth code into a client module:

```ts
import { createServerFn } from '@tanstack/react-start'

export const loadCurrentUser = createServerFn({ method: 'GET' })
  .handler(async () => {
    const { requireCurrentUser } = await import('@/lib/auth.server')
    const auth = await requireCurrentUser()
    if (auth.ok)
      return auth.user
    if (auth.status === 401)
      return null
    throw new Error(`Failed to load user (${auth.status})`)
  })
```

Call `loadCurrentUser()` from the route loader. The signed-out result is `null`;
account-required pages may redirect or render the platform sign-in action.

## Login

Login is browser navigation, not an SDK call:

```ts
function login(returnPath = window.location.pathname + window.location.search) {
  window.location.href = `/__auth/login?return=${encodeURIComponent(returnPath)}`
}
```

Rules:

- Use the current path as `return` by default.
- Encode the return path.
- Keep the return path app-local. Do not pass full external URLs.
- After login completes, the platform redirects back to `return`; then
  `/api/user` should succeed.

## Logout

`GET /__auth/logout?return=<path>` is a platform-owned browser route, not an
app endpoint. Integrated generation apps do not render a logout button or link;
the platform's own chrome controls sign-out. Never clear platform cookies
manually or call `fnf.internal` for logout. If an explicitly separate product
account needs logout, implement only that product's own session contract.

## Authenticated File Downloads

Apps may run inside a cross-origin authenticated iframe. Native download
navigation may not preserve that embedded authentication context and can return
`401 Unauthorized`. For a protected app-local `/api/...` file, NEVER use:

- `<a href="/api/..." download>`
- `window.location`
- `window.open`

Fetch the file with credentials and download the successful response through a
temporary Blob URL instead. This is a browser-only helper: call it from an event
handler, never during SSR or module initialization.

```ts
export async function downloadAuthenticatedFile(
  url: string,
  filename: string,
): Promise<void> {
  const downloadUrl = new URL(url, window.location.href)
  if (
    downloadUrl.origin !== window.location.origin
    || !downloadUrl.pathname.startsWith('/api/')
  ) {
    throw new Error('Authenticated downloads require an app-local /api/... URL')
  }

  const response = await fetch(downloadUrl, {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(`Download failed (${response.status})`)
  }

  const blobUrl = URL.createObjectURL(await response.blob())
  const anchor = document.createElement('a')

  try {
    anchor.href = blobUrl
    anchor.download = filename
    anchor.style.display = 'none'
    document.body.appendChild(anchor)
    anchor.click()
  }
  finally {
    anchor.remove()
    window.setTimeout(() => URL.revokeObjectURL(blobUrl), 0)
  }
}
```

Call the helper from a real Quanta button. The handler owns loading state and
must catch and surface download errors through designed inline feedback or a
toast.

```tsx
<Button
  type="button"
  disabled={isDownloading}
  onClick={handleDownload}
>
  {isDownloading ? 'Downloading…' : 'Download'}
</Button>
```

Requirements:

- The protected server route must re-check the current user and authorize that
  specific file. Return `401`/`403` for unauthenticated/forbidden requests;
  never redirect a download fetch to an HTML login page. Serve the file with a
  truthful `Content-Type` and, when the route owns the filename, matching
  `Content-Disposition`.
- Pass `credentials: 'include'`. The helper enforces a same-origin `/api/...`
  URL; never weaken that check or pass it an untrusted arbitrary URL.
- Check `response.ok` before reading the body.
- Show loading and error states.
- Remove every temporary element and revoke every object URL after the click has
  had a browser task to start the download.
- Do not nest a `<button>` inside an `<a>`.
- Raw download links are allowed only for public static files or self-contained
  signed URLs that require no session.
- For large files, prefer a backend-generated short-lived signed URL with
  `Content-Disposition: attachment` to avoid buffering the entire file in
  browser memory.
- Test downloads inside the Higgsfield iframe, not only with the app opened
  directly. Test both newly generated files and previously saved files.
- If a sandboxed host iframe blocks programmatic downloads, the host must grant
  its download capability. Report that platform constraint; do not work around
  it by navigating to the protected URL.

For generated-media exports, also apply `references/fnf-sdk.md` → “Output and
download format contract” so the downloaded bytes, MIME type, extension, and
filename agree. A direct `getRawUrl()` link is safe only when it is public or a
self-contained signed URL that needs no session; otherwise use the helper.

## Auth UI Rules

- Signed-out state should show a clear sign-in action using the website's normal
  Quanta button style.
- Do not build email/password forms unless the task explicitly asks for a custom
  identity UI and the platform supports it. The default is `/__auth/login`.
- Do not show fake profile data while loading. Use skeletons or neutral loading
  states.
- Never render emails, names, workspace names, tokens, or raw profile payloads
  into observability events.

## FNF SDK Interaction

For generated websites using the fnf SDK, create SDK adapters server-side with
`baseUrl: 'https://fnf.internal'`. The auth boundary above is for website UI
identity. SDK calls should still use server functions or server-only modules and
must not be made directly from browser components.

## Required Auth For SDK Features

Any website that uses SDK-backed generation must be authenticated. This includes:

- generation submit, poll, cancel, feed/history, and cost preview
- media upload, media resolve, and media reads
- profile, workspace switch, wallet, and credits
- any UI that exposes model settings or writes paid/user-owned outputs

When the product's end-user behavior uses Higgsfield SDK features (for example
generation, SDK-backed media upload, or workspace/history operations), platform
auth is implicit even if the user did not say "add sign in." A product-only
upload or build-time asset operation does not by itself require Higgsfield
auth; use the mode selected above. For SDK-backed behavior, require `/api/user`,
a signed-out login link, and server-side auth guards; put model-specific cost
preview/confirmation and generation history in the app. Do not duplicate
platform-owned logout, profile, wallet-balance, or account-credit chrome; expose
workspace selection only if the active SDK contract requires it.

The only exception is an offline/mock demo the user EXPLICITLY asked for — memory
adapters only, never calling fnf.internal, apps-marketplace, media upload, or
profile endpoints. Never choose a mock as the default: a real SDK app is
end-to-end, with a real backend and D1 persistence (see references/app-flow.md rule 3a).

Required flow:

1. Implement `/api/user`.
2. Browser loads `/api/user` before rendering SDK-backed controls.
3. If `/api/user` returns `401`, show a signed-out state and a Quanta sign-in
   button that navigates to `/__auth/login?return=<current path>`.
4. Disable or hide submit/upload/cost/profile controls while signed out.
5. Every server function or server route that performs an SDK operation must
   call `https://fnf.internal/user` first and stop on `401`.

The UI gate is for experience; the server-side auth check is the actual safety
boundary. Do not rely on "button hidden when signed out" as protection.

If a page needs both user state and generation data:

1. Browser calls `/api/user` for display/auth gate.
2. Server function submits/reads jobs through the selected SDK adapter.
3. Browser receives only safe website data: user-safe fields, generation ids,
   statuses, display credits, and sanitized errors.

## Server Auth Guard Pattern

Use a small server-only helper for SDK server functions:

```ts
// app/src/lib/auth.server.ts
export async function requireCurrentUser() {
  const response = await fetch('https://fnf.internal/user')

  if (response.status === 401) {
    const body = await response.json().catch(() => null)
    return {
      ok: false as const,
      status: 401,
      body,
    }
  }

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    return {
      ok: false as const,
      status: response.status,
      body,
    }
  }

  const user = await response.json()
  return {
    ok: true as const,
    user,
  }
}
```

Then guard SDK operations:

```ts
const auth = await requireCurrentUser()
if (!auth.ok) {
  return new Response(JSON.stringify(auth.body), {
    status: auth.status,
    headers: { 'content-type': 'application/json' },
  })
}

// Safe to create SDK adapter/client and submit/read user-owned data here.
```

For `createServerFn`, return a typed `{ ok: false, code: 'unauthorized' }`
result or throw/redirect according to the website's route behavior, but still check
auth before the SDK call.

## Signed-Out UI Pattern

Use this Quanta pattern for **app-shaped** generation/tool UIs. Marketing
waitlists and landing pages should use custom sign-in chrome per
`references/design-taste-frontend.md` instead of Quanta buttons.

```tsx
import { Button } from '@higgsfield/quanta/button'

function SignInRequired() {
  return (
    <div className="grid min-h-72 place-items-center rounded-lg border border-q-border-subtle bg-q-background-secondary p-6 text-center">
      <div className="grid max-w-sm gap-3">
        <h2 className="text-q-title-md-semi-bold">Sign in to generate</h2>
        <p className="text-q-body-sm-regular text-q-text-secondary">
          Generation, uploads, credits, and history are connected to your account.
        </p>
        <div>
          <Button
            onClick={() => {
              const returnPath = window.location.pathname + window.location.search
              window.location.href = `/__auth/login?return=${encodeURIComponent(returnPath)}`
            }}
          >
            Sign in
          </Button>
        </div>
      </div>
    </div>
  )
}
```

Do not render active prompt fields, upload controls, generate buttons, cost
buttons, workspace switchers, or job feeds as usable controls while signed out.

## Anti-Patterns

```ts
await fetch('https://fnf.internal/user') // bad in browser code
await fetch('/api/user')                 // good in browser code
```

```ts
fetch('https://fnf.internal/user', {
  headers: { Authorization: `Bearer ${token}` },
}) // bad; platform attaches identity automatically
```

```ts
window.location.href = '/login' // bad; not the platform auth route
window.location.href = '/__auth/login?return=%2Fdashboard' // good
```

```ts
// bad: anonymous generation surface
await jobs.submit(input)

// good: server-side auth gate first
const auth = await requireCurrentUser()
if (!auth.ok) {
  return new Response(JSON.stringify(auth.body), {
    status: auth.status,
    headers: { 'content-type': 'application/json' },
  })
}
await jobs.submit(input)
```
