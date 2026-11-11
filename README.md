# h6082

A compact start page generated from markdown, with a dark Obsidian-like theme. Runs in Docker.

```bash
cp .env.example .env    # UID/GID, port, editor password
docker compose up -d --build
```

→ http://127.0.0.1:8088

Repository: <https://code.nolog.cz/hindrich/h6082> (mirror <https://github.com/manihindrich/h6082>).

Content lives in `content/`. Documentation and the editor are built into the page, in the **h6082** tab at the top right. The UI and documentation are available in English (default) and Czech.
