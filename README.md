# ooclsap-bot-repository

SAP Bot Repository for SAP Hackathon 2026.

## Hello-world proof of concept

This stateless Flask service returns `hello world` for every `POST /v2/chat` request. It does not call a model, query SAP systems, execute tools, or store conversation history. An optional `conversation_id` is returned unchanged; when absent, a new ID is generated. `GET /v2/health` returns `{"status":"healthy"}`.

Run locally from this repository's root with a Python virtual environment:

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install 'Flask>=3.1,<4'
& .\.venv\Scripts\python.exe -m unittest discover -s tests -v
& .\.venv\Scripts\python.exe -m flask --app app run --port 5000
```

In another PowerShell terminal, send any message:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/v2/chat -Method Post -ContentType application/json -Body '{"message":"Any question"}'
```

The response contains `"content": "hello world"`. The development server is for local testing only.

## Build without local Podman

The manually triggered GitHub Actions workflow in `.github/workflows/build-image.yml` uses Podman on a GitHub-hosted Ubuntu runner. Once these files are committed and pushed to GitHub, use the repository's **Actions** tab to run **Build hello-world bot image**. The job builds the Containerfile, calls the running container, and pushes `ghcr.io/doletro/ooclsap-bot-repository:poc-<commit-sha>` to GitHub Container Registry. The workflow requests only `contents: read` and `packages: write` for its `GITHUB_TOKEN`.

The GHCR package is private by default. To deploy it to SAP AI Core, register separate GHCR read credentials as an AI Core registry secret and reference that secret and the exact pushed image in a ServingTemplate. This registry credential is **not** the token used to register the private Git repository with AI Core. Configure one Joule Action to call the deployed `/v2/chat` endpoint and display the response's `content` field. Confirm the externally exposed inference path before configuring the Action.
