from collections import defaultdict

payment = "payment-001, 1000, Paying off: inv-123 something, "
invoices = [
    "inv-123, 2024-03-15, 1000",
    "inv-456, 2024-03-20, 1000",
    "inv-789, 2024-02-10, 500"
]


#"paying for: invoice-id" or "Paying off: invoice-id"


INVOICE_TERM_1 = "paying for: "
INVOICE_TERM_2 = "paying off: "
def reconcile_payment(payment, invoices):
    invoice_details = defaultdict(tuple)
    for invoice in invoices:
        invoice_id, date, amount = invoice.split(", ")
        invoice_details[invoice_id.lower()] = (date, int(amount))

    parts = payment.split(", ")
    payment_id = parts[0]
    payment_amount = int(parts[1])
    payment_note = ", ".join(parts[2:]).lower()

    found_invoice_id = ""
    if INVOICE_TERM_1 in payment_note:
        index = payment_note.index(INVOICE_TERM_1)
        end_index  = index+len(INVOICE_TERM_1)
        found_invoice_id = payment_note[end_index:].lower().strip()
    elif INVOICE_TERM_2 in payment_note:
        index = payment_note.index(INVOICE_TERM_2)
        end_index  = index+len(INVOICE_TERM_2)
        found_invoice_id = payment_note[end_index:].lower().strip()

    if found_invoice_id and found_invoice_id in invoice_details:
        print(
            f"Payment {payment_id} paid {payment_amount} for invoice {found_invoice_id} "
            f"due on {invoice_details[found_invoice_id][0]}"
        )
    else:
        print(f"Payment {payment_id} could not be matched to any invoice")
reconcile_payment(payment, invoices)


#part 2 match by amount if match by id is not successful and if there are multiple invoice_ids with same amount, return the one with earliest date.


def reconcile_payment(payment, invoices, forgiveness):
    invoice_details = defaultdict(tuple)
    for invoice in invoices:
        invoice_id, date, amount = invoice.split(", ")
        invoice_details[invoice_id.lower()] = (date, int(amount))

    parts = payment.split(",")
    payment_id = parts[0]
    payment_amount = int(parts[1])
    payment_note = ", ".join(parts[2:]).lower()

    found_invoice_id = ""
    if INVOICE_TERM_1 in payment_note:
        index = payment_note.index(INVOICE_TERM_1)
        end_index  = index+len(INVOICE_TERM_1)
        found_invoice_id = payment_note[end_index:].lower()
    elif INVOICE_TERM_2 in payment_note:
        index = payment_note.index(INVOICE_TERM_2)
        end_index  = index+len(INVOICE_TERM_2)
        found_invoice_id = payment_note[end_index:].lower()

    if not found_invoice_id or found_invoice_id not in invoice_details:
        sorted_by_date = []
        for invoice_id, details in invoice_details.items():
            sorted_by_date.append((invoice_id, details[0], details[1]))
            sorted_by_date.sort(key = lambda x: x[1])
        for invoice_id, date, amount in sorted_by_date:
            if amount == payment_amount:
                found_invoice_id = invoice_id
                break
        if not found_invoice_id:
            for invoice_id, date, amount in sorted_by_date:
                if abs(amount-payment_amount)<=forgiveness:
                    found_invoice_id = invoice_id
                    break
    print(
        f"Payment {payment_id} paid {payment_amount} for invoice {found_invoice_id} "
        f"due on {invoice_details[found_invoice_id][0]}"
    )

# payment = "payment-002, 500, Monthly subscription"
#
# invoices = [
#     "inv-001, 2024-03-22, 1000",
#     "inv-002, 2024-02-05, 500",
#     "inv-003, 2024-03-01, 500",
#     "inv-004, 2024-01-15, 500"
# ]

payment = "payment-004, 95, Customer payment"

invoices = [
    "inv-100, 2024-03-15, 100",
    "inv-300, 2024-01-10, 97"
]

forgiveness = 5
reconcile_payment(payment, invoices, forgiveness)

payment = "payment-003, 98, Customer payment"

invoices = [
    "inv-100, 2024-03-15, 100",
    "inv-200, 2024-02-20, 98",
    "inv-300, 2024-01-10, 102"
]

forgiveness = 5

reconcile_payment(payment, invoices, forgiveness)


payment = "payment-004, 95, Customer payment"

invoices = [
    "inv-100, 2024-03-15, 100",
    "inv-300, 2024-01-10, 97"
]

forgiveness = 5

reconcile_payment(payment, invoices, forgiveness)

payment = "payment-003, 98, Customer payment"

invoices = [
    "inv-100, 2024-03-15, 100",
    "inv-200, 2024-02-20, 98",
    "inv-300, 2024-01-10, 102"
]

forgiveness = 5
reconcile_payment(payment, invoices, forgiveness)







