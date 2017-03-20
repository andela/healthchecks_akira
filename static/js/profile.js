$(function() {
    $(".allowed-checks").click(function() {
        var $this = $(this);
        $("#member-id").val($this.data("member-id"));
        $('#all-checks-list-modal').modal("show");
        return false;
    });

    $(".member-remove").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });

});