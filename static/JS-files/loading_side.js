
//TODO:description of the game is which game and which mode it is

jQuery(document).ready(function($) {
    // Sample JSON data (replace this with your actual data)
    var playersData = [
        {"img_profile": "default.png", "nickName": "Player 1"},
        {"img_profile": "default.png", "nickName": "Player 2"},
        {"img_profile": "default.png", "nickName": "Player 3"}
    ];

    var url = '/table/'+table_id+'/player_data'

    // Function to replace the player HTML content form the data received
    function updatePlayersUI(data) {
        var player_numberElement = document.getElementById('player_number');
        player_numberElement.textContent = data[0][0]+"/"+data[0][1];

        var playersContainer = $('.players .playerss'); // Selecting the nested element
        playersContainer.empty(); // Clear existing player data

        for (var i = 1; i < data.length; i++) {
            var playerHTML = '<div class="player">' +
                '<img src="../static/Profil_images/' + data[i][1] + '" alt="' + data[i][0] + '">' +
                '<span>' + data[i][0] + '</span>' +
                '</div>';
            playersContainer.append(playerHTML);
        }

    }

     function fetchPlayerData() {
        $.ajax({
            url: '/table/'+table_id+'/player_data',
            type: 'GET',
            success: function(response) {
                //TODO: Fix the response data
                var tableLength = response[0][0];
                if (tableLength == response[0][1] && response[0][1] != 0){
                    window.location.href = '/table/'+table_id+'/game';
                }
                var playMode = response[0][1];
                console.log("Table Length:", tableLength);
                console.log("Play Mode:", playMode);
                updatePlayersUI(response); // Update UI with received data
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