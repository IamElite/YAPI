async function testAudio() {
    try {
        const response = await fetch('/api/yt-audio-video?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audiobest', {
            headers: {'X-API-Key': 'BadApiYt'}
        });
        if (!response.ok) throw new Error('Failed to fetch audio');
        const blob = await response.blob();
        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = URL.createObjectURL(blob);
        document.getElementById('mediaPlayer').innerHTML = '';
        document.getElementById('mediaPlayer').appendChild(audio);
        audio.play();
    } catch (error) {
        console.error('Error testing audio:', error);
        alert('Failed to load audio. Please try again.');
    }
}

async function testVideo() {
    try {
        const response = await fetch('/api/yt-audio-video?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=best', {
            headers: {'X-API-Key': 'BadApiYt'}
        });
        if (!response.ok) throw new Error('Failed to fetch video');
        const blob = await response.blob();
        const video = document.createElement('video');
        video.controls = true;
        video.src = URL.createObjectURL(blob);
        document.getElementById('mediaPlayer').innerHTML = '';
        document.getElementById('mediaPlayer').appendChild(video);
        video.play();
    } catch (error) {
        console.error('Error testing video:', error);
        alert('Failed to load video. Please try again.');
    }
}

async function playMedia(type) {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('Please enter a YouTube URL');
        return;
    }
    try {
        const response = await fetch(`/api/yt-audio-video?url=${encodeURIComponent(url)}&quality=${type}best`, {
            headers: {'X-API-Key': 'BadApiYt'}
        });
        if (!response.ok) throw new Error(`Failed to fetch ${type}`);
        const blob = await response.blob();
        const media = document.createElement(type === 'audio' ? 'audio' : 'video');
        media.controls = true;
        media.src = URL.createObjectURL(blob);
        document.getElementById('mediaPlayer').innerHTML = '';
        document.getElementById('mediaPlayer').appendChild(media);
        media.play();
    } catch (error) {
        console.error(`Error playing ${type}:`, error);
        alert(`Failed to play ${type}. Please check the URL and try again.`);
    }
}

function downloadMedia(format) {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('Please enter a YouTube URL');
        return;
    }
    window.location.href = `/api/yt-download?url=${encodeURIComponent(url)}&format=${format}&X-API-Key=BadApiYt`;
}
