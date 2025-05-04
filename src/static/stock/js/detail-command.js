document.addEventListener('DOMContentLoaded', function(){
    const listCard = document.querySelectorAll('#card-command');

    listCard.forEach(card => {
      const detailCard = card.querySelector('.detail-card');
      if (detailCard) {
          card.addEventListener('click', function() {
              detailCard.classList.toggle('hidden');
          });
      }
    })
})