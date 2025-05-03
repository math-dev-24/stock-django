

window.addEventListener("DOMContentLoaded", function() {

    document.getElementById("company-name").addEventListener("click", function() {
        document.getElementById("change-company-bg").classList.remove("hidden");
        document.getElementById("change-company").classList.remove("hidden");
    });

    document.getElementById("change-company-bg").addEventListener("click", function() {
        document.getElementById("change-company-bg").classList.add("hidden");
        document.getElementById("change-company").classList.add("hidden");
    });
});