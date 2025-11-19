# Project Architecture Report: Web Testing Sandbox

**Project:** Dockerized Web Testing Sandbox
**Author:** Kh-QrM
**Description:** A deep dive into the technical architecture, component roles, and data flow of the isolated web testing environment.

---

## 1. The Blueprint: `docker-compose.yml`
This file acts as the **Architect**. It tells Docker exactly how to build the lab, defining three distinct "rooms" (containers) and a private hallway (network) connecting them.



[Image of Docker container architecture diagram]


### The Network (`sandbox_net`)
* **Job:** A private virtual cable.
* **Function:** It ensures the containers can talk to each other while remaining strictly separated from the host Windows file system.

### Service 1: `chrome` (The Test Subject)
* **Job:** The actual web browser running inside a Linux container.
* **Security:** If a website downloads a virus, it is contained here—in a disposable environment that can be deleted instantly.
* **Key Setting:** `dns: 1.1.1.1` — Forces the use of Cloudflare's DNS instead of the home router for enhanced privacy and anti-tracking.

### Service 2: `mitmproxy` (The Security Camera)
* **Job:** A reverse proxy sitting between Chrome and the Internet.
* **Function:** Every piece of data (images, text, scripts) must pass through here, allowing for full packet logging and inspection.
* **Key Setting:** `command: ... --set web_password=1234` — Sets a fixed entry password for easy access to the log interface.

### Service 3: `runner` (The Robot Arm)
* **Job:** A lightweight Python container.
* **Function:** Since the host machine (Windows) may not have the correct Python environment, this container is built specifically to execute the control scripts that drive the Chrome browser.

---

## 2. The Brain: `main.py`
This file acts as the **Instruction Manual**. It tells the "Robot Arm" (`runner`) exactly how to manipulate the "Test Subject" (`chrome`).

* **`webdriver.Remote(...)`**: Connects the Python script to the Chrome container (Handshake).
* **`--proxy-server=mitmproxy:8080`**: **CRITICAL.** Configures Chrome to force all traffic through Mitmproxy. Without this, Chrome would bypass the logging system.
* **The Loop (`while True`)**: Enables interactive mode, keeping the session alive and waiting for user input (`google.com`, etc.) until the exit command is received.

---

## 3. The Ignore List: `.gitignore`
This file acts as the **Trash Filter**.

* **Job:** Prevents heavy or unnecessary files from being uploaded to GitHub.
* **Excluded Items:** Temporary traffic logs, Python cache files (`__pycache__`), and system thumbnails.
* **Why:** Ensures the professional portfolio remains clean, lightweight, and focused on source code.

---

## 4. Operational Commands

| Command | Job Description |
| :--- | :--- |
| `docker compose up -d` | **"Build the Lab"** - Downloads images and starts containers in the background. |
| `docker compose exec runner pip install selenium` | **"Equip the Robot"** - Installs necessary Python libraries inside the container. |
| `docker compose exec runner python main.py` | **"Start the Experiment"** - Executes the interactive control script. |
| `docker compose down` | **"Incinerate the Lab"** - Destroys containers and wipes all data/cookies permanently. |

---

## 5. The Flow of Data
A step-by-step breakdown of a web request (e.g., visiting `google.com`):

1.  **USER** types `google.com` in the terminal.
2.  **PYTHON (Runner)** receives the text and sends a navigation command to **CHROME**.
3.  **CHROME** attempts to request Google.
4.  **MITMPROXY** intercepts the request, logs it (visible on `localhost:8081`), and forwards it to the real Internet.
5.  **THE INTERNET** sends the website data back to **MITMPROXY**.
6.  **MITMPROXY** logs the response and forwards it to **CHROME**.
7.  **CHROME** renders and displays the page (visible on `localhost:7900`).