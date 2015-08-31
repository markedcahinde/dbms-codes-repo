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
       $('.thesis-list').prepend('<li>' + list_element + ' by: ' + response.data.author + '</li>'); // + '<a href="#">Update</a>');
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
      thesis_list.author.forEach(function(e) {
        var thesis_auth = e.first_name + ' ' + e.last_name;
        $('.thesis-list').append('<li>' + thesis_item + ' by: ' + thesis_auth + '</li>');
      });
    });
  });
}

function onReg(event)
{
  var data = $(event.target).serializeArray();

  var user = {};
  for (var i = 0; i < data.length; i++) {
    user[data[i].name] = data[i].value;
  }

  var user_api = '/register';
  $.post(user_api, user, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration success');
       window.location.replace("/");
     } else {
       alert('Something went wrong');
     }
  });
  return false;
}

loadAll();
$('.thesis-entry').submit(onForm);
$('.regform').submit(onReg);
