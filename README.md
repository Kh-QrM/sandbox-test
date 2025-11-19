#  Web Testing Sandbox

A fully isolated, Dockerized environment for safe web testing, scraping, and network traffic analysis.

This project launches a disposable Chrome browser inside a container, routes all traffic through a transparent proxy (Mitmproxy), and controls the session via Python—keeping your host machine safe from malware and trackers.

##  Features

* **Isolated Browser:** Runs Chrome in a Linux container (Selenium Grid).
* **Network Logging:** Captures full HTTP/HTTPS traffic flows via Mitmproxy.
* **Python Automation:** Control the browser programmatically.
* **Controlled DNS:** Enforces Cloudflare DNS (1.1.1.1) to bypass local filtering.
* **Auto-Reset:** Containers are ephemeral; shutting down wipes all cookies/cache.

##  Architecture

* **Chrome:** `selenium/standalone-chrome` (Port 7900 for viewing)
* **Proxy:** `mitmproxy/mitmproxy` (Port 8081 for logs)
* **Runner:** `python:3.9-slim` (Executes the control script)

##  Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

##  Quick Start

### 1. Start the Environment
Run the following command to download images and start the private network:
```bash
docker compose up -d