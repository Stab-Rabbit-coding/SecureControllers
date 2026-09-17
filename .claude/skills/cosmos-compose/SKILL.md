---
name: cosmos-compose
description: >
  Generate cosmos-compose.json files and administer Cosmos Cloud. Covers
  services, volumes, routes, reverse proxy, OpenID/SSO, Constellation VPN,
  docker-compose conversion, and container hardening.
---

# Cosmos-Compose Skill

Generate valid `cosmos-compose.json` files and configure any aspect of a [Cosmos Cloud](https://cosmos-cloud.io) deployment: reverse proxy routes, OpenID SSO, Constellation VPN, container management.

## Reference Files

Read these when the task requires deeper knowledge:

- **`references/platform.md`** - Cosmos Cloud install, setup wizard, env vars, ServApp management, URL/route security, Constellation VPN, DNS challenge, SMTP, geo-blocking, IPv6, config-file editing, backups, troubleshooting. For Cosmos admin, server setup, debugging, or platform features beyond cosmos-compose.
- **`references/openid.md`** - OpenID Connect / SSO for apps behind Cosmos (Gitea, Nextcloud, Minio examples). For SSO, OAuth, or centralised auth.

## What is Cosmos-Compose?

A Docker Compose derivative expressed as JSON (or YAML), describing services, volumes, and networks Cosmos manages. Key difference from Docker Compose: each service can have a `routes` array configuring Cosmos's built-in reverse proxy. Cosmos also converts `links` into proper Docker networks (not deprecated Docker links).

## Top-Level Structure

A cosmos-compose.json has three top-level keys:

```json
{
  "services": { ... },
  "volumes": [ ... ],
  "networks": { ... }
}
```

`services` is a map of service-name to service definition. `volumes` is an array of volume objects. `networks` is a map of network-name to network definition. All three are optional — most simple deployments only need `services`.

## Service Definition

Each service is keyed by a descriptive name (e.g. `"jellyfin"`, `"nextcloud"`, `"postgres-db"`). The service object supports these fields:

### Required fields

- `"image"` (string): The Docker image, e.g. `"jellyfin/jellyfin:10.10.6"`
- `"container_name"` (string): The container name, e.g. `"jellyfin"`

### Common fields

- `"restart"` (string): Restart policy — `"always"`, `"unless-stopped"`, `"on-failure"`, or `"no"`
- `"environment"` (array of strings): Env vars in `"KEY=value"` format
- `"volumes"` (array of mount objects): Volume/bind mounts (see Volume Mounts below)
- `"ports"` (array of strings): Port mappings in `"host:container"` or `"host:container/protocol"` format
- `"routes"` (array of route objects): Cosmos reverse proxy routes (see Routes below)
- `"labels"` (map of string to string): Docker labels
- `"depends_on"` (array of strings): Service dependencies by container name
- `"networks"` (map): Network attachments with optional aliases and IP addresses
- `"links"` (array of strings): Creates a Cosmos-managed network between linked containers (preferred over raw Docker links)

### Less common fields

- `"command"` (string): Override the container command
- `"entrypoint"` (string): Override the entrypoint
- `"devices"` (array of strings): Device mappings, e.g. `"/dev/dri:/dev/dri"` for GPU passthrough
- `"expose"` (array of strings): Expose ports without publishing to host
- `"user"` (string): Run as user, e.g. `"1000:1000"`
- `"hostname"` (string): Container hostname
- `"domainname"` (string): Container domain name
- `"privileged"` (boolean): Run in privileged mode
- `"network_mode"` (string): Network mode, e.g. `"host"`, `"bridge"`, `"none"`
- `"working_dir"` (string): Working directory inside the container
- `"tty"` (boolean): Allocate a TTY
- `"stdin_open"` (boolean): Keep stdin open
- `"cap_add"` (array of strings): Linux capabilities to add, e.g. `["NET_ADMIN"]`
- `"cap_drop"` (array of strings): Linux capabilities to drop
- `"dns"` (array of strings): Custom DNS servers
- `"extra_hosts"` (array of strings): Extra hosts in `"hostname:ip"` format
- `"security_opt"` (array of strings): Security options, e.g. `["no-new-privileges:true"]`
- `"sysctls"` (map of string to string): Sysctl settings
- `"mac_address"` (string): MAC address override
- `"stop_signal"` (string): Stop signal
- `"stop_grace_period"` (integer): Grace period in seconds
- `"healthcheck"` (object): Health check config with `"test"` (array), `"interval"` (int), `"timeout"` (int), `"retries"` (int), `"start_period"` (int)

### Volume Mounts

Volume entries in the `"volumes"` array on a service use Docker's mount format:

```json
{
  "source": "/host/path/or/volume-name",
  "target": "/container/path",
  "type": "bind"
}
```

`type` is either `"bind"` (for host path mounts) or `"volume"` (for named Docker volumes). If using named volumes, the volume should also be declared in the top-level `"volumes"` array.

### Routes (Cosmos Reverse Proxy)

The `routes` array is the Cosmos-specific extension. Each route object configures a reverse proxy URL in Cosmos. The route fields are:

```json
{
  "Name": "jellyfin-route",
  "Description": "Jellyfin Media Server",
  "UseHost": true,
  "Host": "jellyfin.yourdomain.com",
  "UsePathPrefix": false,
  "PathPrefix": "",
  "Timeout": 14400000,
  "ThrottlePerMinute": 0,
  "CORSOrigin": "",
  "StripPathPrefix": false,
  "AuthEnabled": false,
  "Target": "http://jellyfin:8096",
  "SmartShield": {
    "Enabled": true
  },
  "Mode": "SERVAPP",
  "BlockCommonBots": false,
  "AcceptInsecureHTTPSTarget": false
}
```

#### Route fields explained

- **`Name`** (string, required): A unique identifier for this route, e.g. `"myapp-web"`. This is the route's internal name in Cosmos.
- **`Description`** (string): A human-readable description shown in the Cosmos UI.
- **`UseHost`** (boolean): Whether to match on a hostname. Set to `true` when using a subdomain.
- **`Host`** (string): The hostname/domain for this route, e.g. `"app.yourdomain.com"`. Only used when `UseHost` is `true`.
- **`UsePathPrefix`** (boolean): Whether to match on a path prefix. Typically `false` for SERVAPP routes.
- **`PathPrefix`** (string): The path prefix, e.g. `"/myapp"`. Only used when `UsePathPrefix` is `true`.
- **`StripPathPrefix`** (boolean): Whether to strip the path prefix before forwarding. Recommended `true` if `UsePathPrefix` is `true`.
- **`Target`** (string): Where to proxy requests. For SERVAPP routes, use `http://container_name:port`. For PROXY routes, use the full URL of the upstream.
- **`Mode`** (string): The route type. One of:
  - `"SERVAPP"` — Proxy to a Docker container managed by Cosmos (most common)
  - `"PROXY"` — Proxy to an external URL not managed by Cosmos
  - `"REDIRECT"` — Redirect requests to another URL
  - `"STATIC"` — Serve static files
  - `"SPA"` — Serve a single-page application
- **`AuthEnabled`** (boolean): Whether Cosmos authentication is required to access this route.
- **`Timeout`** (integer): Request timeout in milliseconds. Default `30000` (30s). Use higher values (e.g. `14400000` for 4 hours) for streaming/media services.
- **`ThrottlePerMinute`** (integer): Rate limit in requests per minute. `0` means no throttle.
- **`CORSOrigin`** (string): CORS origin header value. Empty string means no CORS header.
- **`SmartShield`** (object): Cosmos's anti-bot/anti-DDoS protection. Typically `{"Enabled": true}` to enable with defaults.
- **`BlockCommonBots`** (boolean): Block known bot user agents.
- **`AcceptInsecureHTTPSTarget`** (boolean): Allow proxying to HTTPS targets with invalid/self-signed certificates. Only use as a last resort.

## Top-Level Volumes

The top-level `"volumes"` array declares named volumes:

```json
"volumes": [
  {
    "name": "jellyfin-config",
    "driver": "local",
    "source": "/path/on/host",
    "target": "/config"
  }
]
```

Each volume needs a unique `"name"`. The `"driver"` is typically `"local"`. `"source"` and `"target"` map the host path to the container path.

Note: In practice, most cosmos-compose files use bind mounts directly on the service rather than declaring top-level volumes.

## Top-Level Networks

The top-level `"networks"` map declares custom networks:

```json
"networks": {
  "my-network": {
    "driver": "bridge"
  }
}
```

Network objects support: `"name"`, `"driver"` (usually `"bridge"`), `"attachable"`, `"internal"`, `"enable_ipv6"`, and `"ipam"` (with `"driver"` and `"config"` containing `"subnet"` entries).

In most cases, you do not need to declare networks explicitly. Using `"links"` between services will cause Cosmos to automatically create and manage an isolated network for the linked containers, which is the recommended approach.

## Best Practices

1. **Use `links` for inter-service communication.** Cosmos creates an isolated network automatically - more secure than the default bridge network.
2. **Use SERVAPP mode for Cosmos-managed containers.** `"Mode": "SERVAPP"`, target by container name: `"Target": "http://container_name:port"`.
3. **Enable SmartShield on all public routes.** Anti-bot/anti-DDoS with sensible defaults. Rarely a reason to disable.
4. **Set appropriate timeouts.** Default 30s is too short for media streaming (Jellyfin, Plex, Navidrome), file transfer (Nextcloud), or WebSocket apps. 14400000ms (4h) is common for streaming.
5. **Don't expose ports unnecessarily.** If a service is only accessed through Cosmos's reverse proxy, skip `"ports"` - the container is reachable by name on Cosmos's internal network. Expose only for direct host access (DNS on 53, VPN UDP port).
6. **Use `"restart": "unless-stopped"` or `"always"`.** Services come back after reboot.
7. **Bind mounts with explicit host paths for persistent data.** Simplifies backups and keeps data visible on the host. `"type": "bind"`.
8. **Set `AuthEnabled` thoughtfully.** Enable for admin panels and private services; disable for self-authenticating services (Jellyfin, Nextcloud) or public ones.
9. **Environment variables for config.** List as `"KEY=value"` strings in `"environment"`.
10. **Container names unique and descriptive.** Used in route targets and `links` - keep clear and short, no special characters.
11. **Pin image versions.** Specific tags (`jellyfin/jellyfin:10.10.6`), not `latest`/`stable`. Mutable tags can pull breaking changes or, in a supply-chain attack, malicious code. For maximum security use SHA256 digests (`image@sha256:abc123...`).
12. **Read-only root filesystem where possible.** `"read_only": true` plus writable volume mounts only for directories the app needs to write. Prevents attackers writing backdoor binaries or modifying application code. Add `tmpfs` mounts for `/tmp` and `/var/run` if needed.
13. **Log rotation.** Docker's default `json-file` driver has no size limit - containers can fill the host disk and crash all services. Add `"logging": {"driver": "json-file", "options": {"max-size": "10m", "max-file": "3"}}`.

## Complete Example: Jellyfin with Hardware Acceleration

```json
{
  "services": {
    "jellyfin": {
      "image": "jellyfin/jellyfin:10.10.6",
      "container_name": "jellyfin",
      "restart": "unless-stopped",
      "environment": [
        "JELLYFIN_PublishedServerUrl=https://jellyfin.yourdomain.com"
      ],
      "volumes": [
        {
          "source": "/opt/cosmos/servapps/jellyfin/config",
          "target": "/config",
          "type": "bind"
        },
        {
          "source": "/opt/cosmos/servapps/jellyfin/cache",
          "target": "/cache",
          "type": "bind"
        },
        {
          "source": "/mnt/media",
          "target": "/media",
          "type": "bind"
        }
      ],
      "devices": [
        "/dev/dri:/dev/dri"
      ],
      "routes": [
        {
          "Name": "jellyfin-web",
          "Description": "Jellyfin Media Server",
          "UseHost": true,
          "Host": "jellyfin.yourdomain.com",
          "UsePathPrefix": false,
          "PathPrefix": "",
          "Timeout": 14400000,
          "ThrottlePerMinute": 0,
          "CORSOrigin": "",
          "StripPathPrefix": false,
          "AuthEnabled": false,
          "Target": "http://jellyfin:8096",
          "SmartShield": {
            "Enabled": true
          },
          "Mode": "SERVAPP",
          "BlockCommonBots": false,
          "AcceptInsecureHTTPSTarget": false
        }
      ]
    }
  }
}
```

## Complete Example: App with Database (Linked Services)

```json
{
  "services": {
    "bookstack": {
      "image": "lscr.io/linuxserver/bookstack:24.12.1",
      "container_name": "bookstack",
      "restart": "unless-stopped",
      "environment": [
        "PUID=1000",
        "PGID=1000",
        "TZ=Australia/Sydney",
        "APP_URL=https://docs.yourdomain.com",
        "DB_HOST=bookstack-db",
        "DB_PORT=3306",
        "DB_USER=bookstack",
        "DB_PASS=changeme",
        "DB_DATABASE=bookstackapp"
      ],
      "volumes": [
        {
          "source": "/opt/cosmos/servapps/bookstack/config",
          "target": "/config",
          "type": "bind"
        }
      ],
      "depends_on": [
        "bookstack-db"
      ],
      "links": [
        "bookstack-db"
      ],
      "routes": [
        {
          "Name": "bookstack-web",
          "Description": "BookStack Documentation Wiki",
          "UseHost": true,
          "Host": "docs.yourdomain.com",
          "UsePathPrefix": false,
          "PathPrefix": "",
          "Timeout": 30000,
          "ThrottlePerMinute": 0,
          "CORSOrigin": "",
          "StripPathPrefix": false,
          "AuthEnabled": false,
          "Target": "http://bookstack:6875",
          "SmartShield": {
            "Enabled": true
          },
          "Mode": "SERVAPP",
          "BlockCommonBots": false,
          "AcceptInsecureHTTPSTarget": false
        }
      ]
    },
    "bookstack-db": {
      "image": "lscr.io/linuxserver/mariadb:11.6.2",
      "container_name": "bookstack-db",
      "restart": "unless-stopped",
      "environment": [
        "PUID=1000",
        "PGID=1000",
        "TZ=Australia/Sydney",
        "MYSQL_ROOT_PASSWORD=changeme",
        "MYSQL_DATABASE=bookstackapp",
        "MYSQL_USER=bookstack",
        "MYSQL_PASSWORD=changeme"
      ],
      "volumes": [
        {
          "source": "/opt/cosmos/servapps/bookstack/db",
          "target": "/config",
          "type": "bind"
        }
      ]
    }
  }
}
```

## Converting Docker Compose to Cosmos-Compose

1. **YAML → JSON.** Service fields are largely the same.
2. **Volume syntax.** Short syntax (`/host:/container`) becomes `{"source": "/host", "target": "/container", "type": "bind"}`.
3. **Add `routes`** for any web-facing service - object with hostname and target.
4. **`depends_on`** becomes a simple array of container-name strings (no conditions).
5. **`links` over `networks`.** Replace `networks` declarations with `links` where possible - Cosmos handles networking automatically and more securely.
6. **Ports → routes** where the port was only exposed for HTTP. Keep `ports` only for non-HTTP protocols or direct host access.
7. **No `env_file`.** Inline all env vars into `"environment"`.
8. **No `build`.** Image must be pre-built and on a registry.

## Output Conventions

- Valid, pretty-printed JSON with 2-space indentation.
- Placeholder hostnames like `"app.yourdomain.com"` - tell the user to replace.
- Bind-mount paths under `/opt/cosmos/servapps/<app-name>/`.
- Route `Description` fields as inline comments identifying routes in the Cosmos UI.
- Flag passwords/secrets with `"changeme"` placeholders and remind the user.
- Use any domain, timezone, or data paths the user mentions.
