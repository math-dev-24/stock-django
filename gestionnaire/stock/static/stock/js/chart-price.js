document.addEventListener('DOMContentLoaded', function() {
    const priceDataElement = document.getElementById('priceData');

    if (!priceDataElement) {
        console.error("L'élément contenant les données de prix n'a pas été trouvé");
        return;
    }

    let allPriceData;
    try {
        allPriceData = JSON.parse(priceDataElement.dataset.prices);

        allPriceData.forEach(item => {
            // Convertir l'année, le mois et le jour en nombres
            item.year = parseInt(item.year, 10);
            item.month = parseInt(item.month, 10);
            item.day = parseInt(item.day, 10);
            item.price = parseFloat(item.price.replace(',', '.'));
        });
    } catch (error) {
        console.error("Erreur lors du parsing des données de prix:", error);
        console.error("Message d'erreur:", error.message);
        return;
    }

    allPriceData.forEach(item => {
        item.date = new Date(item.year, item.month - 1, item.day);
    });

    allPriceData.sort((a, b) => a.date - b.date);

    if (allPriceData.length > 0) {
        console.log("Premier prix:", allPriceData[0]);
        console.log("Dernier prix:", allPriceData[allPriceData.length - 1]);
    }

    const chartCanvas = document.getElementById('myChart');

    if (!chartCanvas) {
        console.error("L'élément canvas pour le graphique n'a pas été trouvé");
        return;
    }

    const ctx = chartCanvas.getContext('2d');

    let priceChart = null;

    function filterDataByPeriod(period) {
        const now = new Date();
        let startDate;

        switch (period) {
            case 'month':
                startDate = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
                break;
            case '3months':
                startDate = new Date(now.getFullYear(), now.getMonth() - 3, now.getDate());
                break;
            case '6months':
                startDate = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate());
                break;
            case 'year':
                startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
                break;
            default: // 'all'
                return allPriceData;
        }

        return allPriceData.filter(item => item.date >= startDate);
    }

    function updateStats(filteredData) {
        const minPriceElement = document.getElementById('minPrice');
        const maxPriceElement = document.getElementById('maxPrice');
        const avgPriceElement = document.getElementById('avgPrice');
        const noDataMessageElement = document.getElementById('noDataMessage');

        if (!minPriceElement || !maxPriceElement || !avgPriceElement) {
            console.warn("Certains éléments d'affichage des statistiques n'ont pas été trouvés");
            return;
        }

        if (filteredData.length > 0) {
            const prices = filteredData.map(item => item.price);
            const minPrice = Math.min(...prices);
            const maxPrice = Math.max(...prices);
            const avgPrice = prices.reduce((sum, price) => sum + price, 0) / prices.length;

            minPriceElement.textContent = minPrice.toFixed(2) + ' €';
            maxPriceElement.textContent = maxPrice.toFixed(2) + ' €';
            avgPriceElement.textContent = avgPrice.toFixed(2) + ' €';

            if (noDataMessageElement) {
                noDataMessageElement.classList.add('hidden');
            }
        } else {
            minPriceElement.textContent = '--';
            maxPriceElement.textContent = '--';
            avgPriceElement.textContent = '--';

            if (noDataMessageElement) {
                noDataMessageElement.classList.remove('hidden');
                noDataMessageElement.classList.remove('block');
            }
        }
    }

    function updateChart(period) {
        const filteredData = filterDataByPeriod(period);
        updateStats(filteredData);

        // Si le graphique existe déjà, le détruire
        if (priceChart) {
            priceChart.destroy();
        }

        if (filteredData.length === 0) {
            return;
        }

        const labels = filteredData.map(item => item.formattedDate);
        const prices = filteredData.map(item => item.price);

        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Prix (€)',
                    data: prices,
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(59, 130, 246)',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.raw.toFixed(2) + ' €';
                            },
                            title: function(tooltipItems) {
                                return 'Date: ' + tooltipItems[0].label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Prix (€)'
                        },
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(2) + ' €';
                            }
                        }
                    }
                }
            }
        });
    }

    const periodSelector = document.getElementById('periodSelector');
    if (periodSelector) {
        periodSelector.addEventListener('change', function(e) {
            updateChart(e.target.value);
        });
    } else {
        console.warn("Le sélecteur de période n'a pas été trouvé");
    }
    updateChart('6months');
});