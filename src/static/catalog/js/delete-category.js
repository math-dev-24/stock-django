document.addEventListener('DOMContentLoaded', () => {

    const list_delete_btn = document.querySelectorAll('.btn-delete-category');

    list_delete_btn.forEach(btn => {
        btn.addEventListener('click', function () {
            const category_id = this.id.split('-')[2];
            const name = this.getAttribute('content');
            const form = document.getElementById(`delete-category-${category_id}`);

            if (confirm(`Voulez-vous supprimer la catégorie ${name} ?`)) {
                form.submit();
            }
        })
    });
})