import xlsxwriter

def create_sheet(buffer, data):
    # create workbook, worksheet
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.set_column_pixels(0, 4, 200)

    # define formats
    header_format = workbook.add_format({'bold':True})

    worksheet.write("A1", "Award Name", header_format)
    worksheet.write("B1", "Award Value", header_format)
    worksheet.write("C1", "Award Type", header_format)
    worksheet.write("D1", "Award Description", header_format)

    worksheet.write("E1", "Selection Process", header_format)
    worksheet.write("F1", "Eligibility Criteria", header_format)

    worksheet.write("G1", "Affiliation", header_format)
    worksheet.write("H1", "Term", header_format)
    worksheet.write("I1", "Levels", header_format)
    worksheet.write("J1", "Program", header_format)
    worksheet.write("K1", "Citizenship", header_format)

    colInd = 0
    printRowIndex = 0

    for row in data:
        rowInd = row[0]+1
        row = ["" if i is None else i for i in row]
        if row[2]:
            worksheet.write_url(printRowIndex, colInd, row[2], string=row[1]) #award name and link
        else:
            worksheet.write(printRowIndex, colInd, row[1]) #award name
        worksheet.write(printRowIndex, colInd+1, row[5]) #award value
        worksheet.write(printRowIndex, colInd+2, ', '.join(filter(None, row[9]))) #[award type]
        worksheet.write(printRowIndex, colInd+3, row[6]) #award description

        worksheet.write(printRowIndex, colInd+4, row[3]) #award selection
        worksheet.write(printRowIndex, colInd+5, row[7]) #selection eligibility
        worksheet.write(printRowIndex, colInd+6, ', '.join(filter(None, row[12]))) #[affiliation]
        worksheet.write(printRowIndex, colInd+7, ', '.join(filter(None, row[11]))) #[term]
        worksheet.write(printRowIndex, colInd+8, ', '.join(filter(None, row[8]))) #[levels]
        worksheet.write(printRowIndex, colInd+9, ', '.join(filter(None, row[10]))) #[programs]
        worksheet.write(printRowIndex, colInd+10, row[4]) #citizenship
        printRowIndex += 1

    workbook.close()
    return workbook

