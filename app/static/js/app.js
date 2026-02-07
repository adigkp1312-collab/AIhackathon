const input = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const voiceBtn = document.getElementById('voice-btn');
const messagesEl = document.getElementById('messages');
const welcome = document.getElementById('welcome');
const langSelect = document.getElementById('language-select');

let conversationHistory = [];
let isRecording = false;
let mediaRecorder = null;

// Escape HTML to prevent XSS
function esc(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

function scrollToBottom() {
  const container = document.getElementById('chat-container');
  container.scrollTop = container.scrollHeight;
}

function hideWelcome() {
  if (welcome) welcome.style.display = 'none';
}

function addMessage(role, html) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = html;
  messagesEl.appendChild(div);
  scrollToBottom();
  return div;
}

function renderCoursePlan(plan, ytResults) {
  let html = '<div class="course-plan">';

  // Header
  html += `<div class="plan-header">
    <h3>${esc(plan.title)}</h3>
    <p>${esc(plan.description)}</p>
    <div class="plan-meta">
      <span>${esc(plan.estimated_duration)}</span>
      <span>${esc(plan.skill_level)}</span>
      <span>${plan.modules ? plan.modules.length : 0} modules</span>
    </div>
  </div>`;

  // Modules
  if (plan.modules) {
    plan.modules.forEach(mod => {
      html += `<div class="module">
        <h4>Module ${mod.module_number}: ${esc(mod.title)}</h4>
        <p class="mod-desc">${esc(mod.description)} (${esc(mod.duration)})</p>`;

      if (mod.topics) {
        html += '<div class="topics">';
        mod.topics.forEach(t => { html += `<span>${esc(t)}</span>`; });
        html += '</div>';
      }

      if (mod.resources) {
        mod.resources.forEach(res => {
          html += `<div class="resource">
            <span class="res-title">${esc(res.title)}</span>
            <span class="res-type">${esc(res.type.replace('_', ' '))}</span>
            <p class="res-desc">${esc(res.description)}</p>
            <span class="res-lang">${esc(res.language)}</span>
          </div>`;
        });
      }
      html += '</div>';
    });
  }

  // Tips
  if (plan.tips && plan.tips.length) {
    html += '<div class="tips"><h4>Tips for Success</h4><ul>';
    plan.tips.forEach(tip => { html += `<li>${esc(tip)}</li>`; });
    html += '</ul></div>';
  }

  // YouTube results
  if (ytResults && ytResults.length) {
    html += '<div class="yt-results"><h4>Related Free Content on YouTube</h4>';
    ytResults.forEach(yt => {
      html += `<a class="yt-item" href="${esc(yt.url)}" target="_blank" rel="noopener">
        <div class="yt-title">${esc(yt.title)}</div>
        <div class="yt-channel">${esc(yt.channel)}</div>
      </a>`;
    });
    html += '</div>';
  }

  html += '</div>';
  return html;
}

async function sendMessage(text) {
  if (!text.trim()) return;

  hideWelcome();
  addMessage('user', esc(text));

  conversationHistory.push({ role: 'user', content: text });

  const loadingMsg = addMessage('assistant loading', 'Finding the best free courses for you...');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: conversationHistory.slice(-10),
      }),
    });

    const data = await res.json();
    loadingMsg.remove();

    if (data.plan.type === 'conversation') {
      addMessage('assistant', `<div class="conversation-msg">${esc(data.plan.message)}</div>`);
      conversationHistory.push({ role: 'assistant', content: data.plan.message });
    } else {
      const html = renderCoursePlan(data.plan, data.youtube_results);
      addMessage('assistant', html);
      conversationHistory.push({ role: 'assistant', content: JSON.stringify(data.plan) });
    }

    // TTS for the response (if voice interaction)
    if (data.plan.type === 'conversation' && data.plan.message) {
      tryTTS(data.plan.message);
    }
  } catch (err) {
    loadingMsg.remove();
    addMessage('assistant', `<div class="conversation-msg">Sorry, something went wrong. Please try again.</div>`);
  }
}

async function tryTTS(text) {
  try {
    const lang = langSelect.value;
    const res = await fetch('/api/voice/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, language_code: lang }),
    });
    const data = await res.json();
    if (data.audio_base64 && !data.demo) {
      const audio = new Audio(`data:audio/mp3;base64,${data.audio_base64}`);
      audio.play();
    }
  } catch (e) {
    // TTS is optional, fail silently
  }
}

// Voice recording
async function toggleRecording() {
  if (isRecording) {
    stopRecording();
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

    mediaRecorder.onstop = async () => {
      stream.getTracks().forEach(t => t.stop());
      const blob = new Blob(chunks, { type: 'audio/webm' });

      // Convert to base64
      const reader = new FileReader();
      reader.onload = async () => {
        const base64 = reader.result.split(',')[1];
        const lang = langSelect.value;

        // STT
        try {
          const res = await fetch('/api/voice/stt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio_base64: base64, language_code: lang }),
          });
          const data = await res.json();
          if (data.transcript) {
            input.value = data.transcript;
            sendMessage(data.transcript);
            input.value = '';
          }
        } catch (e) {
          addMessage('assistant', '<div class="conversation-msg">Could not process voice. Please type your query instead.</div>');
        }
      };
      reader.readAsDataURL(blob);
    };

    mediaRecorder.start();
    isRecording = true;
    voiceBtn.classList.add('recording');
  } catch (e) {
    addMessage('assistant', '<div class="conversation-msg">Microphone access denied. Please allow microphone access or type your query.</div>');
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
  }
  isRecording = false;
  voiceBtn.classList.remove('recording');
}

// Event listeners
sendBtn.addEventListener('click', () => {
  sendMessage(input.value);
  input.value = '';
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage(input.value);
    input.value = '';
  }
});

voiceBtn.addEventListener('click', toggleRecording);

// Quick topic chips
document.querySelectorAll('.topic-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const query = chip.dataset.query;
    sendMessage(query);
  });
});
