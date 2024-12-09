frappe.listview_settings['Outgoing Mail'] = {
    add_fields: ['status'],
    get_indicator: function (doc) {
        if (doc.status) {
            return [doc.status, 'green', 'status,=,' + doc.status];
        }
    }
};