function onForm(event){
  var data = $(event.target).serializeArray();

  var student = {};
  for (var i = 0; i < data.length; i++) {
    student[data[i].name] = data[i].value;
  }

  var list_element = $('<li id="item" ' + 'class="' + student.first_name + student.last_name + '">');
  var item = list_element.html(student.first_name + ' ' + student.last_name + ', ' + student.age + '<a href="#" class="delete">  Delete</a>');

  if($('ul.student_list li').hasClass(student.first_name + student.last_name)){
    alert("exists");
  } else {
    $('.student_list').prepend(item);
    $('.field').val(''); //clear fields

  }

  return false;
}

$('.student-form').submit(onForm);
$(document).on('click', '.delete', function() {
  $(this).closest('li').remove();
})
