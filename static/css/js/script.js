console.log("SCRIPT JS LOADED");
function toggleDropdown(menuId) {

    // Get the selected dropdown
    const selectedMenu = document.getElementById(menuId);


    // Close all other dropdowns
    document.querySelectorAll(".dropdown-content").forEach(function(menu) {

        if (menu.id !== menuId) {
            menu.classList.remove("show");
        }

    });


    // Open / close selected dropdown
    selectedMenu.classList.toggle("show");
}


/* Close dropdown when clicking outside */

document.addEventListener("click", function(event) {

    if (!event.target.closest(".dropdown")) {

        document.querySelectorAll(".dropdown-content").forEach(function(menu) {

            menu.classList.remove("show");

        });

    }

});