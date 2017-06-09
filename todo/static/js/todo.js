

  $(".switch-input").click(function(event) {
      var csrftoken = getCookie('csrftoken');
      $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
        });
        var callurl = $(this).attr("data-href");
        var this_=$(this).parent().parent().parent();
        var control=$(this);
        var doneflag=this.checked;
          $.ajax({
            url: callurl,
            type: 'PATCH',
            data: {'id':  control.attr("data-id") ,"Done": doneflag},
            success: function(data){
              if(doneflag==true)
                this_.children("small").html(data.Completed.toString());
              this_.toggleClass('callout-done');
              setTimeout(function(){
                if(this_.hasClass('callout-done')){
                  this_.next().remove();
                  this_.remove();
                }
              },5000);
            },
            failure: function(error){
              console.log(error);
            }
          });
    });

    $(".todo-filters").click(function(event) {
      console.log("res");
      sendUrl=$("#todolist").attr("data-href");
      option=$(this).attr("data-href-option");
      if(option==undefined)
          option="active"; // all, active, completed
      $.ajax({
        url: sendUrl,
        data: {"option":option},
        success: function( data ) {
          $(".aside-menu").html(data);
        }
      });
    });
