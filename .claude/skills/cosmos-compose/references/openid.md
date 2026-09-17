# Cosmos Cloud OpenID / SSO Configuration

Cosmos supports OAuth 2.0 and OpenID Connect for centralised authentication across all your self-hosted applications. This eliminates the need for separate accounts on each service.

## How It Works

1. In the Cosmos UI, go to the OpenID tab and create a client for each application
2. Set a Client ID (e.g. `gitea`, `nextcloud`, `minio`) and a Redirect URL
3. Press "Reset Secret" to generate a client secret
4. Configure the application to use Cosmos as its OpenID provider

The OpenID discovery URL is always: `https://yourdomain.com/.well-known/openid-configuration`

## Common App Configurations

### Gitea

- **Auth Type**: OAuth2 → OpenID Connect
- **Auth Name**: `Cosmos` (capital C matters)
- **Client ID**: the ID you set in Cosmos (e.g. `gitea`)
- **Client Secret**: the generated secret
- **Icon URL**: `https://yourdomain.com/logo`
- **Auto Discovery URL**: `https://yourdomain.com/.well-known/openid-configuration`
- **Redirect URL in Cosmos**: `https://gitea.yourdomain.com/user/oauth2/Cosmos/callback`

### Nextcloud

- **Redirect URL in Cosmos**: `https://nextcloud.yourdomain.com/apps/oidc_login/oidc`
- Requires the "OpenID Connect Login" app installed from the Nextcloud app store
- Configuration goes in `config.php` (inside container at `/config/www/nextcloud/config/config.php`)
- Key config entries:
  - `'oidc_login_provider_url' => 'https://yourdomain.com'`
  - `'oidc_login_client_id' => 'nextcloud'`
  - `'oidc_login_client_secret' => 'YOUR_SECRET'`
  - `'oidc_login_button_text' => 'Log in with Cosmos'`
  - `'oidc_login_scope' => 'openid profile email groups'`
  - `'oidc_login_attributes' => array('id' => 'sub', 'name' => 'sub')`
  - `'oidc_login_default_group' => 'oidc'` (create this group in Nextcloud first)
- Set `'overwriteprotocol' => 'https'` to ensure correct redirect URLs

### Minio

- **Redirect URL in Cosmos**: `https://minio.yourdomain.com/oauth_callback`
- Configuration goes in Identity Providers → Create Configuration in the Minio admin panel
- **Config URL**: `https://yourdomain.com/.well-known/openid-configuration`
- Minio uses a policy system with three modes:
  - **Per-group policy** (recommended): set Claim Name to `role`, Claim User Infos to `true`. Create policies named `admin` and `user`.
  - **Per-user policy**: set Claim Name to `sub`, Claim User Infos to `false`. Create a policy named after each username.
  - **Single/global policy**: leave Claim Name empty, set Role Policy to a policy name (e.g. `readonly`).

## OpenID Environment Variables for cosmos-compose.json

When setting up apps with OpenID in a cosmos-compose file, you'll typically need environment variables pointing back to your Cosmos instance. Common patterns:

```json
"environment": [
  "OIDC_ISSUER=https://yourdomain.com",
  "OIDC_CLIENT_ID=myapp",
  "OIDC_CLIENT_SECRET=changeme",
  "OIDC_REDIRECT_URI=https://myapp.yourdomain.com/callback"
]
```

The exact variable names depend on the application. Always check the app's documentation for the correct environment variable names.
