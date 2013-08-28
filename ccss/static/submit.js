$(document).ready(function(){
  css_file = document.getElementById('filename').value
  $('form').submit(function(){
      $.post($(this).attr('action'), $(this).serialize(), function(css){
          $.ajax({type: "POST", url: '/',});
          $('form').hide();
          $('pre').text(css);
          $('pre').css('display', 'block');
          $('a#css-link').css('display', 'block');
		      $("a[href='compressed.css']").attr('href', '/get/' + css_file) // !!
      });
      return false; // Prevent default action
  });
  $("input[type=submit]").attr('disabled', false); // Enable the submit button
});
