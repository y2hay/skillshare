---
name: create-dns-records
description: Automatically create Cloudflare DNS records for new Traefik Host() labels found in Docker Compose files
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
   - Point to WAN IP from ~/CREDENTIALS.md
   - Use Zone ID and API token from ~/CREDENTIALS.md

4. **Report Results**
   - List created records
   - List already-existing records
   - Show any errors
</process>

<setup>
**From ~/CREDENTIALS.md:**
- Cloudflare API Token: `3r7dm9opEud85MZDlKU3z-lLORho3-_658z1rwM9`
- Zone ID: `11a6a39c89af36908894f05260088da7`
- WAN IP: `73.159.93.55`

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
curl -sX GET 'https://api.cloudflare.com/client/v4/zones/11a6a39c89af36908894f05260088da7/dns_records?type=A' 
  -H 'Authorization: Bearer 3r7dm9opEud85MZDlKU3z-lLORho3-_658z1rwM9' 
  | jq -r '.result[] | select(.name | endswith("y2hay.com")) | .name'
```
</step_2_get_existing_cloudflare_dns_records>

<step_3_compare_and_create_missing_records>
For each hostname found in Traefik labels that doesn't exist in DNS:

```bash
# Extract subdomain (e.g., "newmedia" from "newmedia.y2hay.com")
subdomain=$(echo "$hostname" | sed 's/\.y2hay\.com$//')

# Create DNS record
curl -sX POST 'https://api.cloudflare.com/client/v4/zones/11a6a39c89af36908894f05260088da7/dns_records' 
  -H 'Authorization: Bearer 3r7dm9opEud85MZDlKU3z-lLORho3-_658z1rwM9' 
  -H 'Content-Type: application/json' 
  -d "{"type":"A","name":"$subdomain","content":"73.159.93.55","ttl":1,"proxied":false}" 
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
</error_handling>

<security_notes>
- API token has full DNS access to y2hay.com zone
- Records created with `proxied=false` (DNS-only, no Cloudflare proxy)
- TTL set to 1 (automatic, managed by Cloudflare)
</security_notes>

</skill>
