# AIhackathon

Submission window for the AI Hackathon. Teams can submit their projects within a configurable time window.

## Features

- Time-based submission window (configurable open/close times)
- Live countdown showing time remaining
- Submission form with team info, project details, and repo link
- REST API for managing submissions
- JSON file storage

## Quick Start

```bash
npm install
npm start
```

Open `http://localhost:3000` in your browser.

## Configuration

Edit `config.js` or set environment variables:

| Variable | Description | Default |
|---|---|---|
| `SUBMISSION_WINDOW_OPEN` | Window open time (ISO 8601) | `2026-02-07T00:00:00Z` |
| `SUBMISSION_WINDOW_CLOSE` | Window close time (ISO 8601) | `2026-02-14T23:59:59Z` |
| `PORT` | Server port | `3000` |

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/window` | Get submission window status |
| `GET` | `/api/submissions` | List all submissions |
| `POST` | `/api/submissions` | Create a submission |
| `PUT` | `/api/submissions/:id` | Update a submission |
| `DELETE` | `/api/submissions/:id` | Delete a submission |
