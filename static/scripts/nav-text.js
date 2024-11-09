var wordsToType = document.querySelector("span[words]").getAttribute("words").split(',');
var typer = document.querySelector("span[words]");
var typingSpeed = (parseInt(typer.getAttribute('typing-speed')) || 70);
var typingDelay = (parseInt(typer.getAttribute('typing-delay')) || 700);

var currentWordIndex = 0, currentCharacterIndex = 0;

function type() {
  var wordToType = wordsToType[currentWordIndex % wordsToType.length];

  if (currentCharacterIndex < wordToType.length) {
    typer.innerHTML += wordToType[currentCharacterIndex++];
    setTimeout(type, typingSpeed);
  } else {
    setTimeout(erase, typingDelay);
  }
}

function erase() {
  var wordToType = wordsToType[currentWordIndex % wordsToType.length];
  if (currentCharacterIndex > 0) {
    typer.innerHTML = wordToType.substring(0, --currentCharacterIndex - 1);
    setTimeout(erase, typingSpeed);
  } else {
    currentWordIndex++;
    setTimeout(type, typingDelay);
  }
}

window.onload = function() {
  type();
};