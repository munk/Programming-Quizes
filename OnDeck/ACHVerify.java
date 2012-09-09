/** Verifies ACH file format is correct and compares file to standard for data validation.  Based on http://www.regaltek.com/docs/NACHA%20Format.pdf 
    This format assumes that a blank in a field is a null (0) value.
*/
public class ACHVerify {

    public class ACHRecord {

	private enum RecordType = { FileHeader, BatchHeader = 5, EntryDetail, EntryAddenda, BatchControl, FileControl};
	private int recordLen = 94;

	char[recordLen] record;
	public ACHRecord(char[recordLen] record) {
	    this.record = record;
	    this.RecType
	}
    }
    //TODO: Change data fields to a MAP!
    public class FileHeaderRecord extends ACHRecord {
	private char[1] RecordTypeCode;
	private char[2] PriorityCode;
	private char[10] ImmediateDestination;
	private char[10] ImmediateOrigin;
	private char[6] FileCreationDate;
	private char[4] FileCreationTime;
	private char[1] FileIDModifier;
	private char[3] RecordSize;
	private char[2] BlockingFactor;
	private char[1] FormatCode;
	private char[23] ImmediateDestinationName;
	private char[23] ImmediateOriginName;
	private char[8] ReferenceCode;
	public FileHeaderRecord(char[recordLen] record) {
	    super(record);
	    RecordTypeCode = Array.copyOfRange(record,0,1); // 1

	    assert RecordTypeCode[0] == RecordType.FileHeader;

	    PriorityCode = Array.copyOfRange(record,1,3); // 2
	    ImmediateDestination = Array.copyOfRange(record,3,13); // 10
	    ImmediateOrigin = Array.copyOfRange(record,13,23); // 10
	    FileCreationDate = Array.copyOfRange(record,23,29); // 6
	    FileCreationTime = Array.copyOfRange(record,29,33); // 4
	    FileIDModifier = Array.copyOfRange(record,33,34); // 1
	    RecordSize = Array.copyOfRange(record,34,37); // 3
	    BlockingFactor = Array.copyOfRange(record,37,39); // 2
	    FormatCode = Array.copyOfRange(record,39,40); // 1
	    ImmediateDestinationName = Array.copyOfRange(record,40,63); // 23
	    ImmediateOriginName = Array.copyOfRange(record,63,86); // 23
	    ReferenceCode = Array.copyOfRange(record,86,94); // 8
	}
    }

    public class BatchHeaderRecord extends ACHRecord {
	private char[1] RecordTypeCode;
	private char[3] ServiceClassCode;
	private char[16] CompanyName;
	private char[20] CompanyDiscretionaryData;
	private char[10] CompanyIdentification;
	private char[3] StandardEntryClassCode;
	private char[10] CompanyEntryDescription;
	private char[6] CompanyDescriptiveData;
	private char[6] EffectiveEntryDate;
	private char[3] SettlementDate_Julian;
	private char[1] OriginatorStatusCode;
	private char[8] OriginatingDFIIdentification;
	private char[7] BatchNumber;

	public BatchHeaderRecord(char[recordLen] record) {
	    super(record);
	    RecordTypeCode = Array.copyOfRange(record,0,1); 

	    assert RecordTypeCode[0] == RecordType.BatchHeader;

	    ServiceClassCode = Array.copyOfRange(record,1,4);
	    CompanyName = Array.copyOfRange(record,4,20);
	    CompanyDiscretionaryData = Array.copyOfRange(record,20,40);
	    CompanyIdentification = Array.copyOfRange(record,40,50);
	    StandardEntryClassCode = Array.copyOfRange(record,50,53);
	    CompanyEntryDescription = Array.copyOfRange(record,53,63);
	    CompanyDescriptiveData = Array.copyOfRange(record,63,69);
	    EffectiveEntryDate = Array.copyOfRange(record,69,75);
	    SettlementDate_Julian = Array.copyOfRange(record,75,78);
	    OriginatorStatusCode = Array.copyOfRange(record,78,79);
	    OriginatingDFIIdentification = Array.copyOfRange(record,79,87);
	    BatchNumber = Array.copyOfRange(record,87,94);
	}
    }

    public class EntryDetailRecord extends ACHRecord { 
	private char[1] RecordTypeCode;
	private char[2] TransactionCode;
	private char[8] ReceivingDFIIdentification;
	private char[1] CheckDigit;
	private char[17] DFIAccountNumber;
	private char[10] Amount;
	private char[15] IndividualIdentificationNumber;
	private char[22] IndividualName;
	private char[2] DiscretionaryData;
	private char[1] AddendaRecordIndicator;
	private char[15] TraceNumber;
	public BatchHeaderRecord(char[recordLen] record) {
	    super(record);
	    RecordTypeCode = Array.copyOfRange(record,0,1); 

	    assert RecordTypeCode[0] == RecordType.EntryDetail;
		
	    TransactionCode = Array.copyOfRange(record,1,3);
	    ReceivingDFIIdentification = Array.copyOfRange(record,3,11);
	    CheckDigit = Array.copyOfRange(record,11,12);
	    DFIAccountNumber = Array.copyOfRange(record,12,29);
	    Amount = Array.copyOfRange(record,29,39);
	    IndividualIdentificationNumber = Array.copyOfRange(record,39,54);
	    IndividualName = Array.copyOfRange(record,54,76);
	    DiscretionaryData = Array.copyOfRange(record,76,78);
	    AddendaRecordIndicator = Array.copyOfRange(record,78,79);
	    TraceNumber = Array.copyOfRange(record,79,94);
	}
    }

    public class EntryDetailAddendaRecord extends ACHRecord { 

    }


    public class BatchControlTotalRecord extends ACHRecord { 

    }


    public class FileControlRecord extends ACHRecord { 
    
    }
 
}