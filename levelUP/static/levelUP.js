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
  loginButton.addEventListener("click", () => sendTypingData());
  tdna.addTarget("inputUsername");
  tdna.addTarget("inputPassword");
}

const signUpButton = document.getElementById("signup");
if (signUpButton) {
  signUpButton.addEventListener("click", () => sendTypingData());
  tdna.addTarget("inputUsername");
  tdna.addTarget("inputPassword");
  tdna.addTarget("inputPassword2");
}

const typingPatternsButton = document.getElementById("typing-patterns-button");
if (typingPatternsButton) {
  typingPatternsButton.addEventListener("click", () => sendTypingData());
  tdna.addTarget("inputUsername");
  tdna.addTarget("inputPassword");
}

export function sendTypingData() {
  const rootURL = window.location.origin;
  const fetchURL = `${rootURL}/api/get/dna`;
  const username = document.getElementById("inputUsername").value;
  const password = document.getElementById("inputPassword").value;
  const pattern = tdna.getTypingPattern({
    type: 1,
    text: username + password,
  });
  fetch(fetchURL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pattern: pattern, username: username }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // if (data.message_code == 10) {
      //   alert(
      //     "We need to collect some typing data from you. You may be asked to fill out this form multiple times."
      //   );
      //   window.location.href = "tools/typing-patterns";
      // }
    });
  tdna.reset();
}
