$(document).ready(function () {

    const fs = require('fs');
    let rawdata = fs.readFileSync('test.json');
    let student = JSON.parse(rawdata);
    console.log(student);

    fetch("test.json")
        .then(Response => Response.json())
        .then(data => {
            console.log(data);
            render_comment(data);
        });
    

    render_comment = function(comment) { 
        let target = $("#content"); 
        var $comment = $("<p></p>"); 
        $comment.text(comment.body);
        target.append($comment);
    };


});
