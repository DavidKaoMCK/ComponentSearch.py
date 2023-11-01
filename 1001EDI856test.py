import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import qrcode

def generate_edi():
    # Collect data from input fields
    sender_id = sender_id_entry.get()
    receiver_id = receiver_id_entry.get()
    shipment_id = shipment_id_entry.get()
    carrier = carrier_entry.get()
    method = method_entry.get()
    bill_of_lading = bill_of_lading_entry.get()
    po_number = po_number_entry.get()
    product_upc = product_upc_entry.get()
    quantity = quantity_entry.get()
    uom = uom_entry.get()

    # Generate EDI 856 structure
    edi_content = f"""ISA*00*          *00*          *ZZ*{sender_id}      *ZZ*{receiver_id}    *YYMMDD*HHMM*U*00401*000000001*0*P*>
GS*SH*{sender_id}*{receiver_id}*YYMMDD*HHMM*1*X*004010
ST*856*0001
BSN*00*{shipment_id}*YYMMDD*HHMM*0001
HL*1**S
TD5**2*{carrier}**{method}
REF*BM*{bill_of_lading}
DTM*011*YYMMDD
HL*2*1*O
PRF*{po_number}
HL*3*2*I
LIN**UP*{product_upc}
SN1**{quantity}*{uom}
CTT*3
SE*14*0001
GE*1*1
IEA*1*000000001"""

    # Save to a file
    with open("output_edi_856.txt", "w") as file:
        file.write(edi_content)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(edi_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("output_edi_856_qrcode.png")

    # Show a confirmation message
    messagebox.showinfo("Info", "EDI 856 generated and saved as output_edi_856.txt. QR code saved as output_edi_856_qrcode.png")


# Create the main window
root = tk.Tk()
root.title("EDI 856 Generator")

# Create and place labels and input fields
ttk.Label(root, text="Sender ID").grid(row=0, column=0, padx=10, pady=5)
sender_id_entry = ttk.Entry(root)
sender_id_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Receiver ID").grid(row=1, column=0, padx=10, pady=5)
receiver_id_entry = ttk.Entry(root)
receiver_id_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Shipment ID").grid(row=2, column=0, padx=10, pady=5)
shipment_id_entry = ttk.Entry(root)
shipment_id_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="Carrier").grid(row=3, column=0, padx=10, pady=5)
carrier_entry = ttk.Entry(root)
carrier_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(root, text="Method").grid(row=4, column=0, padx=10, pady=5)
method_entry = ttk.Entry(root)
method_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(root, text="Bill of Lading Number").grid(row=5, column=0, padx=10, pady=5)
bill_of_lading_entry = ttk.Entry(root)
bill_of_lading_entry.grid(row=5, column=1, padx=10, pady=5)

ttk.Label(root, text="PO Number").grid(row=6, column=0, padx=10, pady=5)
po_number_entry = ttk.Entry(root)
po_number_entry.grid(row=6, column=1, padx=10, pady=5)

ttk.Label(root, text="Product UPC").grid(row=7, column=0, padx=10, pady=5)
product_upc_entry = ttk.Entry(root)
product_upc_entry.grid(row=7, column=1, padx=10, pady=5)

ttk.Label(root, text="Quantity").grid(row=8, column=0, padx=10, pady=5)
quantity_entry = ttk.Entry(root)
quantity_entry.grid(row=8, column=1, padx=10, pady=5)

ttk.Label(root, text="UOM").grid(row=9, column=0, padx=10, pady=5)
uom_entry = ttk.Entry(root)
uom_entry.grid(row=9, column=1, padx=10, pady=5)

# Create and place the generate button
generate_button = ttk.Button(root, text="Generate EDI 856", command=generate_edi)
generate_button.grid(row=10, column=0, columnspan=2, pady=20)

root.mainloop()
