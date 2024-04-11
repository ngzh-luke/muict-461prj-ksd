import { TypingDNA } from "./dna.js";
import { AutocompleteDisabler } from "./autocomplete-disabler.js";

// https://github.com/TypingDNA/autocomplete-disabler

const tdna = new TypingDNA();

const autocompleteDisabler = new AutocompleteDisabler({
  showTypingVisualizer: true,
  showTDNALogo: true,
});
autocompleteDisabler.disableAutocomplete();
autocompleteDisabler.disableCopyPaste();

const loginButton = document.getElementById("login");
if (loginButton) {
  loginButton.addEventListener("click", () => loginOrSignUp(true));
  tdna.addTarget("inputUsername");
  tdna.addTarget("inputPassword");
}

const signUpButton = document.getElementById("signup");
if (signUpButton) {
  signUpButton.addEventListener("click", () => loginOrSignUp(false));
  tdna.addTarget("inputUsername");
  tdna.addTarget("inputPassword");
  tdna.addTarget("inputPassword2");
}

export function loginOrSignUp(login = true) {
  const username = document.getElementById("inputUsername").value;
  const password = document.getElementById("inputPassword").value;

  let endpoint;
  if (login) {
    endpoint = "/login-dna/";
  } else {
    endpoint = "/signup-dna/";
  }

  fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: username }),
  })
    .then((res) => {
      return res.json();
      // console.log(e);
    })
    .then((data) => {
      alert(data);
      if (data.userID) {
        sendTypingData(data.userID, password);
      } else if (data.message) {
        alert(data.message);
      }
    });
}

const typingPatternsButton = document.getElementById("typing-patterns-button");
if (typingPatternsButton) {
  typingPatternsButton.addEventListener("click", () => loginOrSignUp(true));
  tdna.addTarget("inputUsername");
  tdna.addTarget("inputPassword");
}

function sendTypingData(id, text) {
  const pattern = tdna.getTypingPattern({
    type: 1,
    text: text,
  });
  fetch("/api/send/dna", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pattern: pattern, userID: id }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.message_code == 10) {
        alert(
          "We need to collect some typing data from you. You may be asked to fill out this form multiple times."
        );
        window.location.href = "tools/typing-patterns";
      } else {
        if (data.result == 1) {
          alert(
            "TypingDNA indicated that there was HIGH confidence in your login."
          );
        } else {
          alert(
            "TypingDNA indicated that there was LOW confidence in your login."
          );
        }
        window.location.href = "/";
      }
    });
  tdna.reset();
}
