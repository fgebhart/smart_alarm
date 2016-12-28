$(function() { 
    $(window).load(function() {
        loadDoc();
    });

    //---------------------------------------------------
    // Read XML File
    //---------------------------------------------------
    function loadDoc(){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          readXmlFile(this);
        }
      };
      xhttp.open("GET", "./data.xml", true);
      xhttp.send();
    };

    function readXmlFile(xml) {
        console.log( xml );
        var xmlDoc = xml.responseXML;
        //var x = xmlDoc.getElementsByTagName("data");
        var content = xmlDoc.getElementsByTagName('content')[0].childNodes[0].nodeValue;
        var content_stream_url = xmlDoc.getElementsByTagName('content_stream_url')[0].childNodes[0].nodeValue;
        var content_podcast_url = xmlDoc.getElementsByTagName('content_podcast_url')[0].childNodes[0].nodeValue;
        var volume = xmlDoc.getElementsByTagName('volume')[0].childNodes[0].nodeValue;
        var alarm_time = xmlDoc.getElementsByTagName('alarm_time')[0].childNodes[0].nodeValue;
        var days = xmlDoc.getElementsByTagName('days')[0].childNodes[0].nodeValue;
        var alarm_active = xmlDoc.getElementsByTagName('alarm_active')[0].childNodes[0].nodeValue;
        var individual_message = xmlDoc.getElementsByTagName('individual_message')[0].childNodes[0].nodeValue;
        var individual_message_text = xmlDoc.getElementsByTagName('text')[0].childNodes[0].nodeValue;
        
        var alarm_active = (alarm_active == "1"); //convert to bool
        var individual_message = (individual_message == "1"); //convert to bool
        var days_array = days.split(",");
        var hour_value = alarm_time.substr(0, alarm_time.indexOf(':'));
        var minute_value = alarm_time.substr(alarm_time.indexOf(':')+1, 2);
                
        // set values
        $("#slider").slider("option", "value", volume); 

        $('#hour_knob').val(hour_value).trigger('change');   
        //$('#hour_knob').change(hour_value);
        $('#minute_knob').val(minute_value).trigger('change');
                
        $('#cb_alarm_active').prop("checked", alarm_active);
        $("#cb_alarm_active").change(); // to set the elements of class "hide" visible or not
        
        $("#sm_content").val(content).prop('selected', true);
        $("#sm_content").selectmenu( "refresh" ); //refreshes the button
        $("#sm_content").selectmenu('option', 'change').call($("#sm_content")); //call change trigger manually
        $("#txt_content_podcast_url").val(content_podcast_url);
        $("#txt_content_stream_url").val(content_stream_url);
        
        $("#cb_individual_message").prop("checked", individual_message);
        $("#cb_individual_message").change();
        $("#txt_individual_message").val(individual_message_text);
        
        $('.cb_days').each(function () {
            var value = $(this).val();
            if(days_array.indexOf(String(value)) != -1)
            {
                $(this).prop("checked", true);
            }   
        });
        $(".cb_days").button("refresh"); 
        
    };
    
    //---------------------------------------------------
    // Clock
    //---------------------------------------------------
    // Create two variable with the names of the months and days in an array
    var monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]; 
    var dayNames= ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    // Create a newDate() object
    var newDate = new Date();
    // Extract the current date from Date object
    newDate.setDate(newDate.getDate());
    // Output the day, date, month and year    
    $('#time_date').html(dayNames[newDate.getDay()] + " " + newDate.getDate() + ' ' + monthNames[newDate.getMonth()] + ' ' + newDate.getFullYear());

    setInterval( function() {
        // Create a newDate() object and extract the seconds of the current time on the visitor's
        var seconds = new Date().getSeconds();
        // Add a leading zero to seconds value
        $("#time_sec").html(( seconds < 10 ? "0" : "" ) + seconds);
        },1000);

    setInterval( function() {
        // Create a newDate() object and extract the minutes of the current time on the visitor's
        var minutes = new Date().getMinutes();
        // Add a leading zero to the minutes value
        $("#time_min").html(( minutes < 10 ? "0" : "" ) + minutes);
        },1000);

    setInterval( function() {
        // Create a newDate() object and extract the hours of the current time on the visitor's
        var hours = new Date().getHours();
        // Add a leading zero to the hours value
        $("#time_hours").html(( hours < 10 ? "0" : "" ) + hours);
        }, 1000);
        
    //---------------------------------------------------
    // Checkboxes
    //---------------------------------------------------
    $( "input[type='checkbox']" ).checkboxradio(); //use jquery ui
    $( "input[type='button']" ).button(); //use jquery ui
    
    $('#cb_alarm_active').change(function() {
        var value;
        if($(this).is(":checked")) 
        {
            value = 1;
            $(".class_hide").show("slow");
        }
        else
        {
            value = 0;
            $(".class_hide").hide("slow");
        }
        
        $.post("index.html",
        {
          alarm_active: value,
        });    
    });
    
    $('.cb_days').change(function() {
        
        var sList = "";
        $('.cb_days').each(function () {
            sList += $(this).is(":checked") ? $(this).val() + "," : "";
        });
        
        if(sList.length >0)
        {
            sList = sList.substr(0, sList.length-1)
        }
        
        $.post("index.html",
        {
          days: sList,
        });    
    });
    
    $('#cb_individual_message').change(function() {
        var value;
        if($(this).is(":checked")) 
        {
            value = 1;
            $("#txt_individual_message").show("fast");
        }
        else
        {
            value = 0;
            $("#txt_individual_message").hide("fast");
        }
        
        $.post("index.html",
        {
          individual_message: value,
        });    
    });
    
    
    //---------------------------------------------------
    // Knob functions
    //---------------------------------------------------    
    $(".knob").knob({
        change : function (value) {
             console.log("change : " + value);
            var type = this.$[0].id;
            value = String(Math.round(value));
            if(value.length == 1)
            {
                value = '0' + value;
            }
            if (type == 'hour_knob')
            {
                $("#hour_text").text(value)
            } else if (type == 'minute_knob')
            {
                $("#minute_text").text(value)
            }
        },
        release : function (value) {
            var type = this.$[0].id;
            value = String(value);
            
            if(value.length == 1)
            {
                value = '0' + value;
            }

            if (type == 'hour_knob')
            {
                $("#hour_text").text(value)
                value = value + ':' + $("#minute_text").text();
            } else if (type == 'minute_knob')
            {
                $("#minute_text").text(value)
                value = $("#hour_text").text() + ':' + value;
            }

            console.log("new alarm time: " + value);
            $.post("index.html",
            {
              alarm_time: value,
            });  
            
        },
        cancel : function () {
            //console.log("cancel : ", this);
        },
        /*format : function (value) {
            return value + '%';
        },*/
        draw : function () {

            // "tron" case
            if(this.$.data('skin') == 'tron') {

                this.cursorExt = 0.3;

                var a = this.arc(this.cv)  // Arc
                    , pa                   // Previous arc
                    , r = 1;

                this.g.lineWidth = this.lineWidth;

                if (this.o.displayPrevious) {
                    pa = this.arc(this.v);
                    this.g.beginPath();
                    this.g.strokeStyle = this.pColor;
                    this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, pa.s, pa.e, pa.d);
                    this.g.stroke();
                }

                this.g.beginPath();
                this.g.strokeStyle = r ? this.o.fgColor : this.fgColor ;
                this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, a.s, a.e, a.d);
                this.g.stroke();

                this.g.lineWidth = 2;
                this.g.beginPath();
                this.g.strokeStyle = this.o.fgColor;
                this.g.arc( this.xy, this.xy, this.radius - this.lineWidth + 1 + this.lineWidth * 2 / 3, 0, 2 * Math.PI, false);
                this.g.stroke();

                return false;
            }
        },
    });

    
    //---------------------------------------------------
    // Slider
    //---------------------------------------------------
    $( "#slider" ).slider({
        max: 100,
        min: 0,
        animate: "fast",

        change: function (event, ui )
        {
            //save new value
            console.log("volume value : " + ui.value);
            $("#volume_text").text(ui.value);
            $.post("index.html",
                {
                  volume: ui.value,
                });
        },
        
        slide : function (event, ui)
        {
            //refresh the text 
            $("#volume_text").text(ui.value);
        }
    });
      
    //---------------------------------------------------
    // content selection
    //---------------------------------------------------
    $( ".selectmenu" ).selectmenu({
        select: function( event, ui ) {
            //save in xml file
            console.log("selected content selected : " + ui.item.value)
            $.post("index.html",
                {
                  content: ui.item.value,
                });
        },
        
        change: function( event, ui ) {
            $( ".content_options" ).hide();
            var sel_content = $("#sm_content")[0].value;
            if(sel_content == "mp3")
            {
                $("#content_mp3_list").show();       
            }
            else if (sel_content == "podcast")
            {
                $("#content_podcast_url").show();      
            }
            else if (sel_content == "stream")
            {
                $("#content_stream_url").show();   
            }
        }
    });
    
    //---------------------------------------------------
    // text fields
    //---------------------------------------------------
    $(".class_input_text").focusout(function(){
        console.log("Textfeld " + this.id + "changed to: \"" + this.value + "\"");
        
        if(this.id == "txt_individual_message")
        {
            $.post("index.html",
                {
                  text: this.value,
                });
        } 
        if(this.id == "txt_content_stream_url")
        {
            $.post("index.html",
                {
                  content_stream_url: this.value,
                });
        }
        else if(this.id == "txt_content_podcast_url")
        {
            $.post("index.html",
                {
                  content_podcast_url: this.value,
                });
        }
    });
    
    //---------------------------------------------------
    // list box
    //---------------------------------------------------
    $('select#planets').listbox();
}); 
       