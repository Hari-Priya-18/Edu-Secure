document.addEventListener('DOMContentLoaded', function() {
    const searchIcon = document.getElementById('searchIcon');

    if (searchIcon) {
        searchIcon.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            window.location.href = '/search'; // Redirect to the search page (Flask route)
        });
    }
});