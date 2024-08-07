frappe.ui.form.on("Sales Invoice", "send_to_eta", function(frm) {
    frappe.call({
      method: "ecs_einvoice.ecs_einvoice.sales_invoice.sales_invoice.test",
      args: {
                'name': frm.doc.name
               
			},
      callback: function(r) {
         // console.log();
          }
    });
  });