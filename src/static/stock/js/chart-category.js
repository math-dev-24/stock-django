document.addEventListener('DOMContentLoaded', function() {

    const categoriesElement = document.getElementById('categories-list');

    if (!categoriesElement) {
        console.error("Élément #categories-list introuvable");
        return;
    }

    let categoriesData;
    try {
        categoriesData = JSON.parse(categoriesElement.textContent);
    } catch (error) {
        console.error("Erreur de parsing JSON:", error);
        console.log("Contenu brut:", categoriesElement.textContent);
        return;
    }

    const labels = categoriesData.map(cat => cat.name);
    const quantities = categoriesData.map(cat => parseInt(cat.quantity, 10));

    const backgroundColors = generateColors(categoriesData.length);

    const ctx = document.getElementById('categoryChart').getContext('2d');

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Nombre de produits',
                data: quantities,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(255, 255, 255, 0.8)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });


    function generateColors(count) {
        const colors = [];
        // Palette de couleurs prédéfinies pour un meilleur rendu visuel
        const colorPalette = [
            'rgba(255, 99, 132, 0.7)',    // Rose
            'rgba(54, 162, 235, 0.7)',    // Bleu
            'rgba(255, 206, 86, 0.7)',    // Jaune
            'rgba(75, 192, 192, 0.7)',    // Turquoise
            'rgba(153, 102, 255, 0.7)',   // Violet
            'rgba(255, 159, 64, 0.7)',    // Orange
            'rgba(199, 199, 199, 0.7)',   // Gris
            'rgba(83, 102, 255, 0.7)',    // Bleu-violet
            'rgba(255, 99, 71, 0.7)',     // Rouge-orange
            'rgba(50, 205, 50, 0.7)'      // Vert
        ];

        for (let i = 0; i < count; i++) {
            if (i < colorPalette.length) {
                colors.push(colorPalette[i]);
            } else {
                const r = Math.floor(Math.random() * 200) + 55;
                const g = Math.floor(Math.random() * 200) + 55;
                const b = Math.floor(Math.random() * 200) + 55;
                colors.push(`rgba(${r}, ${g}, ${b}, 0.7)`);
            }
        }
        return colors;
    }
});