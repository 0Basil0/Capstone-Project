const csrfToken = '{{ csrf_token }}';
let currentChatId = null;

async function loadConversations() {
  // conversation list already rendered server-side; just attach handlers
  document.querySelectorAll('.chat-item').forEach(el => {
    el.addEventListener('click', async (e) => {
      e.preventDefault();
      const sid = el.dataset.sessionId;
      await selectChat(sid);
    });
  });
}

async function selectChat(sessionId) {
  currentChatId = sessionId;
  // fetch chat details for session
  const res = await fetch(`{% url 'chat_get' '00000000-0000-0000-0000-000000000000' %}`.replace('00000000-0000-0000-0000-000000000000', sessionId));
  const data = await res.json();
  const messages = document.getElementById('messages');
  messages.innerHTML = '';
  // server returns the full message list for the session
  for (const m of data.messages) {
    messages.innerHTML += `<div><strong>You:</strong> ${escapeHtml(m.user_message)}</div>`;
    messages.innerHTML += `<div class="text-success"><strong>AI:</strong> ${escapeHtml(m.bot_response)}</div>`;
  }
  scrollChatToBottom();
}

async function sendMessage() {
  const input = document.getElementById('userMessage');
  const message = input.value.trim();
  if (!message) return;

  // show optimistic user message
  const messages = document.getElementById('messages');
  messages.innerHTML += `<div><strong>You:</strong> ${escapeHtml(message)}</div>`;
  scrollChatToBottom();

  const res = await fetch("{% url 'chatbot_api' %}", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ message, session_id: currentChatId })
  });
  const data = await res.json();
  if (data.error) {
    messages.innerHTML += `<div class="text-danger"><strong>Error:</strong> ${escapeHtml(data.error)}</div>`;
  } else {
    messages.innerHTML += `<div class="text-success"><strong>AI:</strong> ${escapeHtml(data.reply)}</div>`;
    // set or update the active session id
    if (data.session_id) {
      currentChatId = data.session_id;
      addConversationToSidebar(data.session_id, message, data.reply);
    }
  }
  input.value = '';
  scrollChatToBottom();
}

function addConversationToSidebar(id, userMsg, botResp) {
  const container = document.getElementById('conversations');
  const a = document.createElement('a');
  a.className = 'list-group-item list-group-item-action chat-item active';
  a.dataset.sessionId = id;
  a.href = '#';
  a.innerHTML = `<div class="d-flex w-100 justify-content-between"><h6 class="mb-1 small text-truncate">${escapeHtml(userMsg)}</h6><small class="text-muted">Now</small></div><p class="mb-1 small text-muted">${escapeHtml(botResp)}</p>`;
  a.addEventListener('click', async (e) => { e.preventDefault(); await selectChat(id); });
  // prepend
  container.prepend(a);
  // set as current
  selectChat(id);
}

async function deleteCurrentChat() {
  if (!currentChatId) return;
  if (!confirm('Delete this conversation?')) return;
  const res = await fetch(`{% url 'chat_delete' '00000000-0000-0000-0000-000000000000' %}`.replace('00000000-0000-0000-0000-000000000000', `${currentChatId}`), {
    method: 'POST', headers: {'X-CSRFToken': csrfToken}
  });
  const data = await res.json();
  if (data.deleted) {
    // remove from sidebar
    const el = document.querySelector(`.chat-item[data-session-id="${currentChatId}"]`);
    if (el) el.remove();
    currentChatId = null;
    document.getElementById('messages').innerHTML = '';
  }
}

function newChat() {
  currentChatId = null;
  document.getElementById('messages').innerHTML = '';
}

function scrollChatToBottom() {
  const pane = document.getElementById('chatPane');
  pane.scrollTop = pane.scrollHeight;
}

function escapeHtml(text) {
  var map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(text).replace(/[&<>\"']/g, function(m) { return map[m]; });
}

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('userMessage').addEventListener('keydown', function(e){ if(e.key === 'Enter') { sendMessage(); }});
document.getElementById('deleteBtn').addEventListener('click', deleteCurrentChat);
document.getElementById('newChatBtn').addEventListener('click', newChat);

loadConversations();