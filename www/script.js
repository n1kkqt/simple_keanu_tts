function _handleSubmit() {
    return new Promise((resolve, reject) => {
      var text = document.getElementById("myText").value;
      console.log(text);
      let formData = new FormData();

      var textString = JSON.stringify(text);

      formData.append("text", textString);
      
      var xhr = new XMLHttpRequest();
      var z = this;
      
      xhr.open('post', '/play/text', true);
      
      xhr.onload = async function () {
        if (this.status == 200) {
          var msg = JSON.parse(this.response);
          var audio = new Audio("data:Audio/WAV;base64," + msg.wav);
          var audioLength = parseFloat(msg.len);
          document.getElementById("keanuGif").src = "talk.gif";
          audio.play();
          await sleep(audioLength*1000);
          document.getElementById("keanuGif").src = "idle.gif";
          resolve(this.response);
        } else {
          reject(this.statusText);
        }
      };
      
      xhr.send(formData);
  
    });
  }

function sleep(ms) {
  return new Promise(
    resolve => setTimeout(resolve, ms)
  );
}