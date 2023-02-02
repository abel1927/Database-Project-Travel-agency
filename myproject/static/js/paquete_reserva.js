
function calcular() {

    var precio = 1;

    $("#id_PrecioPorPersona").each(function() {

        precio *= parseFloat($(this).val());

    });

    $("#id_CantidadParticipantes").each(function() {

        precio *= parseFloat($(this).val());

    });

    //alert(precio);
    const $pf = document.getElementById('id_PF');

    $pf.value = precio;

}

