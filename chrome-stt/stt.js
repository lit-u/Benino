const micBtn = document.getElementById('micBtn');
const clearBtn = document.getElementById('clearBtn');
const transcriptEl = document.getElementById('transcript');
const statusEl = document.getElementById('status');
const copyStatusEl = document.getElementById('copyStatus');

let recognition = null;
let isRecording = false;
let fullText = '';

function copyToClipboard(text) {
  if (!text.trim()) return;
  navigator.clipboard.writeText(text.trim()).then(() => {
    copyStatusEl.textContent = '✓ Nukopijuota į clipboard';
    setTimeout(() => { copyStatusEl.textContent = ''; }, 2000);
  }).catch(() => {});
}

function startRecording() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    statusEl.textContent = '❌ Naršyklė nepalaiko STT';
    return;
  }

  recognition = new SR();
  recognition.lang = 'lt-LT';
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = () => {
    isRecording = true;
    micBtn.textContent = '⏹ Sustabdyti';
    micBtn.classList.add('recording');
    statusEl.textContent = '🔴 Įrašoma...';
  };

  recognition.onresult = (event) => {
    let interim = '';
    let finalChunk = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalChunk += transcript + ' ';
      } else {
        interim = transcript;
      }
    }

    if (finalChunk) {
      let chunk = finalChunk.trim();
      // Kapitalizuoti jei pradžia arba po taško
      if (!fullText.trim() || /[.!?]$/.test(fullText.trim())) {
        chunk = chunk.charAt(0).toUpperCase() + chunk.slice(1);
      }
      fullText += (fullText ? ' ' : '') + chunk;
      copyToClipboard(fullText);
    }

    transcriptEl.innerHTML =
      fullText +
      (interim ? '<span style="color:#555"> ' + interim + '</span>' : '');
  };

  recognition.onerror = (e) => {
    statusEl.textContent = '❌ Klaida: ' + e.error;
    if (e.error !== 'no-speech') stopRecording();
  };

  recognition.onend = () => {
    if (isRecording) recognition.start();
  };

  recognition.start();
}

function stopRecording() {
  isRecording = false;
  if (recognition) { recognition.stop(); recognition = null; }
  // Pridėti tašką pabaigoje jei reikia
  if (fullText.trim() && !/[.!?]$/.test(fullText.trim())) {
    fullText = fullText.trim() + '.';
    transcriptEl.innerHTML = fullText;
    copyToClipboard(fullText);
  }
  micBtn.textContent = '🎤 Įrašyti';
  micBtn.classList.remove('recording');
  statusEl.textContent = fullText.trim() ? 'Baigta — tekstas clipboard' : 'Paspausk mikrofono mygtuką';
}

micBtn.addEventListener('click', () => {
  isRecording ? stopRecording() : startRecording();
});

clearBtn.addEventListener('click', () => {
  stopRecording();
  fullText = '';
  transcriptEl.innerHTML = '';
  copyStatusEl.textContent = '';
  statusEl.textContent = 'Paspausk mikrofono mygtuką';
});

startRecording();
