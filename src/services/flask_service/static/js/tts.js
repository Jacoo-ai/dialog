let started = false;
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
          started = true;
          send_text("hello, really nice to meet you");
          enable_speak();
        },
        sessionDisconnected: () => {
          // Timeout handler.
        },
      });
    } catch (error) {
      console.error("Initialized failed", error);
    }
  });

  // sendTextButton.addEventListener('click', () => {
  //   const text = textInput.value;
  //   if (started && text) {
  //     rapportScene.modules.tts.sendText(text);
  //   } else {
  //     console.error("Not started or no text");
  //   }
  // });

  endButton.addEventListener('click', async () => {

    if (started) {
      await rapportScene.sessionDisconnect();
      started = false;
    } else {
      console.error("Have disconnected");
    }
  });

  async function send_text(text) {
    if (started && text) {
       rapportScene.modules.tts.sendText(text)
      // rapportScene.modules.tts.sendText(text);
    } else {
      console.error("Not started or no text");
    }
  }

  function getTextUpdater() {
      $.ajax({
          url: '/get_text',
          type: 'GET',
          dataType: 'json',
          success: function (data) {
              var text_content = data.text_content

              if (text_content === "") {
                console.log("No text");
              } else {
                send_text(text_content)
                console.log("Popped text:", text_content);
              }
              // 定时调用
              setTimeout(getTextUpdater, 1000);
          }
      });
  }


    function enable_speak() {
      $.ajax({
          url: '/enable_speak',
          type: 'GET',
          dataType: 'json',
          success: function (data) {
              console.log("enabled");
          }
      });
  }

  function disable_speak() {
      $.ajax({
          url: '/disable_speak',
          type: 'GET',
          dataType: 'json',
          success: function (data) {
              console.log("enabled");
          }
      });
  }