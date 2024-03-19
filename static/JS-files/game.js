//front-End game Controller
//Toggle the Will you play screen
function toggleWillYouPlay(show) {
    var Will_you_playElement = document.getElementById("Will_you_play");
    if (show) {
        Will_you_playElement.style.display = "flex";
    } else {
        Will_you_playElement.style.display = "none";
    }
}

//Toggle the game screen
function toggleWhoWins(show) {
    var whoWinsElement = document.getElementById("who_wins");
    if (show) {
        whoWinsElement.style.display = "flex"; // Show the element
    } else {
        whoWinsElement.style.display = "none"; // Hide the element
    }
}

//change with which card the player wants to play
function changeColor_visibility(show){
    var with_which_cardElement = document.getElementById("with_which_color");
    if (show) {
        with_which_cardElement.style.display = "flex"; // Show the element
    }
    else {
        with_which_cardElement.style.display = "none"; // Hide the element
    }
}

// Function to change the image source of a button
function changeImage(buttonId, newImageSrc) {
    var button = document.getElementById(buttonId);
    console.log("Button:", button);
    if (button) {
        var img = button.querySelector('img');
        if (img) {
            if (newImageSrc) {
                img.src = newImageSrc;
                button.style.display = 'inline-block'; // Show the button
            } else {
                button.style.display = 'none'; // Hide the button if no image source
            }
        }
    }
}

// Function to send data to the server
 function sendDataToServer(data) {
    // Construct the request options
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    // Make the fetch request
    fetch('/table/' + table_id + '/send_action', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse response JSON
        })
        .then(data => {
            console.log('Response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

//Buttons for the will you play screen
function button_will_you_play_click(value){
    console.log("Value:", value);
    var data = {
        "action": 1,
        "bet": value
    };
    sendDataToServer(data);
}


function selectTrumpfColor(value){
    console.log("Value:", value);
    var data = {
        "action": 2,
        "color": value
    }
    sendDataToServer(data);
}

function playCard(value){
    console.log("Value:", value);
    var data = {
        "action": 3,
        "id_Hand": value
    }
    sendDataToServer(data);
}






jQuery(document).ready(function($) {
    // Sample JSON data (replace this with your actual data)

    var url = '/table/'+table_id+'/game_data'

    // Function to replace the player HTML content form the data received
    // so the ui will be updated
    function updatePlayersUI(data) {

        if (data[0] == 0 && data[1] == 1){
            toggleWillYouPlay(true);
            toggleWhoWins(false);
            changeColor_visibility(false);
        }
        else if (data[0] == 0 && data[1] == 0){
            toggleWillYouPlay(false);
            toggleWhoWins(false);
            changeColor_visibility(false);

            //TODO: change the text of the lable, in which play phase we are
        }
        else if (data[0] == 1 && data[1] == 1){
            toggleWillYouPlay(false);
            toggleWhoWins(false);
            changeColor_visibility(true);
        }
        else if (data[0] == 1 && data[1] == 0) {
            toggleWillYouPlay(false);
            toggleWhoWins(false);
            changeColor_visibility(false);

            //TODO: change the text of the lable, in which play phase we are
        }
        else if (data[0] == 2)
        {
            toggleWillYouPlay(false);
            toggleWhoWins(false);
            changeColor_visibility(false);

            //TODO: aktive the button to play the cards and see the last stack

        }
        else if (data[0] == 3)
        {
            toggleWillYouPlay(false);
            toggleWhoWins(true);
            changeColor_visibility(false);
            // end of the game
        }

        //show the hand cards
        var handCardsinformation = data[2];
        for (var i = 0; i < 8; i++){
            if (handCardsinformation[i] != null){
                var card = handCardsinformation[i];
                if (card <10){
                    card = "0"+card;
                }
                src_image = "/static/Bilddateien/Card"+card+".png";
                changeImage("card"+i, src_image);
            }
            else
            {
                changeImage("card"+i, null);
            }

        }

        //show the played cards on the table
        var playedCardsinformation = data[3];
        const cardorder = [0, 1, 3, 4, 2]

        for (var i = 0; i < 5; i++){
            if (playedCardsinformation[i] != null){
                var card = playedCardsinformation[i][0];
                if (card <10){
                    card = "0"+card;
                }
                src_image = "/static/Bilddateien/Card"+card+".png";
                changeImage("bord_card"+cardorder[i], src_image);
            }
            else
            {
                src_image = "/static/Bilddateien/Card_placeholder.png";
                changeImage("bord_card"+cardorder[i], src_image);
            }
        }

    }

    //Function to fetch the data from the server to update the UI
     function fetchPlayerData() {
        $.ajax({
            url: url,
            type: 'GET',
            success: function(response) {

                console.log("Game Data:", response);
                if (response == null){
                    window.location.href = '/';
                }
                else{
                    updatePlayersUI(response); // Update UI with received data
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }

    fetchPlayerData(); // Fetch player data when the page loads

    // Example: Call updatePlayerData function every 10 seconds
    setInterval(fetchPlayerData, 1000); // 10000 milliseconds = 1 seconds
});


