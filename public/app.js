const statusEl = document.getElementById('window-status');
const statusIcon = document.getElementById('status-icon');
const statusText = document.getElementById('status-text');
const countdownEl = document.getElementById('countdown');
const formSection = document.getElementById('submission-form-section');
const form = document.getElementById('submission-form');
const submitBtn = document.getElementById('submit-btn');
const formMessage = document.getElementById('form-message');
const submissionsList = document.getElementById('submissions-list');

let windowData = null;

function formatTimeRemaining(ms) {
  if (ms <= 0) return 'now';
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}d ${hours % 24}h ${minutes % 60}m`;
  if (hours > 0) return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
  return `${seconds}s`;
}

function formatDate(iso) {
  return new Date(iso).toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
}

function updateWindowUI() {
  if (!windowData) return;

  const now = new Date();
  const opensAt = new Date(windowData.opensAt);
  const closesAt = new Date(windowData.closesAt);

  statusEl.className = 'window-status ' + windowData.status;

  if (windowData.status === 'open') {
    statusIcon.textContent = '\u2705';
    statusText.textContent = 'Submissions are OPEN';
    const remaining = closesAt - now;
    countdownEl.textContent = `Closes in ${formatTimeRemaining(remaining)} (${formatDate(windowData.closesAt)})`;
    submitBtn.disabled = false;
  } else if (windowData.status === 'not_yet_open') {
    statusIcon.textContent = '\u23F3';
    statusText.textContent = 'Submissions open soon';
    const remaining = opensAt - now;
    countdownEl.textContent = `Opens in ${formatTimeRemaining(remaining)} (${formatDate(windowData.opensAt)})`;
    submitBtn.disabled = true;
  } else {
    statusIcon.textContent = '\uD83D\uDD12';
    statusText.textContent = 'Submissions are CLOSED';
    countdownEl.textContent = `Closed on ${formatDate(windowData.closesAt)}`;
    submitBtn.disabled = true;
  }
}

async function fetchWindowStatus() {
  try {
    const res = await fetch('/api/window');
    windowData = await res.json();
    updateWindowUI();
  } catch (err) {
    statusText.textContent = 'Unable to check submission window status';
    countdownEl.textContent = '';
  }
}

async function fetchSubmissions() {
  try {
    const res = await fetch('/api/submissions');
    const submissions = await res.json();
    renderSubmissions(submissions);
  } catch (err) {
    submissionsList.innerHTML = '<p class="empty-state">Failed to load submissions.</p>';
  }
}

function renderSubmissions(submissions) {
  if (submissions.length === 0) {
    submissionsList.innerHTML = '<p class="empty-state">No submissions yet. Be the first to submit!</p>';
    return;
  }

  submissionsList.innerHTML = submissions
    .sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt))
    .map((s) => {
      const membersStr = s.members && s.members.length ? s.members.join(', ') : 'Not specified';
      const repoLink = s.repoUrl
        ? `<a href="${escapeHtml(s.repoUrl)}" target="_blank" rel="noopener">Repository</a>`
        : '';
      return `
        <div class="submission-item">
          <h3>${escapeHtml(s.projectName)}</h3>
          <p class="team">by ${escapeHtml(s.teamName)}</p>
          <p class="desc">${escapeHtml(s.description)}</p>
          <div class="meta">
            <span>Members: ${escapeHtml(membersStr)}</span>
            ${repoLink}
            <span>Submitted: ${formatDate(s.submittedAt)}</span>
          </div>
        </div>
      `;
    })
    .join('');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function showMessage(type, text) {
  formMessage.className = 'form-message ' + type;
  formMessage.textContent = text;
  if (type === 'success') {
    setTimeout(() => {
      formMessage.className = 'form-message';
    }, 5000);
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const data = {
    teamName: document.getElementById('teamName').value.trim(),
    projectName: document.getElementById('projectName').value.trim(),
    description: document.getElementById('description').value.trim(),
    repoUrl: document.getElementById('repoUrl').value.trim(),
    members: document
      .getElementById('members')
      .value.split(',')
      .map((m) => m.trim())
      .filter(Boolean),
  };

  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';

  try {
    const res = await fetch('/api/submissions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await res.json();

    if (!res.ok) {
      showMessage('error', result.error || 'Submission failed');
      return;
    }

    showMessage('success', 'Project submitted successfully!');
    form.reset();
    fetchSubmissions();
  } catch (err) {
    showMessage('error', 'Network error. Please try again.');
  } finally {
    submitBtn.textContent = 'Submit Project';
    if (windowData && windowData.status === 'open') {
      submitBtn.disabled = false;
    }
  }
});

// Initial load
fetchWindowStatus();
fetchSubmissions();

// Refresh countdown every second
setInterval(updateWindowUI, 1000);

// Refresh window status every 30 seconds
setInterval(fetchWindowStatus, 30000);
