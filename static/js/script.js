function hideChat() {
  const chatSection = document.getElementById("chat-section");
  const chatInput = document.getElementById("chat-input");
  const messagesBtn = document.getElementById("messages");
  const participantsBtn = document.getElementById("participants");
  const chatParticipants = document.getElementById("chat-participants");

  chatParticipants.classList.remove("hidden");
  messagesBtn.classList.remove("selected");
  participantsBtn.classList.add("selected");
  chatSection.classList.add("hidden");
  chatInput.classList.add("hidden");
}

function toggleVisibility(isParticipants) {
  const chatSection = document.getElementById("chat-section");
  const chatInput = document.getElementById("chat-input");
  const messagesBtn = document.getElementById("messages");
  const participantsBtn = document.getElementById("participants");
  const chatParticipants = document.getElementById("chat-participants");

  if (isParticipants) {
    chatParticipants.classList.remove("hidden");
    messagesBtn.classList.remove("selected");
    participantsBtn.classList.add("selected");
    chatSection.classList.add("hidden");
    chatInput.classList.add("hidden");
  } else {
    chatParticipants.classList.add("hidden");
    messagesBtn.classList.add("selected");
    participantsBtn.classList.remove("selected");
    chatSection.classList.remove("hidden");
    chatInput.classList.remove("hidden");
  }
}

function hideChat() {
  toggleVisibility(true); // Show participants, hide chat
}

function hideParticipants() {
  toggleVisibility(false); // Show chat, hide participants
}

document.addEventListener("DOMContentLoaded", () => {
  const listItems = document.querySelectorAll("#my-list li");

  listItems.forEach((item) => {
    item.addEventListener("click", () => {
      listItems.forEach((i) => i.classList.remove("active"));
      item.classList.add("active");
    });
  });
});
