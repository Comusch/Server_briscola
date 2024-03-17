//front-End game Controller
//Toggle the Will you play screen
function toggleWillYouPlay() {
    var Will_you_playElement = document.getElementById("Will_you_play");
    if (Will_you_playElement.display === "none") {
        Will_you_playElement.style.display = "flex";
    } else {
        Will_you_playElement.style.display = "none";
    }
}

//Toggle the game screen
function toggleWhoWins() {
    var whoWinsElement = document.getElementById("who_wins");
    if (whoWinsElement.style.display === "none" || whoWinsElement.style.display === "") {
        whoWinsElement.style.display = "flex"; // Show the element
    } else {
        whoWinsElement.style.display = "none"; // Hide the element
    }
}

