class BoggleGame {
     /* Constructor: create a new game at the specified DOM id with an optional game length in seconds */

     constructor(boardId, secs = 60) {
          this.secs = secs; // Game length in seconds
          this.showTimer(); // Initialize and display the timer

          this.score = 0; // Initialize the score
          this.words = new Set(); // Initialize a set to store unique words
          this.board = $("#" + boardId); // Get the game board element from the DOM

          // Set up a timer that calls the tick method every 1000 milliseconds (1 second)
          this.timer = setInterval(this.tick.bind(this), 1000);

          // Add a submit event listener to the "add-word" form in the game board
          $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
          $word.val("").focus();
     }

     /* Show a word in the list of words */

     showWord(word) {
          // Append a new list item with the word to the "words" element in the game board
          $(".words", this.board).append($("<li>", { text: word }));
     }

     /* Show the current score in the HTML */

     showScore() {
          // Update the text of the "score" element in the game board with the current score
          $(".score", this.board).text(this.score);
     }

     /* Show a status message in the game board */

     showMessage(msg, cls) {
          // Set the text and CSS class of the "msg" element in the game board
          $(".msg", this.board)
               .text(msg)
               .removeClass()
               .addClass(`msg ${cls}`);
     }

     /* Handle the submission of a word: check if it's unique and valid, then score and display it */

     async handleSubmit(evt) {
          evt.preventDefault(); // Prevent the default form submission behavior
          const $word = $(".word", this.board); // Get the input field for the word

          let word = $word.val(); // Get the value of the input field
          if (!word) return; // If the input is empty, do nothing

          if (this.words.has(word)) {
               // If the word has already been found, show an error message
               this.showMessage(`Already found ${word}`, "err");
               return;
          }

          // Check the server for word validity
          const resp = await axios.get("/word-check", { params: { word: word } });
          if (resp.data.result === "not-word") {
               this.showMessage(`${word} is not a valid English word`, "err");
          } else if (resp.data.result === "not-on-board") {
               this.showMessage(`${word} is not a valid word on this board`, "err");
          } else {
               // If the word is valid, display it, update the score, and show a success message
               this.showWord(word);
               this.score += word.length;
               this.showScore();
               this.words.add(word);
               this.showMessage(`Added: ${word}`, "ok");
          }

          $word.val("").focus(); // Clear the input field and set focus back to it
     }

     /* Update the timer in the DOM */

     showTimer() {
          // Update the text of the "timer" element in the game board with the remaining seconds
          $(".timer", this.board).text(this.secs);
     }

     /* Handle a second passing in the game */

     async tick() {
          this.secs -= 1; // Decrease the remaining seconds by 1
          this.showTimer(); // Update and display the timer

          if (this.secs === 0) {
               // If the timer reaches 0, stop the timer and score the game
               clearInterval(this.timer);
               await this.scoreGame();
          }
     }

     /* End of the game: score the game and update the message */

     async scoreGame() {
          // Hide the "add-word" form in the game board
          $(".add-word", this.board).hide();

          // Send a POST request to the server to submit the final score
          const resp = await axios.post("/score", { score: this.score });

          if (resp.data.brokeRecord) {
               // If it's a new record, show a message with the new score
               this.showMessage(`New record: ${this.score}`, "ok");
          } else {
               // Otherwise, show a message with the final score
               this.showMessage(`Final score: ${this.score}`, "ok");
          }
     }
}
