$(document).ready(function () {
    var table = $('#tabla-bitacoras').DataTable({
        serverSide: true,
        processing: true,
        responsive: true,
        ajax: {
            url: "/admin-panel/ajax/",
            data: function (d) {
                d.fecha = $('#filter-fecha').val();
                d.ubicacion = $('#filter-ubicacion').val();
                d.responsable = $('#filter-responsable').val();
                d.tipo = $('#filter-tipo').val();
            },
            dataSrc: function (json) {
                $('#total-internos').text(json.totales.internos);
                $('#total-externos').text(json.totales.externos);
                $('#total-general').text(json.totales.general);
                return json.data;
            }
        },
        columns: [
            { data: "id" },
            { 
                data: "externo",
                render: function (data) {
                    return data 
                        ? '<span class="badge bg-info">Externo</span>'
                        : '<span class="badge bg-success">Interno</span>';
                }
            },
            { data: "fecha" },
            { data: "hora_entrada" },
            { data: "hora_salida" },
            { data: "nombre_visitante" },
            { data: "responsable" },
            { data: "ubicacion" },
            { data: "motivo_visita" },
            { data: "observaciones" }
        ],
        order: [[0, 'desc']],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        dom: '<"row mb-3"<"col-md-6"l><"col-md-6 d-flex justify-content-md-end gap-2"fB>>rt<"d-flex justify-content-between"ip>',
        buttons: [
            {
                extend: 'pdfHtml5',
                text: '<i class="fa fa-file-pdf me-2"></i> PDF',
                className: 'btn btn-danger btn-sm btn-pdf',
                orientation: 'landscape'
            }
        ]
    });

    $('#filter-fecha, #filter-ubicacion, #filter-responsable, #filter-tipo').on('change', function () {
        table.ajax.reload();
    });

    $('#limpiar-filtros').on('click', function (e) {
        e.preventDefault();
        $('#filter-fecha').val('');
        $('#filter-ubicacion').val('');
        $('#filter-responsable').val('');
        $('#filter-tipo').val('');
        table.ajax.reload();
    });
});
