for line in open('replace_strings.txt'):
   data = line.strip()
   if len(data) > 0:
      print "sed -i 's/%s/\\\"%s\\\"/g' data2.log" % (data, data)
   print "sed -i 's/%s/%s/g' data2.log" % ('\\"\\"', '\\"')
