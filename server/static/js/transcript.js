let transcriptData = undefined;

async function extractTranscript() {
  const url = document.getElementById("urlInput").value;

  if (!url) {
    showError("Please enter a YouTube URL.");
    return;
  }

  document.getElementById("loading").style.display = "block";
  document.getElementById("error").style.display = "none";
  document.getElementById("results").style.display = "none";

  try {
    const response = await fetch("/api/v1/transcript", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();
    document.getElementById("loading").style.display = "none";

    if (!data.success) {
      showError(data.error || "Something went wrong.");
      return;
    }

    displayResults(data);
  } catch (err) {
    console.error("Error fetching transcript:", err);
    document.getElementById("loading").style.display = "none";
    showError("Error fetching transcript.");
  }
}

function displayResults(data) {
  document.getElementById("results").style.display = "block";

  // Show video info
  const videoInfoHTML = `
    <div class="video-header">
      <img src="${data.thumbnail}" alt="Thumbnail" style="width: 100%; max-height: 250px; object-fit: cover;" />
      <h2>${data.title}</h2>
      <p><strong>Channel:</strong> ${data.channel}</p>
    </div>
  `;
  document.getElementById("videoInfo").innerHTML = videoInfoHTML;

  // Stats
  const statsHTML = `
    <div><strong>📝 Word Count:</strong> ${data.word_count}</div>
    <div><strong>⏱ Estimated Duration:</strong> ${data.estimated_duration}</div>
  `;
  document.getElementById("stats").innerHTML = statsHTML;

  // Keywords
  const keywordsHTML = `
    <ul>
      ${extractKeywords(data.transcript).map(word => `<li>${word}</li>`).join("")}
    </ul>
  `;
  document.getElementById("keywords").innerHTML = keywordsHTML;

  // Save transcript data for download
  transcriptData = data.transcript;

  // Full Transcript
  document.getElementById("transcript").innerText = data.transcript;
}

function downloadTranscript() {
  if (!transcriptData) {
    showError("Transcript data is missing.");
    return;
  }

  const blob = new Blob([transcriptData], { type: "text/plain" });
  const downloadUrl = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = downloadUrl;
  a.download = "transcript.txt";
  document.body.appendChild(a);
  a.click();
  a.remove();

  URL.revokeObjectURL(downloadUrl);
}

function convertAudioToText(formId = 'uploadForm', inputId = 'audioInput', resultId = 'transcriptResult') {
  const form = document.getElementById(formId);
  const audioInput = document.getElementById(inputId);
  const transcriptDiv = document.getElementById(resultId);

  if (!form || !audioInput || !transcriptDiv) {
    console.error("Missing required elements in the DOM.");
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!audioInput.files.length) {
      transcriptDiv.innerHTML = '<p style="color:red;">Please select a file.</p>';
      return;
    }

    const formData = new FormData();
    formData.append('file', audioInput.files[0]);

    try {
      transcriptDiv.innerHTML = 'Uploading and transcribing...';

      const response = await fetch('/api/v1/upload', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.error) {
        transcriptDiv.innerHTML = `<p style="color:red;">${result.error}</p>`;
        return;
      }

      transcriptDiv.innerHTML = `
        <p><strong>Uploaded:</strong> ${result.filename}</p>
        <p><strong>Transcript:</strong><br>${result.transcript || 'Transcription not implemented yet.'}</p>
      `;

    } catch (err) {
      console.error(err);
      transcriptDiv.innerHTML = '<p style="color:red;">Something went wrong.</p>';
    }
  });
}

// Initialize the upload handler after the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  convertAudioToText();
});

function showError(message) {
  document.getElementById("error").style.display = "block";
  document.getElementById("error").innerText = message;
}

function clearResults() {
  document.getElementById("urlInput").value = "";
  document.getElementById("results").style.display = "none";
  document.getElementById("error").style.display = "none";
}

function loadSampleVideo() {
  document.getElementById("urlInput").value = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
  extractTranscript().then(r => {});
}

function extractKeywords(text) {
  // Simple keyword extraction (placeholder)
  const words = text.toLowerCase().split(/\W+/);
  const freq = {};
  words.forEach(word => {
    if (word.length > 4) freq[word] = (freq[word] || 0) + 1;
  });

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word]) => word);
}
