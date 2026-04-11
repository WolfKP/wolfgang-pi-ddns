# wolfgang-pi-ddns

A Dynamic DNS (DDNS) program that runs on my Raspberry Pi (wolfgang-pi). It checks wolfgang-pi's public IP every 5 minutes and updates a Cloudflare A record on change.

## How it works

1. Fetches the current public IP from [ipify.org](https://api.ipify.org)
2. Fetches the current IP stored in Cloudflare's DNS A record
3. If they match, does nothing
4. If they differ, updates the Cloudflare record

## Requirements

- Python 3.11+
- Cloudflare account with an A record to update
- Cloudflare API token scoped to zone with DNS edit permissions

## Setup

Clone the repo and create a virtual environment with:
```bash
git clone git@github.com:wolfgangkp/wolfgang-pi-ddns.git
cd wolfgang-pi-ddns
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then create an `.env` file in the project root that contains:
```
CF_API_TOKEN=<Cloudflare API token>
RECORD_NAME=<your.domain.something>
ZONE_ID=<Cloudflare zone id>
```

## Cron job

To have the script run automatically every `x` minutes via cron run
```bash
crontab -e
```
and add
```
*/x * * * * /path/to/wolfgang-pi-ddns/.venv/bin/python3 /path/to/wolfgang-pi-ddns/main.py >> /path/to/wolfgang-pi-ddns/log 2>&1
```
to the crontab file.

## Logging

Logs are written to `log` in the project directory.
