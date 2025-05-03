
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".alert").forEach(function(alert) {
        alert.addEventListener("click", function() {
            alert.classList.add("hidden");
        });

        setTimeout(function() {
            alert.classList.add("hidden");
        }, 6000);
    });


})