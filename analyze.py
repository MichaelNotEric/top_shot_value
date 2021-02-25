listings = []
temp = []

with open('text.txt') as f:
  lines = f.readline().replace('</option>','\n').split('\n')
  lines.pop(0)
  lines.pop(1)
  lines.pop(len(lines)-1)
  lines.pop(len(lines)-1)

  for line in lines:
    temp.append(line.split('#')[1])

with open('parsed.txt','w') as f: 
  for line in temp:
    f.write(str(line) + '\n')

with open('parsed.txt') as f:
  line = f.readline()

  while line:
    serial = int(line.split(' - ')[0])
    price = int(float(line.split(' - $')[1].split(' - L')[0].split('\n')[0].replace(',','').replace(' (Jersey Number)','')))
    if price <= 50:
      listings.append((serial, price))
    line = f.readline()


i = 0

while i < len(listings):
  for l in listings:
    if listings[i][1] == l[1] and listings[i][0] > l[0]:
      listings.pop(i)
      i = i - 1
      #print(listings[i])
      #print(l)
      #print(' ')

  i = i + 1

i = 0

while i < len(listings):
  for l in listings:
    if listings[i][1] > l[1] and listings[i][0] > l[0]:
      listings.pop(i)
      i = i - 1

  i = i + 1

with open('out.txt','w') as f:
  for l in listings:
    f.write(str(l[0]) + ',' + str(l[1]) + '\n')
