$(function () {

    var MINUTE = {name: "minute", nsecs: 60};
    var HOUR = {name: "hour", nsecs: MINUTE.nsecs * 60};
    var DAY = {name: "day", nsecs: HOUR.nsecs * 24};
    var WEEK = {name: "week", nsecs: DAY.nsecs * 7};
    var UNITS = [WEEK, DAY, HOUR, MINUTE];

    var secsToText = function(total) {
        var remainingSeconds = Math.floor(total);
        var result = "";
        for (var i=0, unit; unit=UNITS[i]; i++) {
            if (unit === WEEK && remainingSeconds % unit.nsecs != 0) {
                // Say "8 days" instead of "1 week 1 day"
                continue
            }

            var count = Math.floor(remainingSeconds / unit.nsecs);
            remainingSeconds = remainingSeconds % unit.nsecs;

            if (count == 1) {
                result += "1 " + unit.name + " ";
            }

            if (count > 1) {
                result += count + " " + unit.name + "s ";
            }
        }

        return result;
    }

    var periodSlider = document.getElementById("period-slider");
    noUiSlider.create(periodSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '5%':[388800,388800],
            '10%':[777600,777600],
            '15%':[1166400,1166400],
            '20%':[1555200,1555200],
            '25%':[1944000,1944000],
            '30%':[2332800,2332800],
            '35%':[2721600,2721600],
            '40%':[3110400,3110400],
            '45%':[3499200,3499200],
            '50%':[3888000,3888000],
            '55%':[4276800,4276800],
            '60%':[4665600,4665600],
            '65%':[5054400,5054400],
            '70%':[5443200,5443200],
            '75%':[5832000,5832000],
            '80%':[6220800,6220800],
            '85%':[6609600,6609600],
            '90%':[6998400,6998400],
            '95%':[7387200,7387200],
            'max':7776000,

        },
        pips: {
            mode: 'values',
            values: [60, 1296000, 2592000, 3888000, 5184000, 5184000, 6480000, 7776000],
            density: 4,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    periodSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#period-slider-value").text(secsToText(rounded));
        $("#update-timeout-timeout").val(rounded);
    });


    var graceSlider = document.getElementById("grace-slider");
    noUiSlider.create(graceSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '5%':[388800,388800],
            '10%':[777600,777600],
            '15%':[1166400,1166400],
            '20%':[1555200,1555200],
            '25%':[1944000,1944000],
            '30%':[2332800,2332800],
            '35%':[2721600,2721600],
            '40%':[3110400,3110400],
            '45%':[3499200,3499200],
            '50%':[3888000,3888000],
            '55%':[4276800,4276800],
            '60%':[4665600,4665600],
            '65%':[5054400,5054400],
            '70%':[5443200,5443200],
            '75%':[5832000,5832000],
            '80%':[6220800,6220800],
            '85%':[6609600,6609600],
            '90%':[6998400,6998400],
            '95%':[7387200,7387200],
            'max':7776000,
        },
        pips: {
            mode: 'values',
            values: [60, 1296000, 2592000, 3888000, 5184000, 5184000, 6480000, 7776000],
            density: 60,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    graceSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#grace-slider-value").text(secsToText(rounded));
        $("#update-timeout-grace").val(rounded);
    });


    $('[data-toggle="tooltip"]').tooltip();

    $(".my-checks-name").click(function() {
        var $this = $(this);

        $("#update-name-form").attr("action", $this.data("url"));
        $("#update-name-input").val($this.data("name"));
        $("#update-tags-input").val($this.data("tags"));
        $('#update-name-modal').modal("show");
        $("#update-name-input").focus();

        return false;
    });

    $(".timeout-grace").click(function() {
        var $this = $(this);

        $("#update-timeout-form").attr("action", $this.data("url"));
        periodSlider.noUiSlider.set($this.data("timeout"))
        graceSlider.noUiSlider.set($this.data("grace"))
        $('#update-timeout-modal').modal({"show":true, "backdrop":"static"});

        return false;
    });

    $(".check-menu-remove").click(function() {
        var $this = $(this);

        $("#remove-check-form").attr("action", $this.data("url"));
        $(".remove-check-name").text($this.data("name"));
        $('#remove-check-modal').modal("show");

        return false;
    });


    $("#my-checks-tags button").click(function() {
        // .active has not been updated yet by bootstrap code,
        // so cannot use it
        $(this).toggleClass('checked');

        // Make a list of currently checked tags:
        var checked = [];
        $("#my-checks-tags button.checked").each(function(index, el) {
            checked.push(el.textContent);
        });

        // No checked tags: show all
        if (checked.length == 0) {
            $("#checks-table tr.checks-row").show();
            $("#checks-list > li").show();
            return;
        }

        function applyFilters(index, element) {
            var tags = $(".my-checks-name", element).data("tags").split(" ");
            for (var i=0, tag; tag=checked[i]; i++) {
                if (tags.indexOf(tag) == -1) {
                    $(element).hide();
                    return;
                }
            }

            $(element).show();
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $("#checks-table tr.checks-row").each(applyFilters);
        // Mobile: for each list item, see if it needs to be shown or hidden
        $("#checks-list > li").each(applyFilters);

    });

    $(".pause-check").click(function(e) {
        var url = e.target.getAttribute("data-url");
        $("#pause-form").attr("action", url).submit();
        return false;
    });


    $(".usage-examples").click(function(e) {
        var a = e.target;
        var url = a.getAttribute("data-url");
        var email = a.getAttribute("data-email");

        $(".ex", "#show-usage-modal").text(url);
        $(".em", "#show-usage-modal").text(email);

        $("#show-usage-modal").modal("show");
        return false;
    });


    var clipboard = new Clipboard('button.copy-link');
    $("button.copy-link").mouseout(function(e) {
        setTimeout(function() {
            e.target.textContent = "copy";
        }, 300);
    })

    clipboard.on('success', function(e) {
        e.trigger.textContent = "copied!";
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        var text = e.trigger.getAttribute("data-clipboard-text");
        prompt("Press Ctrl+C to select:", text)
    });


});
