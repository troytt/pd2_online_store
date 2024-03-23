document.getElementById('character-search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the character name from the input field
    var characterName = document.getElementById('character-name').value;

    // Redirect to the character page based on the input
    window.location.href = 'http://101.37.117.183:8080/api/char/' + characterName;
});

