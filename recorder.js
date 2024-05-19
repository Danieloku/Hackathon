let chunks = [];
let mediaRecorder;

const recordButton = document.getElementById("recordButton");
const stopButton = document.getElementById("stopButton");
const recordingsList = document.getElementById("recordingsList");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                chunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
                chunks = [];
                const audioURL = window.URL.createObjectURL(blob);
                const li = document.createElement("li");
                const audio = document.createElement("audio");
                audio.controls = true;
                audio.src = audioURL;
                li.appendChild(audio);
                recordingsList.appendChild(li);

                // Enviar el archivo grabado al servidor
                const formData = new FormData();
                formData.append('audio', blob, 'recording.ogg');
                fetch('/transcribe', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('transcriptionResult').innerText = data.transcription;
                    document.getElementById('scheduleText').value = data.transcription;
                })
                .catch(error => console.error('Error transcribing audio:', error));
            };
            mediaRecorder.start();
            recordButton.disabled = true;
            stopButton.disabled = false;
        })
        .catch((error) => {
            console.error("Error accessing microphone:", error);
        });
}

function stopRecording() {
    mediaRecorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;
}
