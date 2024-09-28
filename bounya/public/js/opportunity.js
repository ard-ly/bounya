frappe.ui.form.on('Opportunity', {

    refresh: function (frm) {
        if (frm.doc.custom_towers){
            frm.trigger("custom_towers");
        }
        if(frm.doc.custom_equipment_radius_ == ""){
            frm.set_df_property("custom_equipment_height", "read_only", 0);
        }
        if(frm.doc.custom_equipment_height == ""){
            frm.set_df_property("custom_equipment_radius_", "read_only", 0);
        }
    },

    custom_towers: function (frm) {
        if (frm.doc.custom_equipment_installation == 1){
            frappe.call({
                method :"bounya.api.get_pricing_matrix",
                args: {
                    tower_type: frm.doc.custom_tower_type,
                },
                callback:function(r){
                    if(r.message){
                        console.log(r.message);
                        frm.set_df_property("custom_equipment_radius_", "options", r.message.radius_list);
                        frm.set_df_property("custom_equipment_height", "options", r.message.height_list);
                        frm.refresh_fields();
                    }
                }
            });
        }
    },

    custom_equipment_radius_:function (frm) {
        if (frm.doc.custom_equipment_installation == 1){
            if (frm.doc.custom_equipment_radius_){
                frappe.call({
                    method :"bounya.api.get_price_for_radius",
                    args: {
                        tower_type: frm.doc.custom_tower_type,
                        custom_equipment_radius_:frm.doc.custom_equipment_radius_,
                    },
                    callback:function(r){
                        if(r.message){
                            console.log(r.message);
                            frm.set_df_property("custom_equipment_height", "read_only", 1);
                            if (r.message.height > 0){
                                frm.doc.custom_equipment_height = r.message.height;
                            }
                            if (r.message.price > 0){
                                    var child = frm.add_child('items');
                                    child.rate = r.message.price;
                                    child.amount = r.message.price;
                                    child.base_rate = r.message.price;
                                    child.base_amount = r.message.price;
                            
                                    frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
                                        return {
                                            filters: {
                                                "item_group": "Services",
                                                "is_stock_item": 0,
                                            }
                                        };
                                    };
                            }
                            frm.refresh_fields();
                        }
                    }
                });
            }
        }
    },

    custom_equipment_height:function (frm) {
        if (frm.doc.custom_equipment_installation == 1){
            if (frm.doc.custom_equipment_height){
                frappe.call({
                    method :"bounya.api.get_price_for_height",
                    args: {
                        tower_type: frm.doc.custom_tower_type,
                        custom_equipment_height:frm.doc.custom_equipment_height,
                    },
                    callback:function(r){
                        if(r.message){
                            console.log(r.message);
                            frm.set_df_property("custom_equipment_radius_", "read_only", 1);
                            if (r.message.radius > 0){
                                frm.doc.custom_equipment_radius_ = r.message.radius;
                            }
                            if (r.message.price > 0){
                                    var child = frm.add_child('items');
                                    child.rate = r.message.price;
                                    child.amount = r.message.price;
                                    child.base_rate = r.message.price;
                                    child.base_amount = r.message.price;
                                    
                                    frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
                                        return {
                                            filters: {
                                                "item_group": "Services",
                                                "is_stock_item": 0,
                                            }
                                        };
                                    };
                            }
                            frm.refresh_fields();
                        }
                    }
                });
            }
        }
    },
});

frappe.ui.form.on('Opportunity Item', {
    
    items_add: function(frm, cdt, cdn) {
        if (frm.doc.custom_equipment_installation == 1){
            frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
                return {
                    filters: {
                        "item_group": "Services",
                        "is_stock_item": 0,
                    }
                };
            };
            
            frm.refresh_fields();
        }
    },
});