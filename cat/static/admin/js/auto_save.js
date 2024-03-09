//var inputs = document.querySelectorAll('td.field-x_code input[type="number"]');

document.addEventListener("DOMContentLoaded", function() {
    // Находим кнопку по классу и значению
    var saveButton = document.querySelector('.default');
    var inputs = document.querySelectorAll('td.field-x_code input[type="number"]');
    var inputsMin = document.querySelectorAll('td.field-min_price input[type="number"]');

    function handleInputBlur() {
    // Нажимаем кнопку сохранения
    if (saveButton) {
    saveButton.click();
    console.log("Сохранили");
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

  });
