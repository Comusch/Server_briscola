current_bet = 99

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

//with this function you can get the number of the player(p_id : id form the server) for the player on the bord
//get number between 0 and 4 without 3
function get_id_form_p_id(p_id){
    for(var i = 0; i < player_field.length; i++) {
        if(p_id == player_field[i][0]) {
            return i
        }
    }
}


function changetheBorder_of_activePlayer(data_active_player_id){
    var number_active = -1;
    number_active = get_id_form_p_id(data_active_player_id)
    for(var i = 0; i<5; i++) {
        if(i==3){
            continue;
        }
        var playerElement = document.getElementById('player'+i);
        if(i == number_active){
            playerElement.style.border = '4px solid green';
        }
        else{
            playerElement.style.border = 'none';
        }
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

function get_Name_of_player(p_id) {
    for(const player of player_field){
        if (player[0] == p_id){
            return player[1]
        }
    }
}

function change_Speech_field(p_id, text){
    var b_p_id = get_id_form_p_id(p_id)
    var playerElement = document.getElementById('call_player_'+b_p_id);
    if (text == ""){
        playerElement.textContent = "";
    }
    else{
        playerElement.textContent = text;
    }
}

function change_game_state_lable(text){
    var lableElemnt = document.getElementById('StichLable')
    lableElemnt.textContent = text;
}

//main function to update the website
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

            var bet_p_id = data[9][1]
            var lowest_bet = data[9][0]
            change_game_state_lable("Betting:...")
            //TODO: get a card name of the card value lowest bet and show it with the name of the player, who bet on this card value, on the lable of the bord
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

        //show, which player is active and which not (with a green circle at the profil pictures)
        changetheBorder_of_activePlayer(data[7])

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


