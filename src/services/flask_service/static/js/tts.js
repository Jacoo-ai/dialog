let enableTTS = false;
let textUpdater;
const rapportScene = document.getElementById('rapportScene');
const demoButton = document.getElementById('demoButton');
const endButton = document.getElementById('endButton');

demoButton.addEventListener('click', async () => {
    const enableCookies = false;

    try {
        await rapportScene.sessionRequest({
            projectId: '0af3897d-9454-4b87-b1a1-b3ef18a709a9',
            projectToken: '7e653f4c-4b29-4929-bd07-488707b3a423',
            aiUserId: 'a32a2b2b-fd77-48d7-9795-36f84ea26965',
            lobbyZoneId: 'MPA',
            openingText: 'Start',
            enableCookies,
            sessionConnected: () => {
                notice_complete();
                enableTTS = true;
                send_text("hello, really nice to meet you");
            },
            sessionDisconnected: () => {
                // Timeout handler.
            },
        });
    } catch (error) {
        console.error("Initialized failed", error);
    }
});


endButton.addEventListener('click', async () => {

    if (enableTTS) {
        cancelTextUpdater();
        await rapportScene.sessionDisconnect();
        enableTTS = false;
    } else {
        console.log("Have disconnected");
    }
});

async function send_text(text) {
    // addMessage("Agent", text, "../static/img/Agent.png");
    if (enableTTS && text) {
        rapportScene.modules.tts.sendText(text)
    } else {
        console.error("Not started or no text");
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', function () {
        console.log('Connected to Flask');
    });

    socket.on('disconnect', function () {
        console.log('Disconnected to Flask');
    });

    socket.on('get_tts_text', function (data) {
        send_text(data.text_content)
        console.log("Popped text:", data.text_content);
    });

    socket.on('get_tts_command', function (data) {
        rapportScene.modules.commands.stopAllSpeech();
        console.log("Stopped!!!");
    });
});

rapportScene.addEventListener('ttsStart', (e) => {
    $.ajax({
        url: '/tts_start', type: 'GET', dataType: 'json', success: function (data) {
            console.log("tts_disabled");
        }
    });
});


rapportScene.addEventListener('ttsEnd', (e) => {
    $.ajax({
        url: '/tts_end', type: 'GET', dataType: 'json', success: function (data) {
            console.log("tts_enabled");
        }
    });
});

function cancelTextUpdater() {
    clearTimeout(textUpdater);
}
