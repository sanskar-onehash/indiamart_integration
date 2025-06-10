import frappe


def after_install():
    add_custom_fields_to_lead()


def add_custom_fields_to_lead():
    custom_fields = [
        {
            "dt": "Lead",
            "fieldname": "requirement",
            "fieldtype": "Small Text",
            "insert_after": "dashboard_tab",
            "label": "Requirement",
            "module": "Indiamart Integration",
            "name": "Lead-requirement",
        },
        {
            "dt": "Lead",
            "fieldname": "india_mart_id",
            "fieldtype": "Data",
            "insert_after": "requirement",
            "label": "India Mart ID",
            "module": "Indiamart Integration",
            "name": "Lead-india_mart_id",
        },
        {
            "dt": "Lead",
            "fieldname": "product_enquiry",
            "fieldtype": "Section Break",
            "insert_after": "india_mart_id",
            "label": "Product Enquiry",
            "module": "Indiamart Integration",
            "name": "Lead-product_enquiry",
        },
        {
            "dt": "Lead",
            "fieldname": "product_name",
            "fieldtype": "Data",
            "insert_after": "product_enquiry",
            "label": "Product Name",
            "module": "Indiamart Integration",
            "name": "Lead-product_name",
        },
        {
            "dt": "Lead",
            "fieldname": "description",
            "fieldtype": "Small Text",
            "insert_after": "product_name",
            "label": "Description",
            "module": "Indiamart Integration",
            "name": "Lead-description",
        },
        {
            "dt": "Lead",
            "fieldname": "mcat_name",
            "fieldtype": "Data",
            "insert_after": "description",
            "label": "MCAT Name",
            "module": "Indiamart Integration",
            "name": "Lead-mcat_name",
        },
    ]

    for field in custom_fields:
        if not frappe.db.exists(
            "Custom Field", {"dt": "Lead", "fieldname": field["fieldname"]}
        ):
            new_field = frappe.get_doc({"doctype": "Custom Field", **field})
            new_field.insert()
            frappe.db.commit()
