const openMicrophoneButton = document.getElementById('openMicrophoneButton');
const closeMicrophoneButton = document.getElementById('closeMicrophoneButton');

let microphone;
let socket;
let asrStarted = false;

openMicrophoneButton.addEventListener("click", async () => {

    if (!microphone && asrStarted) {
        microphone = await getMicrophone();
        await openMicrophone(microphone, socket);
    }
});

async function openMicrophone_helper() {
    if (!microphone && asrStarted) {
        microphone = await getMicrophone();
        await openMicrophone(microphone, socket);
    }
}

closeMicrophoneButton.addEventListener("click", async () => {

    if (microphone) {
        await closeMicrophone(microphone);
        microphone = undefined;
    }
});

window.addEventListener("load", async () => {

    const key = "88117800e0472e1c435f883aeeacba4542feec68";
    const {createClient} = deepgram;
    const _deepgram = createClient(key);

    socket = _deepgram.listen.live({
        model: "nova-2",
        smart_format: true,
        endpointing: 200,
    });

    socket.on("open", async () => {
        asrStarted = true;
        console.log("client: connected to websocket");
        await openMicrophone_helper()
        socket.on("Results", (data) => {
            // console.log(data);
            const transcript = data.channel.alternatives[0].transcript;

            if (transcript !== "")
                send_asr_text(transcript);

        });
        socket.on("error", (e) => console.error(e));
        socket.on("warning", (e) => console.warn(e));
        socket.on("Metadata", (e) => console.log(e));
        socket.on("close", (e) => console.log(e));

    });
});

function send_asr_text(text) {
    addMessage("User", text, "../static/img/User.png")
    $.ajax({
        url: '/asr_text',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({text_content: text}),
    });
}