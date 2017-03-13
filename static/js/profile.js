$(function() {

    $(".member-remove").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });
});

$(function() {
    
    $(".allow-checks").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#allow-checks-email").val($this.data("email"));
        $('#allow-checks-modal').modal("show");

        return false;
    });


    
});