document.addEventListener('DOMContentLoaded', function() {
    const productsList = JSON.parse(document.getElementById('products-list').textContent);

    let lineCounter = 1;

    // Fonction pour ajouter une nouvelle ligne de produit
    document.getElementById('addProductLine').addEventListener('click', function() {
        const productLines = document.getElementById('productLines');
        const newLine = document.createElement('div');
        newLine.className = 'product-line grid grid-cols-5 gap-2';

        // Construction du HTML des options à partir de productsList
        let optionsHtml = '';
        for (let product of productsList) {
            optionsHtml += `<option value="${product.id}">${product.name}</option>`;
        }

        newLine.innerHTML = `
            <div class="col-span-2">
                <label for="product_${lineCounter}">Produit :</label>
                <select name="products[]" id="product_${lineCounter}" class="form-control w-full">
                    ${optionsHtml}
                </select>
            </div>
            <div class="col-span-2">
                <label for="quantity_${lineCounter}">Quantité :</label>
                <input type="number" name="quantities[]" id="quantity_${lineCounter}" class="form-control w-full" value="1" min="1">
            </div>
            <div class="col-span-1 flex items-end">
                <button type="button" class="btn btn-danger remove-line">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
        `;

        productLines.appendChild(newLine);
        lineCounter++;

        // Afficher le bouton de suppression sur la première ligne
        const firstLineRemoveBtn = document.querySelector('#productLines .product-line:first-child .remove-line');
        if (firstLineRemoveBtn) {
            firstLineRemoveBtn.style.display = 'block';
        }

        // Ajouter l'événement de suppression aux boutons
        attachRemoveEvents();
    });

    // Fonction pour attacher les événements de suppression
    function attachRemoveEvents() {
        document.querySelectorAll('.remove-line').forEach(button => {
            button.addEventListener('click', function() {
                const productLines = document.getElementById('productLines');
                if (productLines.children.length > 1) {
                    this.closest('.product-line').remove();

                    // Si après suppression il ne reste qu'une ligne, masquer son bouton de suppression
                    if (productLines.children.length === 1) {
                        const lastRemoveBtn = document.querySelector('#productLines .product-line:first-child .remove-line');
                        if (lastRemoveBtn) {
                            lastRemoveBtn.style.display = 'none';
                        }
                    }
                }
            });
        });
    }

    // Initialisation des événements
    attachRemoveEvents();
});