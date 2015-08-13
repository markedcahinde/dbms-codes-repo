function onForm(event){
  var data = $(event.target).serializeArray();

  var thesis = {};
  for (var i = 0; i < data.length; i++) {
    thesis[data[i].name] = data[i].value;
  }

  var thesis_api = '/api/thesis';
  $.post(thesis_api, thesis, function(response) {
    if (response.status = 'OK') {
      var list_element = response.data.year + ' ' + response.data.title;
      $('.thesis_list').prepend('<li>' + list_element + '</li>');
      $('.field').val(''); //clear fields
    } else {
      alert('Something went wrong');
    }
  });
  return false;
}

function loadAll() {
  var thesis_api = '/api/thesis';
  $.get(thesis_api, {}, function(response) {
    console.log('thesis_list', response)
    response.data.forEach(function(thesis) {
      var list_element = thesis.year + ' ' + thesis.title;
      $('.thesis_list').prepend('<li>' + list_element + '</li>');
    });
  });
}

$('.thesis-entry').submit(onForm);
loadAll();
