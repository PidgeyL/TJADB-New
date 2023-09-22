function playpreview(ID){
    $("#preview_"+ID).get(0).play();
    $("#play_"+ID).hide();
    $("#stop_"+ID).show();
}

function stoppreview(ID){
    console.log($("#preview_"+ID));
    console.log($("#preview_"+ID).get(0));
    $("#preview_"+ID).get(0).pause();
    $("#play_"+ID).show();
    $("#stop_"+ID).hide();
}

$(document).ready(function () {
    var table = $('#dtSongTable').DataTable({
        "order": [[ 12, "desc" ]],
        "columnDefs": [
            { width: 27, targets: 4 },
            { width: 27, targets: 5 },
            { width: 27, targets: 6 },
            { width: 27, targets: 7 },
            { width: 27, targets: 8 },
            { visible: false, targets: 3 },
            { visible: false, targets: 10 },
            { visible: false, targets: 11 },
            { visible: false, targets: 12 }
        ],
        "autoWidth": false,
        "fixedColumns": true,
        "lengthMenu": [[25, 50, 100, 200, -1], [25, 50, 100, 200, "All"]],
        "pageLength" : 100,
    });
    $('.dataTables_length').addClass('bs-select');

    $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();
        var column = table.column( $(this).attr('data-column') );
        column.visible( ! column.visible() );
    } );

    $('a.toggle-dif').on( 'click', function (e) {
        e.preventDefault();
        var first = $(this).attr('data-column');
        for (let i = first; i < parseInt(first)+5; i++) {
            var column = table.column( i );
            column.visible( ! column.visible() );
        }
    } );

});
