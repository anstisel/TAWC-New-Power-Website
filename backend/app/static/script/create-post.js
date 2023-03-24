$(document).ready(function () {
    $("#post_form").on("submit",function(event){event.preventDefault()});
    
    $("#post_form").submit(function (event) {
        var formData = {
        title: $("#title").val(),
        body: $("#details").val(),
        };
        console.log("Submitting post:")
        console.log(formData)

        $.ajax({
        type: "POST",
        url: "api/v1/post/create-post",
        data: formData,
        dataType: "json",
        encode: true,
        }).done(function (data) {
        console.log(data);
        });

        event.preventDefault();
    });
});