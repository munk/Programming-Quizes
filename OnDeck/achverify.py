import sys
import thread
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

def makeACHFile_example():
    """These are just some made up entries.  They're based on the format described in http://www.regaltek.com/docs/NACHA%20Format.pdf
    but have not been checked for accuracy or correctness.  Importantly, they are 94 characters wide and similar to the standard"""
    fileHeader   = '101 07100050501234567891209091111A094101DestinationBank12345678OriginCompany1234567890abcdefgh'
    batchHeader  = '5225COMPANYINC123456discretionarydataabc0123456789PPDpayments00abcdef120910   1071000500000001'
    PPDEntry1    = '622000123411234567890ABC     0000111100CompanyInc     JohnSmith             dd0123456789012345'
    PPDEntry2    = '622000123411234567890ABC     1111222200CompanyInc     JohnSmith             dd0123456789012345' #This line does not match standard
    PPDEntry3    = '622000123411234567890ABC     0000333300CompanyInc     JohnSmith             dd0123456789012345'
    BatchControl = '82250000030000020040000000666600000000000000CompanyInc                         000012340000001'
    FileControl  = '900000100000700000003000000020040000666600                                                    '
    ACHFile = fileHeader + batchHeader + PPDEntry1 + PPDEntry2 + PPDEntry3 + BatchControl + FileControl
    with open('test.ach', 'w') as f:
        f.write(ACHFile)
    
def makeACHFile_standard():
    """These are just some made up entries.  They're based on the format described in http://www.regaltek.com/docs/NACHA%20Format.pdf
    but have not been checked for accuracy or correctness.  Importantly, they are 94 characters wide and similar to the standard"""
    fileHeader   = '101 07100050501234567891209091111A094101DestinationBank12345678OriginCompany1234567890abcdefgh'
    batchHeader  = '5225COMPANYINC123456discretionarydataabc0123456789PPDpayments00abcdef120910   1071000500000001'
    PPDEntry1    = '622000123411234567890ABC     0000111100CompanyInc     JohnSmith             dd0123456789012345'
    PPDEntry2    = '622000123411234567890ABC     0000222200CompanyInc     JohnSmith             dd0123456789012345'
    PPDEntry3    = '622000123411234567890ABC     0000333300CompanyInc     JohnSmith             dd0123456789012345'
    BatchControl = '82250000030000020040000000666600000000000000CompanyInc                         000012340000001'
    FileControl  = '900000100000700000003000000020040000666600                                                    '
    ACHFile = fileHeader + batchHeader + PPDEntry1 + PPDEntry2 + PPDEntry3 + BatchControl + FileControl
    with open('std.ach', 'w') as f:
        f.write(ACHFile)

def readACHFile(filename):
    result = ''
    with open(filename, "r") as f:
        result = f.read()
    return result

def compareACHFiles(test, std):
    #TODO: If an entry line fails to match, but a control line also fails to match, flag that.  Requires file format validation
    Fail = False
    Pass = True

    test_const = readACHFile(test)
    standard_const = readACHFile(std)
    test_result = []
    std_result = []

    test = []
    standard = []
    test.extend(test_const)
    standard.extend(standard_const)

    recordSize = 94
    recordCount = len(standard) / recordSize
    
    RecordFlags = [Fail] * recordCount

    # Check for missing records
    if len(standard) != len(test): #TODO: See if we can find out which records are missing
        raise Exception("<html> <body> <p> Test file is not the same size as standard! Records are missing </p> </body> </html>")
    if len(test) % 94 != 0:
        raise Exception ("<html> <body> <p> Incomplete Record Fields! File is corrupted </p> </body> </html>")

    # Verify all records are the same - flag those that are different
    print "THERE"
    for i in range (0,recordCount): #for each record in Test

        record_test = test[0:recordSize]
        record_std  = standard[0:recordSize]
        
        for j in range(0,recordSize): #for each character in record
            if record_test[j] != record_std[j]: #if the records are different, note this
                RecordFlags[i] = Fail
                break
            RecordFlags[i] = Pass
        test_result.append("".join(test[0:recordSize]))
        std_result.append("".join(standard[0:recordSize]))
        test = test[recordSize:]
        standard = standard[recordSize:]
    print "IN METHOD: ", RecordFlags
    return RecordFlags, test_result, std_result

def startServer():
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    server_address = ('127.0.0.1', 8000)

    HandlerClass.protocol_version = "HTTP/1.0"
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

def main():
    makeACHFile_example()
    makeACHFile_standard()
    webInfo = ''
    diff = None
    try:
        diff = compareACHFiles('test.ach','std.ach')
    except Exception as e:
        webinfo = e
        startServer()

    print diff 
    flags = diff[0]
    test  = diff[1]
    std   = diff[2] 
    
    webinfo = '<html> <body>'
    for t,s,goodRecord in zip(test,std,flags):
        if goodRecord:
            webinfo = webinfo + '<p style="color:green"> Valid Record: ' + t + '</p>'
        else:
            webinfo = webinfo + '<p style="color:red"> ERROR: ' + t + ' <br /> Record should have been: ' + s + '</p>'
    webinfo = webinfo + '</body></html>'
    with open('index.html', 'w') as f:
        f.write(webinfo)

    startServer()
    

