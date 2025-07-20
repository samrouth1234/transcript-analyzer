let recognition;
let isRecording = false;
let audioContext;
let source;
let processor;
let currentTranscript = '';

// Initialize Speech Recognition
function initSpeechRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Speech recognition is not supported in this browser. Please use Chrome, Safari, or Edge.');
        return false;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = document.getElementById('language').value;

    recognition.onstart = function() {
        isRecording = true;
        updateLiveStatus('🎤 Recording... Speak now!', 'recording');
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
    };

    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        if (finalTranscript) {
            currentTranscript += finalTranscript;
            document.getElementById('transcript').value = currentTranscript + interimTranscript;
        } else {
            document.getElementById('transcript').value = currentTranscript + interimTranscript;
        }
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        updateLiveStatus('❌ Error: ' + event.error, 'error');
        resetRecording();
    };

    recognition.onend = function() {
        if (isRecording) {
            updateLiveStatus('🎤 Recording stopped', 'processing');
        }
        resetRecording();
    };

    return true;
}

function startRecording() {
    if (!recognition && !initSpeechRecognition()) {
        return;
    }

    recognition.lang = document.getElementById('language').value;
    recognition.start();
}

function stopRecording() {
    if (recognition) {
        recognition.stop();
    }
    isRecording = false;
}

function resetRecording() {
    isRecording = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
}

function clearTranscript() {
    document.getElementById('transcript').value = '';
    currentTranscript = '';
    updateLiveStatus('', '');
    updateFileStatus('', '');
}

function updateLiveStatus(message, type) {
    const statusDiv = document.getElementById('liveStatus');
    if (message) {
        statusDiv.innerHTML = `<div class="status ${type}">${type === 'recording' ? '<span class="recording-indicator"></span>' : ''}${message}</div>`;
    } else {
        statusDiv.innerHTML = '';
    }
}

function updateFileStatus(message, type) {
    const statusDiv = document.getElementById('fileStatus');
    if (message) {
        statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
    } else {
        statusDiv.innerHTML = '';
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = URL.createObjectURL(file);
        audioPlayer.style.display = 'block';
        document.getElementById('transcribeBtn').disabled = false;
        updateFileStatus(`📁 File loaded: ${file.name}`, 'processing');
    }
}

function transcribeAudioFile() {
    if (!recognition && !initSpeechRecognition()) {
        return;
    }

    const audioPlayer = document.getElementById('audioPlayer');

    updateFileStatus('🎯 Starting transcription... Play the audio and speak along or let it play through speakers', 'processing');

    // Start recognition
    recognition.lang = document.getElementById('language').value;
    recognition.start();

    // Auto-play the audio
    audioPlayer.play();

    document.getElementById('transcribeBtn').disabled = true;
    document.getElementById('stopFileBtn').disabled = false;

    // Stop recognition when audio ends
    audioPlayer.onended = function() {
        setTimeout(() => {
            if (recognition) {
                recognition.stop();
            }
            updateFileStatus('✅ Transcription completed', 'processing');
            document.getElementById('transcribeBtn').disabled = false;
            document.getElementById('stopFileBtn').disabled = true;
        }, 1000);
    };
}

function stopFileTranscription() {
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.pause();

    if (recognition) {
        recognition.stop();
    }

    document.getElementById('transcribeBtn').disabled = false;
    document.getElementById('stopFileBtn').disabled = true;
    updateFileStatus('⏹️ Transcription stopped', 'processing');
}

function switchTab(tabName) {
    // Hide all content
    document.querySelectorAll('.method-content').forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected content and activate tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');

    // Stop any ongoing processes
    stopRecording();
    stopFileTranscription();
    clearTranscript();
}

function copyTranscript() {
    const transcript = document.getElementById('transcript');
    transcript.select();
    document.execCommand('copy');

    // Show feedback
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '✅ Copied!';
    setTimeout(() => {
        btn.textContent = originalText;
    }, 2000);
}

function downloadTranscript() {
    const transcript = document.getElementById('transcript').value;
    if (!transcript.trim()) {
        alert('No transcript to download!');
        return;
    }

    const blob = new Blob([transcript], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'transcript_' + new Date().toISOString().slice(0, 10) + '.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check if speech recognition is supported
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        document.body.innerHTML = `
            <div class="container">
                <h2>❌ Speech Recognition Not Supported</h2>
                <div class="feature-info">
                    <p>Your browser doesn't support speech recognition. Please use:</p>
                    <ul>
                        <li>Google Chrome (recommended)</li>
                        <li>Microsoft Edge</li>
                        <li>Safari (iOS/macOS)</li>
                    </ul>
                </div>
            </div>
        `;
        return;
    }

    // Update language when changed
    document.getElementById('language').addEventListener('change', function() {
        if (recognition) {
            recognition.lang = this.value;
        }
    });
});