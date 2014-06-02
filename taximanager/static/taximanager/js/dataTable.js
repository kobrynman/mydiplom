    $(document).ready(function() {
        $('#example').dataTable( {

            "language":
            {
                "emptyTable":     "Дані відсутні в таблиці",
                "info":           "Відображено _START_ - _END_  з _TOTAL_ записів",
                "infoEmpty":      "Відображено 0 - 0 з 0 записів",
                "infoFiltered":   "(filtered from _MAX_ total entries)",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Кількість записів на сторінці: _MENU_ ",
                "loadingRecords": "Загрузка...",
                "processing":     "Обробка...",
                "search":         "Пошук:",
                "zeroRecords":    "Не знайдено жодного запису",
                "paginate": {
                    "first":      "Перша",
                    "last":       "Остання",
                    "next":       "Наступна",
                    "previous":   "Попередня"
                },
                "aria": {
                    "sortAscending":  ": activate to sort column ascending",
                    "sortDescending": ": activate to sort column descending"
                    }
            },
            "order": [ 0, "dec" ]
        } );
    } );