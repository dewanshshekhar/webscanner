document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('videoElement');
    const cameraToggleBtn = document.getElementById('cameraToggleBtn');
    const fileInput = document.getElementById('fileInput');
    const scanningOverlay = document.getElementById('scanning-overlay');
    const videoContainer = document.getElementById('video-container');

    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');

    let stream = null;
    let isCameraActive = false;

    // Chat Message History
    let messages = [
        { role: 'assistant', content: 'Hello, welcome to the Sanskrit Mantra Converter. How can I assist you with your translation needs today?' }
    ];

    // Helper: Add message to Chat UI
    function appendMessage(role, content) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${role === 'user' ? 'user' : 'bot'}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        // Parse markdown if it's from the bot
        contentDiv.innerHTML = role === 'bot' || role === 'assistant' ? marked.parse(content) : content;

        msgDiv.appendChild(contentDiv);
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Initialize Camera
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            video.srcObject = stream;
            isCameraActive = true;
            videoContainer.style.display = 'block';
        } catch (err) {
            console.error("Error accessing camera:", err);
            isCameraActive = false;
            videoContainer.style.display = 'none';
            alert("Camera access denied or unavailable. You can still type messages or upload an image.");
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            video.srcObject = null;
            isCameraActive = false;
            videoContainer.style.display = 'none';
        }
    }

    // Toggle Camera View
    cameraToggleBtn.addEventListener('click', () => {
        if (isCameraActive) {
            // If active, it means we clicked it to capture
            captureAndScan();
        } else {
            // Start Camera
            startCamera();
        }
    });

    // Send text message
    async function sendMessage(text) {
        if (!text.trim()) return;

        // Add user message to UI
        appendMessage('user', text);
        messages.push({ role: 'user', content: text });
        chatInput.value = '';

        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.id = loadingId;
        loadingDiv.className = 'chat-message bot';
        loadingDiv.innerHTML = `<div class="message-content"><div class="spinner" style="width:20px;height:20px;border-width:2px;margin:0;"></div></div>`;
        chatWindow.appendChild(loadingDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: messages })
            });

            const data = await response.json();

            // Remove loading
            document.getElementById(loadingId).remove();

            if (data.success && data.reply) {
                appendMessage('assistant', data.reply);
                messages.push({ role: 'assistant', content: data.reply });
            }

        } catch (error) {
            console.error(error);
            document.getElementById(loadingId).remove();
            appendMessage('assistant', "Sorry, I encountered an error connecting to the converter.");
        }
    }

    // Process Image for OCR
    async function processImage(imageSource) {
        scanningOverlay.classList.remove('active');
        stopCamera();

        // Show parsing status in chat
        appendMessage('user', '*(Scanning image for Sanskrit text...)*');

        try {
            // Run Tesseract OCR (Sanskrit + English)
            const result = await Tesseract.recognize(
                imageSource,
                'hin+san+eng',
                { logger: m => console.log(m.status, m.progress) }
            );

            const rawText = result?.data?.text || "";
            const text = rawText.trim();

            if (!text || text.length === 0) {
                appendMessage('assistant', "No Text Detected. Please try scanning a clearer image or ensure the text is visible.");
                return;
            }

            // Send extracted text to the chat
            sendMessage(`I scanned the following text: \n\n${text}`);

        } catch (error) {
            console.error(error);
            appendMessage('assistant', "Error analyzing text: " + error.message);
        }
    }

    // Capture from Camera
    function captureAndScan() {
        if (!isCameraActive) return;
        scanningOverlay.classList.add('active');

        setTimeout(() => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            processImage(canvas.toDataURL('image/jpeg'));
        }, 1000);
    }

    // Upload from File
    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            const reader = new FileReader();

            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);
                    processImage(canvas.toDataURL('image/jpeg'));
                };
                img.src = event.target.result;
            };

            reader.readAsDataURL(file);
        }
    });

    // Chat controls
    sendBtn.addEventListener('click', () => {
        sendMessage(chatInput.value);
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(chatInput.value);
        }
    });

    // Hide camera initially
    videoContainer.style.display = 'none';
});
