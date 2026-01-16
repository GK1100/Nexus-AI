// const BACKEND_URL = "http://127.0.0.1:8000"; // FOR LOCAL SETUP
// const BACKEND_URL = "http://localhost:8000"; // FOR DOCKER SETUP (browser access)

const BACKEND_URL = "https://nexus-ai-backend-34k9.onrender.com"; // FOR RENDER SETUP

// State
let SESSION_ID = null;
let uploadedFiles = [];

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadProgress = document.getElementById('uploadProgress');
const progressBar = document.getElementById('progressBar');
const uploadStatusText = document.getElementById('uploadStatusText');
const uploadingFileName = document.getElementById('uploadingFileName');
const filesList = document.getElementById('filesList');
const fileCount = document.getElementById('file-count');
const chatContainer = document.getElementById('chatContainer');
const userQuery = document.getElementById('userQuery');
const sendBtn = document.getElementById('sendBtn');
const connectionToast = document.getElementById('connection-toast');

/* =========================================
   INITIALIZATION & DRAG-N-DROP
   ========================================= */
document.addEventListener('DOMContentLoaded', () => {
    checkServerStatus();
    warmupModels(); // Pre-load models in background
    userQuery.focus();
});

// Warmup models in background (optional, improves first upload speed)
async function warmupModels() {
    try {
        console.log("[INFO] Warming up models in background...");
        await fetch(`${BACKEND_URL}/warmup`, { method: 'GET' });
        console.log("[INFO] Models warmed up successfully!");
    } catch (e) {
        console.log("[INFO] Model warmup skipped (server might be cold starting)");
    }
}

// Drag & Drop Events
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length) handleFileUpload(files[0]);
});

// Click to Upload
dropZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (fileInput.files.length) handleFileUpload(fileInput.files[0]);
});

// Auto-resize textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
    // Max height limitation handled effectively by max-height in CSS
}

// Enter key to send
userQuery.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        askQuestion();
    }
});

/* =========================================
   CORE FUNCTIONS
   ========================================= */

// Check Server Health
async function checkServerStatus(retries = 10, delay = 2000) {
    for (let i = 0; i < retries; i++) {
        try {
            const res = await fetch(`${BACKEND_URL}/health`);
            if (res.ok) {
                document.getElementById('serverDot').classList.add('online');
                document.getElementById('serverText').innerText = "Server Online";
                connectionToast.classList.add('hidden');
                return;
            }
        } catch (e) {
            // ignore and retry
        }

        await new Promise(resolve => setTimeout(resolve, delay));
    }

    document.getElementById('serverDot').classList.remove('online');
    document.getElementById('serverDot').classList.add('offline');
    document.getElementById('serverText').innerText = "Offline";
    connectionToast.classList.remove('hidden');
}


// Handle File Upload
async function handleFileUpload(file) {
    // Validation
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/png', 'image/jpeg', 'image/webp', 'text/plain'];
    if (!validTypes.includes(file.type)) {
        showToast("Unsupported file type. Please upload PDF, DOCX, TXT, or Image.", "error");
        return;
    }

    // UI Update
    dropZone.classList.add('hidden');
    uploadProgress.classList.remove('hidden');
    uploadingFileName.innerText = file.name;
    uploadStatusText.innerText = "Uploading & Indexing... (First upload may take 2-3 minutes)";
    progressBar.style.width = "30%";

    const formData = new FormData();
    formData.append("file", file);

    try {
        // Longer timeout for Render cold starts (models loading)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes
        
        const response = await fetch(`${BACKEND_URL}/ingest/file`, {
            method: "POST",
            body: formData,
            mode: 'cors',
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        progressBar.style.width = "80%";

        if (!response.ok) {
            const err = await response.text();
            let errorMsg = "Upload failed";
            try {
                errorMsg = JSON.parse(err).detail || errorMsg;
            } catch {
                errorMsg = err || errorMsg;
            }
            throw new Error(errorMsg);
        }

        const result = await response.json();

        // Critical: Set Session ID
        SESSION_ID = result.session_id;

        // UI Success
        progressBar.style.width = "100%";
        uploadStatusText.innerText = "Completed!";

        setTimeout(() => {
            uploadProgress.classList.add('hidden');
            dropZone.classList.remove('hidden');
            addFileToList(file.name, result.modality);

            // Add system message
            addMessage('bot', `I've successfully processed **${file.name}**. You can now ask questions about it!`);
        }, 1000);

    } catch (error) {
        console.error("Upload error:", error);
        uploadStatusText.innerText = "Failed";
        uploadStatusText.style.color = "var(--error)";
        
        // Better error message for network issues
        let errorMessage = error.message;
        if (error.name === 'AbortError') {
            errorMessage = "Request timed out. The server might be loading models (cold start). Please try again in a minute.";
        } else if (error.message.includes('fetch') || error.name === 'TypeError') {
            errorMessage = "Cannot connect to backend. Please ensure the backend is running at " + BACKEND_URL;
        }
        
        showToast(errorMessage, "error");

        setTimeout(() => {
            uploadProgress.classList.add('hidden');
            dropZone.classList.remove('hidden');
            uploadStatusText.style.color = ""; // Reset color
        }, 3000);
    }
}

// Add File to Sidebar List
function addFileToList(name, type) {
    uploadedFiles.push({ name, type });
    fileCount.innerText = `${uploadedFiles.length} file${uploadedFiles.length !== 1 ? 's' : ''}`;

    const icon = type === 'image' ? 'ri-image-line' : 'ri-file-text-line';

    const div = document.createElement('div');
    div.className = 'uploaded-item active';
    div.innerHTML = `
        <i class="${icon}"></i>
        <span>${name}</span>
        <i class="ri-check-line" style="color: var(--success); font-size: 14px;"></i>
    `;
    filesList.appendChild(div);
}

// Ask Question
async function askQuestion() {
    const query = userQuery.value.trim();
    if (!query) return;

    if (!SESSION_ID) {
        showToast("Please upload a document to start the conversation.", "warning");
        addMessage('bot', "⚠️ Please upload a document or image first so I have something to talk about!");
        return;
    }

    // UI Updates
    addMessage('user', query);
    userQuery.value = '';
    userQuery.style.height = 'auto'; // Reset height
    sendBtn.disabled = true;

    // Show Typing Indicator
    const typingId = showTypingIndicator();

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minutes for queries
        
        const response = await fetch(`${BACKEND_URL}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: query,
                session_id: SESSION_ID
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (!response.ok) throw new Error("Failed to get answer");

        const result = await response.json();

        // Remove typing indicator & show answer
        removeMessage(typingId);
        addMessage('bot', result.answer);

    } catch (error) {
        console.error(error);
        removeMessage(typingId);
        
        let errorMsg = "❌ Sorry, I encountered an error while processing your request.";
        if (error.name === 'AbortError') {
            errorMsg = "⏱️ Request timed out. The server might be busy or loading models. Please try again.";
        }
        
        addMessage('bot', errorMsg);
    } finally {
        sendBtn.disabled = false;
        userQuery.focus();
    }
}

/* =========================================
   UI HELPERS
   ========================================= */

function addMessage(sender, text) {
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;

    // Icon
    const icon = sender === 'bot' ? 'ri-robot-2-fill' : 'ri-user-smile-fill';

    // Markdown Parsing (using marked.js)
    const content = sender === 'bot' ? marked.parse(text) : text;

    div.innerHTML = `
        <div class="avatar">
            <i class="${icon}"></i>
        </div>
        <div class="message-content">
            ${content}
        </div>
    `;

    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return div.id = 'msg-' + Date.now();
}

function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.className = 'message bot-message';
    div.id = id;
    div.innerHTML = `
        <div class="avatar"><i class="ri-robot-2-fill"></i></div>
        <div class="message-content" style="padding: 12px 20px;">
            <i class="ri-more-fill" style="animation: pulse 1s infinite;"></i>
        </div>
    `;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function clearSession() {
    if (confirm("Are you sure you want to clear the session and all files?")) {
        location.reload();
    }
}

function showToast(msg, type = 'info') {
    // Simple alert replacement for now, ideally a custom toast
    // But since we have a connection-toast element, we could reuse it or alert
    if (type === 'error') alert("❌ " + msg);
    else if (type === 'warning') alert("⚠️ " + msg);
    else alert(msg);
}
