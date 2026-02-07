const express = require('express');
const fs = require('fs');
const path = require('path');
const config = require('./config');

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Ensure data directory exists
if (!fs.existsSync(config.dataDir)) {
  fs.mkdirSync(config.dataDir, { recursive: true });
}

// Initialize submissions file if it doesn't exist
if (!fs.existsSync(config.submissionsFile)) {
  fs.writeFileSync(config.submissionsFile, JSON.stringify([], null, 2));
}

function loadSubmissions() {
  const raw = fs.readFileSync(config.submissionsFile, 'utf-8');
  return JSON.parse(raw);
}

function saveSubmissions(submissions) {
  fs.writeFileSync(config.submissionsFile, JSON.stringify(submissions, null, 2));
}

function getWindowStatus() {
  const now = new Date();
  const open = new Date(config.windowOpen);
  const close = new Date(config.windowClose);

  if (now < open) {
    return { status: 'not_yet_open', opensAt: config.windowOpen, closesAt: config.windowClose };
  }
  if (now > close) {
    return { status: 'closed', opensAt: config.windowOpen, closesAt: config.windowClose };
  }
  return { status: 'open', opensAt: config.windowOpen, closesAt: config.windowClose };
}

// GET /api/window - Get submission window status
app.get('/api/window', (req, res) => {
  res.json(getWindowStatus());
});

// GET /api/submissions - List all submissions
app.get('/api/submissions', (req, res) => {
  const submissions = loadSubmissions();
  res.json(submissions);
});

// POST /api/submissions - Create a new submission
app.post('/api/submissions', (req, res) => {
  const window = getWindowStatus();
  if (window.status !== 'open') {
    return res.status(403).json({
      error: 'Submission window is not open',
      windowStatus: window.status,
      opensAt: window.opensAt,
      closesAt: window.closesAt,
    });
  }

  const { teamName, projectName, description, repoUrl, members } = req.body;

  // Validate required fields
  if (!teamName || !projectName || !description) {
    return res.status(400).json({
      error: 'Missing required fields: teamName, projectName, and description are required',
    });
  }

  const submissions = loadSubmissions();

  // Check for duplicate team name
  if (submissions.some((s) => s.teamName.toLowerCase() === teamName.toLowerCase())) {
    return res.status(409).json({
      error: `A submission from team "${teamName}" already exists. Use PUT to update.`,
    });
  }

  const submission = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7),
    teamName,
    projectName,
    description,
    repoUrl: repoUrl || '',
    members: members || [],
    submittedAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  submissions.push(submission);
  saveSubmissions(submissions);

  res.status(201).json(submission);
});

// PUT /api/submissions/:id - Update an existing submission
app.put('/api/submissions/:id', (req, res) => {
  const window = getWindowStatus();
  if (window.status !== 'open') {
    return res.status(403).json({
      error: 'Submission window is not open',
      windowStatus: window.status,
    });
  }

  const submissions = loadSubmissions();
  const index = submissions.findIndex((s) => s.id === req.params.id);

  if (index === -1) {
    return res.status(404).json({ error: 'Submission not found' });
  }

  const { teamName, projectName, description, repoUrl, members } = req.body;
  const existing = submissions[index];

  submissions[index] = {
    ...existing,
    teamName: teamName || existing.teamName,
    projectName: projectName || existing.projectName,
    description: description || existing.description,
    repoUrl: repoUrl !== undefined ? repoUrl : existing.repoUrl,
    members: members || existing.members,
    updatedAt: new Date().toISOString(),
  };

  saveSubmissions(submissions);
  res.json(submissions[index]);
});

// DELETE /api/submissions/:id - Delete a submission
app.delete('/api/submissions/:id', (req, res) => {
  const window = getWindowStatus();
  if (window.status !== 'open') {
    return res.status(403).json({
      error: 'Submission window is not open',
      windowStatus: window.status,
    });
  }

  const submissions = loadSubmissions();
  const index = submissions.findIndex((s) => s.id === req.params.id);

  if (index === -1) {
    return res.status(404).json({ error: 'Submission not found' });
  }

  const removed = submissions.splice(index, 1)[0];
  saveSubmissions(submissions);
  res.json({ message: 'Submission deleted', submission: removed });
});

app.listen(config.port, () => {
  const window = getWindowStatus();
  console.log(`AI Hackathon Submission Server running on port ${config.port}`);
  console.log(`Submission window: ${window.status}`);
  console.log(`  Opens:  ${config.windowOpen}`);
  console.log(`  Closes: ${config.windowClose}`);
});
