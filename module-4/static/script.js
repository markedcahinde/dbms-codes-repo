function onForm(event){
  var data = $(event.target).serializeArray();

  var thesis = {};
  for (var i = 0; i < data.length; i++) {
    thesis[data[i].name] = data[i].value;
  }

  var thesis_api = '/api/thesis';
  $.post(thesis_api, thesis, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       var list_element = response.data.year + ' ' + response.data.title
       $('.thesis-list').prepend('<li>' + list_element + ' addded by: ' + response.data.author + '</li>'); // + '<a href="#">Update</a>');
       $('.field').val(''); //clear fields
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

function loadAll() {
  var thesis_list_api = '/api/thesis';
  $.get(thesis_list_api, {}, function(response) {
    response.data.forEach(function(thesis_list) {
      var thesis_item = thesis_list.year + ' ' + thesis_list.title;
      $('.thesis-list').append('<li>' + thesis_item + ' addded by: ' + thesis_list.author + '</li>'); // + '<a href="/edit/' + thesis_list.id + '">Update</a>');
    });
  });
}

loadAll();
$('.thesis-entry').submit(onForm);
