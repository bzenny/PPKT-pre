# Environment / release separation

| Environment | GitHub | Cloudflare | Supabase | Provider | Funds |
|---|---|---|---|---|---|
| `local` | cloned branch | local dev | local emulator/none | fake | synthetic only |
| `staging` | reviewed branch | preview/staging worker | isolated staging project | simulator | synthetic only |
| `prelaunch-demo` | signed review/tag | controlled demo domain | isolated demo project | simulator | synthetic only |
| `production` | **unapproved** | **uncreated** | **uncreated** | **no contracts** | **prohibited until separate authorizations** |

**Policy:** Never reuse production credentials or customer identity data in staging/AI Studio. Environment values belong in managed secrets, not this repo. Test rollback and state reconciliation separately: reverting code cannot reverse external bank or chain transactions.
