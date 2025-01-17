//var inputs = document.querySelectorAll('td.field-x_code input[type="number"]');

document.addEventListener("DOMContentLoaded", function() {
    // Находим кнопку по классу и значению
    var changesMade = false; // Флаг для отслеживания несохраненных изменений
    var saveButton = document.querySelector('.default');
    var inputs = document.querySelectorAll('td.field-x_code input[type="number"]');
    var inputsMin = document.querySelectorAll('td.field-min_price input[type="number"]');
    var incomps = document.querySelectorAll('td.field-in_comps input[type="checkbox"]');
    var inauto = document.querySelectorAll('td.field-auto input[type="checkbox"]');

    var paginator = document.querySelector('.paginator');
    var form = document.getElementById('changelist-form');


    var paginatorClone = paginator.cloneNode(true);
    var saveButtonClone = paginatorClone.querySelector('.default');
    // Вставляем скопированный paginator в начало формы
    form.insertBefore(paginatorClone, form.firstChild);

    function handleInputBlur() {
    // Нажимаем кнопку сохранения
    if (saveButton) {
    //saveButton.click();
    //console.log("Сохранили");
    changesMade = true; // Устанавливаем флаг изменений при потере фокуса
    console.log("Есть изменение");
    }}
    if (inputs) {
    inputs.forEach(function(input) {
    input.addEventListener('blur', handleInputBlur);
    });
    }
    if (inputsMin) {
    inputsMin.forEach(function(input) {
    input.addEventListener('blur', handleInputBlur);
    });
    }
    if (incomps) {
    incomps.forEach(function(input) {
    input.addEventListener('blur', handleInputBlur);
    });
    }
    if (inauto) {
    inauto.forEach(function(input) {
    input.addEventListener('blur', handleInputBlur);
    });
    }

    if (saveButton) {
        saveButton.addEventListener('click', function() {
            // Логика сохранения данных
            changesMade = false; // Сбрасываем флаг изменений при сохранении
            console.log("Сохранили");
        });
     }
     if (saveButtonClone) {
         saveButtonClone.addEventListener('click', function() {
             // Логика сохранения данных
             changesMade = false; // Сбрасываем флаг изменений при сохранении
             console.log("Сохранили");
         });
      }

    window.addEventListener('beforeunload', function(event) {
      if (changesMade) {
        var message = 'У вас есть несохраненные изменения. Вы уверены, что хотите покинуть страницу?';
        event.returnValue = message; // Для старых версий браузеров
        console.log("Выходим?");
        return message; // Для современных версий браузеров
      }
    });

  });
