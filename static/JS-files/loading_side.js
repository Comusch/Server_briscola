jQuery(document).ready(function($) {
    // Sample JSON data (replace this with your actual data)
    var playersData = [
        {"img_profile": "default.png", "nickName": "Player 1"},
        {"img_profile": "default.png", "nickName": "Player 2"},
        {"img_profile": "default.png", "nickName": "Player 3"}
    ];

    var url = '/table/'+table_id+'/player_data'

    // Function to replace the player HTML content
    function updatePlayersUI(players) {
        var player_numberElement = document.getElementById('.player_number');
        player_numberElement.textContent = players[0][0]

        var playersContainer = $('.players .playerss'); // Selecting the nested element
        playersContainer.empty(); // Clear existing player data

        players.slice(1).forEach(function(player) {
            var playerHTML = '<div class="player">' +
                                 '<img src="../static/Profil_images/' + player[1]+ '" alt="' + player[0] + '">' +
                                 '<span>' + player[0] + '</span>' +
                             '</div>';
            playersContainer.append(playerHTML);
        });

    }

     function fetchPlayerData() {
        $.ajax({
            url: '/table/'+table_id+'/player_data',
            type: 'GET',
            success: function(response) {
                //TODO: Fix the response data
                var tableLength = data[0][0];
                var playMode = data[0][1];
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
    setInterval(fetchPlayerData, 10000); // 10000 milliseconds = 10 seconds
});