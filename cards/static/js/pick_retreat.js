$(document).ready(function () {
    $('#turnus').hide();
    $('#turnus_label').hide();

    $('#youth_stays').hide();
    $('#youth_stays_label').hide();

    $('#family_stays').hide();
    $('#family_stays_label').hide();

    $('#next').prop('disabled', true);

    $('.inputs').click(function () {
        var turnus = document.getElementById("turnus").value;
        var categories = document.getElementById("categories").value;
        var youthStays = document.getElementById("youth_stays").value;
        var familyStays = document.getElementById("family_stays").value;

        if (categories !== '') {
            $('#turnus').show();
            $('#turnus_label').show();
        }

        if (turnus !== '') {
            if (categories === 'youth_oases') {
                filterStays('youth_stays', turnus);

                $('#youth_stays').show();
                $('#youth_stays_label').show();

                $('#family_stays').hide();
                $('#family_stays_label').hide();

                disableUnusedFormAndTurnOnButton(categories)
            } else if (categories === 'family_oases') {
                filterStays('family_stays', turnus);

                $('#family_stays').show();
                $('#family_stays_label').show();

                $('#youth_stays').hide();
                $('#youth_stays_label').hide();
                disableUnusedFormAndTurnOnButton(categories)
            }
        }
    });

    function disableUnusedFormAndTurnOnButton(category) {
        if (category === 'youth_oases') {
            $('#next').prop('disabled', false);
            document.getElementById("youth_stays").disabled = false;
            document.getElementById("family_stays").disabled = true;
        } else if (category === 'family_oases') {
            $('#next').prop('disabled', false);
            document.getElementById("youth_stays").disabled = true;
            document.getElementById("family_stays").disabled = false;
        }
    }

    function filterStays(stayId, turnusId) {
        var stays = document.getElementById(stayId);
        for (var i = 0; i < stays.length; i++) {        
            var val = stays.options[i].value;
            // val can be string with numbers separated by ';', we are interested in the first one (turnusId)
            var valNum = parseInt(val.split(';')[0]);
            var turnusIdNum = parseInt(turnusId);
            // valNum is NaN if val string was empty
            stays.options[i].hidden = (!isNaN(valNum) && valNum !== turnusIdNum);
        }
    }

    $('#turnus').click(function () {
        $("#youth_stays").val("");
        $("#family_stays").val("");
    });
});
