
function initialice_tp(){
    // Setup - add a text input to each footer cell
    $('#tabla_principal tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder=" '+title+'" />' );
    } );
    // DataTable
    var table = $('#tabla_principal').DataTable({
        scrollY:        '50vh',
        scrollCollapse: true,
        paging:         false,
        initComplete: function () {
            // Apply the search
            this.api().columns().every( function () {
                var that = this;

                $( 'input', this.footer() ).on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                } );
            } );
        }
    });
}


$(document).ready(function() {
    initialice_tp();
} );