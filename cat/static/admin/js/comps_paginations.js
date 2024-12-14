document.addEventListener("DOMContentLoaded", function() {
    var paginator = document.querySelector('.paginator');
    var form = document.getElementById('changelist-form');

    var paginatorClone = paginator.cloneNode(true);
    // Вставляем скопированный paginator в начало формы
    form.insertBefore(paginatorClone, form.firstChild);
  });
