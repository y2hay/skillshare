---
name: create-dns-records
description: Automatically create Cloudflare DNS records for new Traefik Host() labels found in Docker Compose files
version: 1
triggers: ["Traefik Host()", "DNS records", "Cloudflare DNS", "create DNS"]
---

<skill>
<objective>
Scan Docker Compose files for Traefik labels with `Host()` directives and create corresponding Cloudflare DNS A records pointing to the current WAN IP.
</objective>

<quick_start>
Scan for Host labels in /opt/stacks/, compare with existing Cloudflare DNS records, and create missing entries to sync DNS with Traefik configurations.
</quick_start>

<success_criteria>
- All Traefik Host labels in compose files have corresponding DNS A records
- DNS records point to the correct current WAN IP
- Summary report correctly identifies created, skipped, and failed records
</success_criteria>

<examples>
Run this skill:
- After adding new Traefik labels to compose files
- To sync all missing DNS records
- To audit current DNS vs. Traefik configuration
</examples>

<process>
1. **Scan Compose Files**
   - Search for all `compose.yaml` and `docker-compose.yml` files on Dockge LXC (10.10.0.155)
   - Extract `traefik.http.routers.*.rule=Host(...)` labels
   - Parse out domain names

2. **Check Existing DNS**
   - Query current DNS records for y2hay.com zone
   - Identify missing records

3. **Create Missing Records**
   - Use Cloudflare API to create A records
   - Point to WAN IP from `.env` file
   - Use Zone ID and API token from `.env` file

4. **Report Results**
   - List created records
   - List already-existing records
   - Show any errors
</process>

<setup>
**Credentials (create `.env` in this directory):**
```
CLOUDFLARE_API_TOKEN=your_api_token_here
CLOUDFLARE_ZONE_ID=your_zone_id_here
WAN_IP=your_current_wan_ip
```

**Compose File Locations:**
- `/opt/stacks/*/compose.yaml` on 10.10.0.155
- `/opt/stacks/*/docker-compose.yml` on 10.10.0.155
</setup>

<implementation>
Execute the following steps:

<step_1_extract_all_traefik_hostnames>
```bash
ssh root@10.10.0.155 'grep -rh "traefik.http.routers.*rule=Host" /opt/stacks/*/compose.yaml /opt/stacks/*/docker-compose.yml 2>/dev/null | grep -oP "Host\(\K[^\)]+(?=\))" | tr -d "`"" | sort -u'
```
</step_1_extract_all_traefik_hostnames>

<step_2_get_existing_cloudflare_dns_records>
```bash
source .env
curl -sX GET "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?type=A" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  | jq -r '.result[] | select(.name | endswith("y2hay.com")) | .name'
```
</step_2_get_existing_cloudflare_dns_records>

<step_3_compare_and_create_missing_records>
For each hostname found in Traefik labels that doesn't exist in DNS:

```bash
# Load credentials
source .env

# Extract subdomain (e.g., "newmedia" from "newmedia.y2hay.com")
subdomain=$(echo "$hostname" | sed 's/\.y2hay\.com$//')

# Create DNS record
curl -sX POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"A\",\"name\":\"$subdomain\",\"content\":\"$WAN_IP\",\"ttl\":1,\"proxied\":false}" \
  | jq -r '.success, .result.name // .errors[0].message'
```
</step_3_compare_and_create_missing_records>

<step_4_report_results>
Present a summary table:
- ✅ Created: [list of newly created records]
- ⏭️ Skipped: [list of already-existing records]
- ❌ Failed: [list of failed creations with error messages]
</step_4_report_results>
</implementation>

<error_handling>
- If Cloudflare API fails, show the error message
- If SSH to Dockge fails, report connection issue
- If no Traefik labels found, inform user
- Validate that all hostnames are *.y2hay.com domains
- If `.env` file is missing, instruct user to create it from the setup section
</error_handling>

<security_notes>
- API token has full DNS access to y2hay.com zone — store securely in `.env`, never commit
- Records created with `proxied=false` (DNS-only, no Cloudflare proxy)
- TTL set to 1 (automatic, managed by Cloudflare)
- `.env` is gitignored — add to `.gitignore` if not already present
</security_notes>

</skill>
