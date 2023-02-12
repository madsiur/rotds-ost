$(document).ready(function() {
    var dirName = dirs[2];
    var array = $.grep(ost_a, function(e) {return e.dir == 3;});    
    listSongTable(array, dirName);

    $('#sortTbl').DataTable({
        "order": [[2, 'asc']],
        "columnDefs": [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 7 },
            { orderable: false, targets: 8 }
        ],
        "paging": false,
        "searching": false,
        "info": false
    });
});