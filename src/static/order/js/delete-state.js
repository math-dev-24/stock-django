document.addEventListener('DOMContentLoaded', () => {

    const list_delete_btn = document.querySelectorAll('.btn-delete-state');

    list_delete_btn.forEach(btn => {
        btn.addEventListener('click', function() {
            const state_id = this.id.split('-')[2];
            const name = this.getAttribute('content');
            const form = document.getElementById(`delete-state-${state_id}`);

            if (confirm(`Voulez-vous supprimer l'état ${name} ?`)) {
                form.submit();
            }
        })
    });
})
