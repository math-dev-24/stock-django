document.addEventListener('DOMContentLoaded', () => {
    const prevLink = document.getElementById('link-page-prev');
    const nextLink = document.getElementById('link-page-next');
    const filterForm = document.getElementById('filter-form');
    const maxPage = document.getElementById('max_page');

    let max = parseInt(maxPage.value);

    prevLink.addEventListener('click', () => {
        if (parseInt(filterForm.elements.page.value) > 1) {
            const page = filterForm.elements.page.value;
            filterForm.elements.page.value = parseInt(page) - 1;
            filterForm.submit();
        } else {
            generateError('Vous ne pouvez pas vous déplacer en arrière !');
        }
    });

    nextLink.addEventListener('click', () => {
        if (max < parseInt(filterForm.elements.page.value)) {
            const page = filterForm.elements.page.value;
            filterForm.elements.page.value = parseInt(page) + 1;
            filterForm.submit();
        } else {
            generateError('Vous ne pouvez pas allez plus loin !');
        }
    });

    const generateError = (message) => {
        const newElement = document.createElement('div');
        newElement.innerHTML = `<p>${message}</p>`;
        newElement.classList.add('alert', 'alert-danger', 'my-2', 'alert-dismissible', 'fade', 'show', 'relative', 'py-4', 'px-6','rounded-md', 'min-w-[450px]');

        const progressBar = document.createElement('div');
        progressBar.classList.add('progress-bar-3', 'absolute', 'bottom-0', 'left-0', 'progress-bar-danger');
        newElement.appendChild(progressBar);

        const html = document.getElementById('popup');
        html.appendChild(newElement);

        setTimeout(function() {
            newElement.classList.add("hidden");
        }, 6000);

        newElement.addEventListener('click', () => {
            newElement.classList.add("hidden");
        });
    }
})