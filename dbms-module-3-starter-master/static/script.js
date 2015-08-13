function onForm(event) {
    var data = $(event.target).serializeArray();
    var thesis = {}

    for (var i = 0; i <= data.length; i++) {
      thesis[data[i].name] = data[i].value;
    }

    var thesis_api = '/api/thesis';
    $.post(thesis_api, thesis, function(response) {
      if (response.status = 'OK') {
        var list_element = response.data.thesis_year + ' ' + response.data.thesis_title
        $('.thesis_list').prepend('<li>' + list_element + '</li>');
        //$('.field').val(''); //clear fields
      } else {
        alert('Something went wrong');
      }
    });

    return false;
  }

    // your code here

$('.thesis-entry').submit(onForm);
