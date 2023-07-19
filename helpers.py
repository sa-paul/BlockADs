### Required datas
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
            if byte == 0: # End of parts
                if tmp != "":
                    domainParts.append(tmp)
                break

            if length == -1: # Yet not started, so first byte is length
                length = byte
            elif length == 0: # Read one part, so next byte is length
                domainParts.append(tmp)
                tmp = ""
                length = byte
            else: # Its part of domain name
                tmp += chr(byte)
                length -= 1
        
        tmp = data[totalLengthOfDomainPartsWithLengthCharacter:totalLengthOfDomainPartsWithLengthCharacter+4]
        # QType
        QTypeRaw = tmp[:2]
        QType = ""
        for x in QTypeRaw:
            QType += hex(x)[2:]
        QType = int(QType, 16)
        # QClass
        QClassRaw = tmp[2:]
        QClass = ""
        for x in QClassRaw:
            QClass += hex(x)[2:]
        QClass = int(QClass, 16)
        return Query(domainParts, QType, QClass)

    def toBytes(self):
        res = b""
        for part in self.nameParts:
            res += bytes([len(part)]) + bytes(part, "utf-8")
        res += b"\x00"
        res += self.type.to_bytes(2, "big")
        res += self.qclass.to_bytes(2, "big")
        return res

def getTransactionID(rawData:bytes):
    transactionIDRaw = rawData[:2]
    transactionID = ""
    for x in transactionIDRaw:
        transactionID += hex(x)[2:]
    return transactionID


def blankResponse(data:bytes, query:Query):
    QDCount = (1).to_bytes(2, "big")
    ANCount = (0).to_bytes(2, "big")
    NSCount = (0).to_bytes(2, "big")
    ARCount = (0).to_bytes(2, "big")
    responseHeader = data[:4] + QDCount + ANCount + NSCount + ARCount
    responseQuestion = query.toBytes()
    responseAnswer = b""
    return responseHeader + responseQuestion + responseAnswer
