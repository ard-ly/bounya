// Copyright (c) 2024, ARD Company and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stop Deducting Loan', {
	refresh: function(frm) {
		frm.set_query("loan", function () {
			return {
			  filters: [
				["Loan", 'docstatus', '=', 1 ],
				
			  ],
			};
		  });

		//   if (frm.doc.docstatus != 1) {
		// 	frm.add_custom_button(
		// 	  __("Get Employess"),
		// 	  function () {
		// 		frappe.model.open_mapped_doc({
		// 		  method: "",
		// 		  frm: frm,
		// 		});
		// 	  },
		// 	);
		//   }
	  

	},

	get_employees(frm) {
		frappe.call({
			method :"get_employees",
			doc:frm.doc,
			args: {
				start_date : frm.doc.start_date,
				end_date: frm.doc.end_date,
			},
			callback:function(r){
				if(r.message){
					console.log("aaaaaaaaaaaaaaaaaaaaaaaaa");
					console.log(r.message.loans_dict);
					for (const [key, value] in r.message.loans_dict) {
						console.log(key, value);
						console.log((r.message.loans_dict).get(key));
					  }
					// r.message.forEach(function (element) {
					// 	console.log("a");
					// 	console.log(element);
						
					// })
					// console.log(r.message.object);
					// for (let i = 1; i <= (r.message).length; i++) {
					// 	console.log(r.message[i][3]);
					// };
					
					// for (let i = 1; i <= 3; i++){
					// 	console.log("a")
					// }
					
				}
			}
		});
	},
});

