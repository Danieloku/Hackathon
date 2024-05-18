document.getElementById('audioForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('audio', document.getElementById('audio').files[0]);

    try {
        const response = await fetch('/transcribe', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        document.getElementById('transcriptionResult').innerText = result.transcription;
        document.getElementById('scheduleText').value = result.transcription;
    } catch (error) {
        console.error('Error transcribing audio:', error);
    }
});

document.getElementById('standardizeButton').addEventListener('click', async function() {
    const scheduleText = document.getElementById('scheduleText').value;

    try {
        const response = await fetch('/standardize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ schedule_text: scheduleText })
        });
        const result = await response.json();
        document.getElementById('standardizedResult').innerText = result.standardized_text;
    } catch (error) {
        console.error('Error standardizing text:', error);
    }
});

document.getElementById('createScheduleButton').addEventListener('click', async function() {
    const scheduleText = document.getElementById('standardizedResult').innerText;

    try {
        const response = await fetch('/create_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ schedule_text: scheduleText })
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Error creating schedule:', error);
    }
});
