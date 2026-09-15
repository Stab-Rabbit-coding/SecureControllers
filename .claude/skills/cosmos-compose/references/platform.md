# Cosmos Cloud Platform Reference

## Installation & Setup

### Docker Run Command

```
docker run -d -p 80:80 -p 443:443 -p 4242:4242/udp --privileged --name cosmos-server -h cosmos-server --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /:/mnt/host -v /var/lib/cosmos:/config azukaar/cosmos-server:latest
```

Key mount points:

- `/var/run/docker.sock:/var/run/docker.sock` — Docker socket for container management (required)
- `/var/lib/cosmos:/config` — Cosmos config storage (recommended as bind mount for backups)
- `/:/mnt/host` — Host filesystem access for creating bind mount folders during compose imports (optional)

The `--privileged` flag is required for SELinux/AppArmor systems and for the Constellation VPN. Without it, add `--cap-add=NET_ADMIN` for Constellation only.

Port 4242/udp is for the Constellation VPN.

### Setup Wizard Steps

1. **Docker**: Verifies Docker socket access
2. **Database**: Creates a secure MongoDB instance (auto) or connects to an external one. Connection string format: `mongodb+srv://<user>:<pass>@<host>`
3. **HTTPS**: Options are Let's Encrypt (recommended), own certificate, self-signed, or HTTP only. DNS challenge supports wildcard certs — hostname must be bare domain (e.g. `mydomain.com` not `www.mydomain.com`)
4. **Admin Account**: Creates the admin user. Set an email to enable password resets.

### Environment Variables

- `COSMOS_HTTP_PORT` / `COSMOS_HTTPS_PORT` — Custom ports
- `COSMOS_HOSTNAME` — Hostname/IP
- `COSMOS_HTTPS_MODE` — `SELFSIGNED`, `LETSENCRYPT`, `PROVIDED`, or `DISABLED`
- `COSMOS_MONGODB` — MongoDB connection string
- `COSMOS_SERVER_COUNTRY` — Two-letter country code to whitelist your country
- `COSMOS_LOG_LEVEL` — `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `COSMOS_GENERATE_MISSING_AUTH_CERT` — Auto-generate auth cert if missing
- `COSMOS_TLS_CERT` / `COSMOS_TLS_KEY` — Custom TLS cert/key
- `COSMOS_AUTH_PRIV_KEY` / `COSMOS_AUTH_PUBLIC_KEY` — Auth key paths

### Architecture Support

AMD64 and ARM64 only. Both OS and CPU must be 64-bit. Raspberry Pi 3+ or Zero 2 W minimum.

## ServApps (Container Management)

ServApps are Cosmos's name for Docker containers. Key concepts:

### Security Indicators

- **Port colours**: Orange ports are exposed to the internet — avoid exposing HTTP ports, use routes instead
- **Network colours**: Orange network means the container is on the shared bridge — use isolated networks instead
- **Force Secure checkbox**: Automatically un-exposes ports and moves to an isolated network

### Container Actions

Start, Stop, Restart, Pause, Unpause, Recreate (destroys and recreates), Kill (immediate stop), Update (pulls latest image and recreates).

### Auto-Updates

Cosmos checks for image updates every 6 hours. Containers must use an updatable tag (e.g. `latest`, `stable`) not a pinned version.

### Container Settings

Editable from the UI:

- Image, restart policy, environment variables, labels (Docker tab)
- Networks and port mappings (Networks tab)
- Volume mounts — bind or named volume (Volumes tab)
- Terminal access — attach to main process TTY or spawn a new bash shell

### Importing Compose Files

Use the "Import Docker Compose" button on the ServApps page. Supports both docker-compose.yml and cosmos-compose.json. Unsupported docker-compose features are silently ignored.

## URL / Route Management

### Route Types

- **SERVAPP** — Proxy to a Cosmos-managed container (most common)
- **PROXY** — Proxy to an external URL not managed by Cosmos
- **REDIRECT** — HTTP redirect
- **STATIC** — Serve static files / open directory
- **SPA** — Single-page application (routes all paths to index.html)

### Security Features Per Route

- **SmartShield** — Anti-bot/DDoS with configurable strictness (Normal/Lenient/Strict)
  - Time budget (default 2h per user per hour)
  - Byte budget (default 150GB per user per hour)
  - Per-user simultaneous requests (default 24)
  - Global simultaneous requests (default 250)
  - Privileged users (exempt from shield, default: admin only)
- **Authentication** — Require Cosmos login
- **Admin Only** — Restrict to admin users
- **Rate Limiting** — Requests per minute
- **Timeout** — Request timeout in ms
- **Block Common Bots** — User-agent filtering
- **Block requests without referrer** — Prevents direct API calls (not recommended, breaks mobile apps)
- **IP Whitelist** — Restrict to specific IPs/ranges
- **Constellation Only** — Restrict to VPN-connected users

### Chaining Proxies (IP Hiding)

To hide your server's IP (like Cloudflare Proxy):

1. Server A (private, main) and Server B (public, proxy)
2. DNS A record points to Server B
3. On Server B: create PROXY route with target `http://ServerA_IP:port` and set OverwriteHostHeader to the domain name
4. Secure the A↔B link with Constellation VPN or HTTPS

## Constellation VPN

Cosmos's built-in mesh VPN based on Nebula. Key features:

- P2P mesh networking — devices connect directly where possible
- Lighthouse nodes relay traffic when direct connection fails (essential behind CGNAT)
- Automatic DNS integration — Cosmos rewrites all URLs to use VPN IPs when connected
- Device types: regular nodes and lighthouses (publicly accessible relay points)
- Default subnet: 192.168.201.x (main server typically .1)

Requirements:

- Port 4242/udp exposed on the Cosmos container
- `--privileged` flag or `NET_ADMIN` capability
- Cannot coexist with another VPN (e.g. WireGuard) on the same server

## DNS Challenge & Wildcard Certificates

- Set hostname to bare domain (`mydomain.com`)
- Select DNS provider in config (uses LEGO under the hood, no manual env vars needed)
- Check "Wildcard Certificate" — Cosmos requests `*.mydomain.com` automatically
- Supported providers: see https://go-acme.github.io/lego/dns/
- Cloudflare: use either API KEY or TOKEN, not both, and in the correct fields

## Email (SMTP)

Configure in Cosmos settings. Required for:

- User invitations
- Password reset links

Supports any SMTP server. Gmail requires an App Password.

## Geo-Blocking

Configurable per-country blocking. Blocked by default: CN, RU, TR, BR, BD, IN, NP, PK, LK, VN, ID, IR, IQ, EG, AF, RO. Override with `COSMOS_SERVER_COUNTRY` env var.

## IPv6

Requires Docker IPv6 support. Edit `/etc/docker/daemon.json`:

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "your:ipv6:range::/64"
}
```

## Config File

Located at `/var/lib/cosmos/cosmos-config.json` (or custom config mount). All settings are editable here. To re-run setup: set `NewInstall` to `true` and restart.

## Backups

Cosmos exports all container definitions to a single file in the config folder. Use this to restore or migrate servers.

## Common Troubleshooting

### General

- Always check `docker logs cosmos-server` first
- Edit config directly at `/var/lib/cosmos/cosmos-config.json` in rescue situations
- Flush and restart: delete `/var/lib/cosmos` folder and restart container
- Re-run setup: set `NewInstall: true` in config and restart

### HTTPS Issues

- Domain not pointing to server
- New subdomain not in DNS yet
- Cloudflare proxy enabled (disable the orange cloud, or use DNS challenge)
- DNS challenge tokens incorrect (Cloudflare: KEY vs TOKEN confusion)
- Cosmos falls back to HTTP mode when cert fails

### Database Issues

- Check MongoDB is running and accessible
- Verify connection string in config
- Check credentials

### Constellation VPN Issues

- Outdated client certificate → recreate device from scratch
- Port 4242/udp not exposed
- Missing `--privileged` flag → "Failed to get a tun/tap device"
- No lighthouse in network (required if behind CGNAT)
- Another VPN (WireGuard) running on same server
- Port 4242 busy → restart Cosmos container
