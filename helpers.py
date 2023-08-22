# Constants for DNS query types and classes
queryTypesName = ["A", "NS", "MD", "MF", "CNAME", "SOA", "MB", "MG", "MR", "NULL", "WKS", "PTR", "HINFO", "MINFO", "MX", "TXT"]
queryClassesName = ["IN", "CS", "CH", "HS"]

# Query Questions parser
class Query:
    def __init__(self, nameParts, type, qclass):
        self.nameParts = nameParts
        self.type = type
        self.qclass = qclass

    def domainName(self, endDot=False):
        res = '.'.join(self.nameParts)
        if endDot and res[-1] != ".":
            res += "."
        return res

    def queryType(self):
        if self.type > 16:
            return "Unknown"
        return queryTypesName[self.type - 1]

    @staticmethod
    def fromBytes(rawData:bytes):
        data = rawData[12:]
        domainParts = []

        totalLengthOfDomainPartsWithLengthCharacter = 0
        length = -1
        tmp = ""
        for byte in data:
            totalLengthOfDomainPartsWithLengthCharacter += 1
            if byte == 0:  # End of domain name parts
                if tmp != "":
                    domainParts.append(tmp)
                break

            if length == -1:  # Length of the domain name part not started yet, so the first byte is length
                length = byte
            elif length == 0:  # Length of the domain name part reached, so the next byte is the length
                domainParts.append(tmp)
                tmp = ""
                length = byte
            else:  # Part of the domain name
                tmp += chr(byte)
                length -= 1
        
        # Parsing QType and QClass
        tmp = data[totalLengthOfDomainPartsWithLengthCharacter:totalLengthOfDomainPartsWithLengthCharacter+4]
        QTypeRaw = tmp[:2]
        QType = int.from_bytes(QTypeRaw, byteorder='big')  # Convert bytes to integer
        QClassRaw = tmp[2:]
        QClass = int.from_bytes(QClassRaw, byteorder='big')  # Convert bytes to integer
        
        return Query(domainParts, QType, QClass)

    def toBytes(self):
        res = b""
        for part in self.nameParts:
            res += bytes([len(part)]) + bytes(part, "utf-8")
        res += b"\x00"
        res += self.type.to_bytes(2, "big")  # Convert integer to bytes
        res += self.qclass.to_bytes(2, "big")  # Convert integer to bytes
        return res

def getTransactionID(rawData:bytes):
    transactionIDRaw = rawData[:2]
    transactionID = transactionIDRaw.hex()  # Convert bytes to hexadecimal
    return transactionID

def blankResponse(data:bytes, query:Query):
    # Prepare DNS response header
    QDCount = (1).to_bytes(2, "big")
    ANCount = (0).to_bytes(2, "big")
    NSCount = (0).to_bytes(2, "big")
    ARCount = (0).to_bytes(2, "big")
    responseHeader = data[:4] + QDCount + ANCount + NSCount + ARCount
    
    # Prepare response question section
    responseQuestion = query.toBytes()
    
    # Prepare response answer section (blank in this case)
    responseAnswer = b""
    
    return responseHeader + responseQuestion + responseAnswer
