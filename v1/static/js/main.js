$(document).ready(function () {
    // Init
    $('#submitform').hide();
    $('.image-section').hide();
    var slider1 = document.getElementById("slider1");
    var output1 = document.getElementById("demo1");

    var slider2 = document.getElementById("slider2");
    var output2 = document.getElementById("demo2");


function getCheckboxes(){
    var selected = new Array();
    $('#table_result input[type="checkbox"]:checked').each(function() {
        selected.push($(this).attr('id'));
    });
    // console.log(selected);
    var tr = $("#table_result>tbody>tr").filter(function() {

        slider1_value = parseFloat(slider1.value); // SCORE MINIMO
        slider2_value = parseFloat(slider2.value); // N resultados

        var rank = parseFloat($(this).data('rank')); 
        var score = parseFloat($(this).data('score')); 

        if( (score >= slider1_value) && (rank <= slider2_value)){

            $(this).find("input:checkbox").each(function() {
                if($(this).is(':visible')){
                    //console.log("VISIBLE");
                    ;
                }else{
                    //$(this).prop('checked', $(this).prop('checked'));
                    $(this).prop('checked', true );
                }
            });

            $(this).show();
        }else{

            $(this).find("input:checkbox").each(function() {
                if($(this).is(':visible')){
                    ;
                }else{
                    //$(this).prop('checked', $(this).prop('checked'));
                    $(this).prop('checked', false );
                }
            });

            $(this).hide();
        }

    });

}

// Update the current slider value (each time you drag the slider handle)
slider1.oninput = function() {
  //output1.innerHTML = this.value;
  getCheckboxes();

}
// Update the current slider value (each time you drag the slider handle)
slider2.oninput = function() {
  //output2.innerHTML = this.value;
  getCheckboxes();
}

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').fadeIn(650);
                text = reader.result;
                var lines = text.split(/[\r\n]+/g);
                $('#imagePreview').html( '<textarea id="contentPreview" name="contentPreview" cols="50"></textarea>');
                lines.forEach(function(line) { 
                    $('#contentPreview').append( line + "<br />");
                });
            }
            reader.readAsText(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        readURL(this);
        $('.img-preview').show();
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.img-preview').hide();

                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                $('#submitform').show();

    const myObj = JSON.parse(data);
    var jsonData = (eval(myObj))

    let text = "<table border='1' id='table_result'>"
    text += "<thead>";
    text += "<tr>";
    text += "<th>" + "Checkbox" + "</th>";
    text += "<th>" + "Número Entrada" + "</th>";
    text += "<th>" + "Entrada" + "</th>";
    text += "<th>" + "Rank" + "</th>";
    text += "<th>" + "ODS" + "</th>";
    text += "<th>" + "Score" + "</th>";
    text += "</tr>";
    text += "</thead>";
    text += "<tbody>";

    index  = 0
    for (let x in jsonData) {
      text += "<tr data-rank=" + jsonData[x].Rank + " data-score=" + jsonData[x].score + " data-index= " + index + ">";
      text += "<td>" +  '<input type="checkbox" name="check_list" value=' + index + ' id="' + jsonData[x].score +'"  />' +  "</td>";
      text += "<td>" + jsonData[x].n_sentence + "</td>";
      text += "<td>" + jsonData[x].sentence + "</td>";
      text += "<td>" + jsonData[x].Rank + "</td>";
      text += "<td>" + jsonData[x].ODS + "</td>";
      text += "<td>" + jsonData[x].score + "</td>";
      text += "</tr>";
      index += 1 ;
    }
    text += "</tbody>";
    text += "</table>"
    document.getElementById("result").innerHTML = text;
    console.log('Success!');

            },
        });
    });

});
