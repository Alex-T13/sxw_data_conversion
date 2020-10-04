from openpyxl import load_workbook, Workbook

wb = load_workbook(filename='work_2.xlsx', data_only=True)
ws = wb.active

names = list(ws.iter_rows(min_row=1, min_col=2,
                          max_row=ws.max_row, max_col=2, values_only=True))
quants = list(ws.iter_rows(min_row=1, min_col=4,
                           max_row=ws.max_row, max_col=4, values_only=True))
summs = list(ws.iter_rows(min_row=1, min_col=3,
                          max_row=ws.max_row, max_col=3, values_only=True))

wb.close

th_quants = [item for sublist in quants for item in sublist]
new_quants = list(map(float, th_quants))
th_cenas = [item for sublist in cenas for item in sublist]
new_cenas = list(map(float, th_cenas))
#print(names, len(names))
#print(quants, len(quants))
#print(summs, len(summs))
#print(names[7])
#new_quants = list(map(int, quants))
#new_summs = list(map(float, summs))

i = 0
while i < len(names):
    #th_quants = str(quants[i])
    #th_summs = str(summs[i])
    #new_list = list(map(int, old_list))
    #new_quants = map(float, th_quants)
    #new_summs = map(float, th_summs)
    #new_quants = int(th_quants)
    #new_summs = int(th_summs)
    #mat = new_summs[i] / new_quants[i]
    #print(mat)
    #th_summs = summs[i]
    #print(th_summs)
    i += 1
