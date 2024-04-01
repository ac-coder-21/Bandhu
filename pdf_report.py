from fpdf import FPDF
import qrcode
from get_gt_arr import get_gt_val
from datetime import datetime

prev_values =  get_gt_val("2bf8a5c047d8429993f2ea21e65fa44c")

date = "13-02-2023"
name = "Aston Martin"
age = "22"
gender = "Male"
education = "Under-Graduate"
test = "Depression Test"
prev_score = prev_values[1]
prev_test_date = prev_values[0]
score = "46.7%"

def generate_pdf(date, name, age, gender, education, test, prev_score, prev_test_date, score, file_name):
    pdf = FPDF('P', 'mm', 'Letter')

    #adding a page
    pdf.add_page()

    #adding page break
    pdf.set_auto_page_break(auto=True, margin = 15)

    #add text headings
    pdf.set_font('times','BU', 16)
    pdf.cell(200, 10, 'Bandhu- A Mental Health Aid', border=True, ln=1, align='C')
    pdf.set_font('times','', 14 )
    pdf.cell(10, 40, 'GENERATED REPORT')
    pdf.cell(140, 40, f'DATE: {date}', 0, 1, 'R')

    #personal details
    pdf.set_font('times', 'B', 14)
    pdf.cell(40, 1, 'Personal Details', ln=True)
    pdf.set_font('times', '', 12)
    pdf.cell(40, 20, f'Name: {name}', ln= True)
    pdf.cell(40, 1, f'Age: {age}', ln=True)
    pdf.cell(40, 20, f'Sex: {gender}', ln=True)
    pdf.cell(40, 1, f'Educational Attainment: {education}', ln=True)

    #patient history
    pdf.set_font('times', 'B', 14)
    pdf.cell(40, 20, 'Patient History', ln=True)
    pdf.set_font('times', '', 12)
    pdf.cell(40, 1, f'Test Type: {test}', ln=True)
    pdf.cell(40, 20, f'Test Score: {prev_score}', ln= True)
    pdf.cell(40, 1, 'Previously Recommended Remedy: Try to relax and meditate, Have proper sleep and proper rest in free time.', ln= True)
    pdf.cell(40, 20, f'Test Date: {prev_test_date}', ln= True)

    #test details
    pdf.set_font('times', 'B', 14)
    pdf.cell(40, 10, 'Test Details', ln=True)
    pdf.set_font('times', '', 12)
    pdf.cell(40, 10, f'Test Type: {test}t', ln=True)
    pdf.cell(40, 10, f'Current Test Score: {score}', ln=True)
    pdf.cell(100, 10, 'Reference:   Level 1: 0-5      Level 2: 6-7     Level 3: 8-10', border=True, ln=True, align='C')
    pdf.cell(40, 20, 'Remedy: Try to have proper Sleep and proper diet on time.', ln=True)

    # Generate QR code
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4,
    # )
    # qr.add_data('https://www.google.com')
    # qr.make(fit=True)
    # # Save the QR code as an image
    # img = qr.make_image(fill='black', back_color='white')
    # img.save('google_homepage_qr.png')
    # # Create a PDF and insert the QR code image
    # #pdf = FPDF()
    # #pdf.add_page()
    # pdf.image('google_homepage_qr.png', x=140, y=80, w=50, h=50)
    #pdf.output('pdf_report.pdf', 'F')

    #footer
    def footer(pdf):
            pdf.set_y(-15)
            pdf.set_font('times', '', 10)
            pdf.cell(0, 0, '**An automatically generated report not for medical use**', 0, 0, 'C')
    footer(pdf)

    pdf.output(file_name)
