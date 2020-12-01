/* global aaSrpSettings, moment */

$(document).ready(function() {
    /**
     * Table :: SRP Requests
     */
    var srpRequestsTable = $('#tab_aasrp_srp_requests').DataTable({
        ajax: {
            url: aaSrpSettings.url.requestsForSrpLink,
            dataSrc: '',
            cache: false
        },
        columns: [
            {
                data: 'request_time',
                render: $.fn.dataTable.render.moment(
                    moment.ISO_8601,
                    aaSrpSettings.datetimeFormat
                )
            },
            {data: 'requester'},
            {data: 'character'},
            {data: 'request_code'},
            {data: 'ship'},
            {data: 'zkb_link'},
            {
                data: 'zbk_loss_amount',
                render: function(data, type, row, meta) {
                    if(type === 'display'){
                        var currency = 'ISK';
                        var iskValue = $.fn.dataTable.render.number(
                            ',',
                            '.'
                        ).display(data);

                        return iskValue + ' ' + currency;
                    } else {
                        return data;
                    }
                },
                className: 'text-right'
            },
            {
                data: 'payout_amount',
                render: function(data, type, row, meta) {
                    if(type === 'display'){
                        var currency = 'ISK';
                        var iskValue = $.fn.dataTable.render.number(
                            ',',
                            '.'
                        ).display(data);

                        return iskValue + ' ' + currency;
                    } else {
                        return data;
                    }
                },
                className: 'text-right'
            },
        ],
        order: [[0, 'desc']]
    });

    srpRequestsTable.rows().every(function() {
        var d = this.data();

        d['zbk_loss_amount'] = d['zbk_loss_amount']  + 'ISK';
        d['payout_amount'] = d['payout_amount']  + 'ISK';

        srpRequestsTable.row(this).data(d);
    });
});