# from __future__ import unicode_literals
# import frappe
# from frappe.utils import format_datetime
# from datetime import datetime
# import json
# import requests

# from frappe.utils.data import today

# @frappe.whitelist()
# def add_source_lead():
# 	if not frappe.db.exists("Lead Source", "India Mart"):
# 		doc = frappe.get_doc({
# 			"doctype": "Lead Source",
# 			"source_name": "India Mart"
# 		})
# 		doc.insert(ignore_permissions=True)
# 		frappe.msgprint(("Lead Source Added For India Mart"))
# 	else:
# 		frappe.msgprint(("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date, to_date):
# 	try:
# 		india_mart_setting = frappe.get_doc("IndiaMart Setting", "IndiaMart Setting")
# 		if not (india_mart_setting.url and india_mart_setting.mobile_no and india_mart_setting.key):
# 			frappe.throw(("URL, Mobile, Key mandatory for Indiamart API Call. Please set them and try again."))

# 		req = get_request_url(india_mart_setting, from_date, to_date)
# 		frappe.msgprint(str(req))
# 		res = requests.post(url=req)
# 		if res.status_code == 200:
# 			response = json.loads(res.text)
# 			frappe.msgprint(str(response))
# 			if response["CODE"] == 200:
# 				leads_created = []
# 				for lead_data in response['RESPONSE']:
# 					india_mart_id = lead_data["UNIQUE_QUERY_ID"]
# 					frappe.msgprint(str(india_mart_id))
# 					if not frappe.db.exists("Lead", {"india_mart_id": india_mart_id}):
# 						lead = frappe.get_doc({
# 							"doctype": "Lead",
# 							"lead_name": lead_data["SENDER_NAME"],
# 							"email_id": lead_data["SENDER_EMAIL"],
# 							"phone": lead_data["SENDER_MOBILE"],
# 							"requirement": lead_data["SUBJECT"],
# 							"india_mart_id": india_mart_id,
# 							"source": "India Mart",
# 							"city": lead_data["SENDER_CITY"],
# 							"state": lead_data["SENDER_STATE"],
# 							"company_name": lead_data["SENDER_COMPANY"],
# 							"product_name": lead_data["QUERY_PRODUCT_NAME"],
# 							"description": lead_data["QUERY_MESSAGE"],
# 							"mcat_name": lead_data["QUERY_MCAT_NAME"]
# 						}).insert(ignore_permissions = True)
# 						leads_created.append(lead)
# 						frappe.msgprint(str(lead))

# 				if leads_created:
# 					frappe.db.insert_many(leads_created)
# 					count = len(leads_created)
# 					frappe.msgprint(f"{count} Leads Created")
# 			else:
# 				frappe.throw(response["MESSAGE"])
# 		else:
# 			frappe.throw(("Failed to fetch data from IndiaMart API"))

# 	except Exception as e:
# 		frappe.log_error(frappe.get_traceback(), ("India Mart Sync Error"))

# def get_request_url(india_mart_setting, from_date, to_date):
# 	start_time = datetime.strptime(from_date, "%d-%m-%Y").strftime("%d-%B-%Y")
# 	end_time = datetime.strptime(to_date, "%d-%m-%Y").strftime("%d-%B-%Y")
# 	req = f"{india_mart_setting.url}?glusr_mobile={india_mart_setting.mobile_no}&glusr_crm_key={india_mart_setting.key}&start_time={start_time}&end_time={end_time}"
# 	return req

# @frappe.whitelist()
# def cron_sync_lead():
# 	try:
# 		sync_india_mart_lead(format_datetime(today()), format_datetime(today()))
# 	except Exception as e:
# 		frappe.log_error(frappe.get_traceback(), ("India Mart Sync Error"))


from __future__ import unicode_literals
import frappe
from frappe.utils import cint, format_datetime, add_days, today, date_diff, getdate, get_last_day, flt, nowdate
from frappe import msgprint, _
from datetime import datetime
import re 
import json
import traceback
import urllib
from urllib.request import urlopen
import requests

@frappe.whitelist()
def add_source_lead():
	if not frappe.db.exists("Lead Source","India Mart"):
		doc=frappe.get_doc(dict(
			doctype = "Lead Source",
			source_name = "India Mart"
		)).insert(ignore_permissions=True)
		if doc:
			frappe.msgprint(_("Lead Source Added For India Mart"))
	else:
		frappe.msgprint(_("India Mart Lead Source Already Available"))

# @frappe.whitelist()
# def sync_india_mart_lead(from_date,to_date):
# 	try:
# 		india_mart_setting = frappe.get_doc("IndiaMart Setting","IndiaMart Setting")
# 		if (not india_mart_setting.url
# 			or not india_mart_setting.mobile_no
# 			or not india_mart_setting.key):
# 				frappe.throw(
# 					msg=_('URL, Mobile, Key mandatory for Indiamart API Call. Please set them and try again.'),
# 					title=_('Missing Setting Fields')
# 				)
		
# 		req = get_request_url(india_mart_setting, from_date, to_date)
		
# 		res = requests.post(url=req)
# 		if res.text:
# 			count = 0
# 			row =json.loads(res.text)
			
# 			if row["CODE"] == 200:
				
# 				leads_created = []
# 				for i in row['RESPONSE']:
# 					india_mart_id = i["UNIQUE_QUERY_ID"]
# 					if not frappe.db.exists("Lead", {"india_mart_id": india_mart_id}):
# 						lead = frappe.get_doc({
# 							"doctype": "Lead",
# 							"lead_name": i["SENDER_NAME"],
# 							"email_id": i["SENDER_EMAIL"],
# 							"phone": i["SENDER_MOBILE"],
# 							"requirement": i["SUBJECT"],
# 							"india_mart_id": india_mart_id,
# 							"source": "India Mart",
# 							"city":i["SENDER_CITY"],
# 							"state":i["SENDER_STATE"],
# 							"company_name":i["SENDER_COMPANY"],
# 							"product_name":i["QUERY_PRODUCT_NAME"],
# 							"description":i["QUERY_MESSAGE"],
# 							"mcat_name":i["QUERY_MCAT_NAME"]
# 						}).insert(ignore_permissions = True)
# 						leads_created.append(lead)

# 				if leads_created:
# 					frappe.db.insert_many(leads_created)
# 					count = len(leads_created)
# 					frappe.msgprint(f"{count} Leads Created")
# 			else:
# 				frappe.throw(row["MESSAGE"])
			
# 			# if not count == 0:
# 			# 	frappe.msgprint(_("{0} Lead Created").format(count))
			

# 	except Exception as e:
# 		frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

#updated code to sync lead - sukhman

@frappe.whitelist()
def sync_india_mart_lead(from_date,to_date):
    try:
        india_mart_setting = frappe.get_doc("IndiaMart Setting","IndiaMart Setting")
        if (not india_mart_setting.url
            or not india_mart_setting.mobile_no
            or not india_mart_setting.key):
                frappe.throw(
                    msg=_('URL, Mobile, Key mandatory for Indiamart API Call. Please set them and try again.'),
                    title=_('Missing Setting Fields')
                )
        
        req = get_request_url(india_mart_setting, from_date, to_date)
        
        res = requests.post(url=req)
        if res.text:
            count = 0
            skipped = 0
            row = json.loads(res.text)
            
            if row["CODE"] == 200:
                
                leads_created = []
                for i in row['RESPONSE']:
                    india_mart_id = i["UNIQUE_QUERY_ID"]
                    email = i["SENDER_EMAIL"]
                    # Skip if india_mart_id already exists OR email already exists
                    if frappe.db.exists("Lead", {"india_mart_id": india_mart_id}) or (email and frappe.db.exists("Lead", {"email_id": email})):
                        skipped += 1
                        continue
                        
                    phone = i["SENDER_MOBILE"]
                    if phone and phone.startswith("+91-"):
                        phone = phone.replace("+91-", "", 1)
                    elif phone and phone.startswith("+91"):
                        phone = phone.replace("+91", "", 1)
                    elif phone and phone.startswith("91"):
                        phone = phone.replace("91", "", 1)
                    
                    lead = frappe.get_doc({
                        "doctype": "Lead",
                        "lead_name": i["SENDER_NAME"],
                        "email_id": email,
                        "phone": phone,
                        "requirement": i["SUBJECT"],
                        "india_mart_id": india_mart_id,
                        "source": "India Mart",
                        "city": i["SENDER_CITY"],
                        "state": i["SENDER_STATE"],
                        "company_name": i["SENDER_COMPANY"],
                        "product_name": i["QUERY_PRODUCT_NAME"],
                        "description": i["QUERY_MESSAGE"],
                        "mcat_name": i["QUERY_MCAT_NAME"]
                    }).insert(ignore_permissions = True)
                    leads_created.append(lead)
                    
            else:
                frappe.throw(row["MESSAGE"])

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))

def get_request_url(india_mart_setting, from_date, to_date):
		
		start_time = str(datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%b-%Y"))
		end_time = str(datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%b-%Y"))
		

		req = f"{india_mart_setting.url}?glusr_mobile={india_mart_setting.mobile_no}&glusr_crm_key={india_mart_setting.key}&start_time={start_time}&end_time={end_time}"

		return req
    


@frappe.whitelist()
def cron_sync_lead():
	try:
		sync_india_mart_lead(today(),today())
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("India Mart Sync Error"))


# @frappe.whitelist()
# def add_lead():
# 	frappe.msgprint("fgvffg?")
	



