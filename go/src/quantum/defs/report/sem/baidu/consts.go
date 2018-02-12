package baidu

const (
	DAY_SECONDS    = 86400
	INIT_INTERVAL  = 30
	CLEAR_INTERVAL = 1
	INIT_TIMEOUT   = 3600
)

// 百度API
const (
	API_URL          = "https://api.baidu.com/sms/service/"
	CT               = "application/json"
	MAX_RETRY        = 3
	RETRY_INTERVAL   = 10
	REQUEST_INTERVAL = 10
)

const (
	SERVICE_ACCOUNT          = "AccountService"
	SERVICE_ADGROUP          = "AdgroupService"
	SERVICE_BULKJOB          = "BulkJobService"
	SERVICE_CAMPAIGN         = "CampaignService"
	SERVICE_CREATIVE         = "CreativeService"
	SERVICE_DYNAMIC_CREATIVE = "DynamicCreativeService"
	SERVICE_KEYWORD          = "KeywordService"
	SERVICE_KR               = "KRService"
	SERVICE_NEW_CREATIVE     = "NewCreativeService"
	SERVICE_REPORT           = "ReportService"
	SERVICE_SEARCH           = "SearchService"
)

const (
	ID_SERVICE_ACCOUNT          = 100
	ID_SERVICE_ADGROUP          = 200
	ID_SERVICE_BULKJOB          = 300
	ID_SERVICE_CAMPAIGN         = 400
	ID_SERVICE_CREATIVE         = 500
	ID_SERVICE_DYNAMIC_CREATIVE = 600
	ID_SERVICE_KEYWORD          = 700
	ID_SERVICE_KR               = 800
	ID_SERVICE_NEW_CREATIVE     = 900
	ID_SERVICE_REPORT           = 1000
	ID_SERVICE_SEARCH           = 1100
)

const (
	METHOD_GET_ACCOUNT_INFO    = "getAccountInfo"
	METHOD_UPDATE_ACCOUNT_INFO = "updateAccountInfo"
	// AdgroupService
	METHOD_ADD_ADGROUP    = "addAdgroup"
	METHOD_UPDATE_ADGROUP = "updateAdgroup"
	METHOD_DELETE_ADGROUP = "deleteAdgroup"
	METHOD_GET_ADGROUP    = "getAdgroup"
	// BulkJobService
	METHOD_GET_ALL_CHANGED_OBJECTS = "getAllChangedObjects"
	METHOD_CANCEL_DOWNLOAD         = "cancelDownload"
	METHOD_GET_CHANGED_ITEM_ID     = "getChangedItemId"
	METHOD_GET_CHANGED_SCALE       = "getChangedScale"
	METHOD_GET_ALL_OBJECTS         = "getAllObjects"
	METHOD_GET_FILE_STATUS         = "getFileStatus"
	METHOD_GET_FILE_PATH           = "getFilePath"
	METHOD_GET_CHANGED_ID          = "getChangedId"
	METHOD_GET_USER_CACHE          = "getUserCache"
	// CampaignService
	METHOD_GET_CAMPAIGN    = "getCampaign"
	METHOD_UPDATE_CAMPAIGN = "updateCampaign"
	METHOD_DELETE_CAMPAIGN = "deleteCampaign"
	METHOD_ADD_CAMPAIGN    = "addCampaign"
	// CreativeService
	METHOD_GET_CREATIVE    = "getCreative"
	METHOD_UPDATE_CREATIVE = "updateCreative"
	METHOD_DELETE_CREATIVE = "deleteCreative"
	METHOD_ADD_CREATIVE    = "addCreative"
	// DynamicCreativeService
	METHOD_GET_DYN_CREATIVE                  = "getDynCreative"
	METHOD_GET_EXCLUSION_TYPE_BY_CAMPAIGN_ID = "getExclusionTypeByCampaignId"
	METHOD_ADD_DYN_CREATIVE                  = "addDynCreative"
	METHOD_DELETE_DYN_CREATIVE               = "deleteDynCreative"
	METHOD_UPDATE_DYN_CREATIVE               = "updateDynCreative"
	METHOD_ADD_EXCLUSION_TYPE                = "addExclusionType"
	METHOD_DEL_EXCLUSION_TYPE                = "delExclusionType"
	// KeywordService
	METHOD_UPDATE_WORD = "updateWord"
	METHOD_ADD_WORD    = "addWord"
	METHOD_DELETE_WORD = "deleteWord"
	METHOD_GET_WORD    = "getWord"
	// KRService
	METHOD_GET_ESTIMATED_DATABYBID = "getEstimatedDataByBid"
	METHOD_GET_ESTIMATED_DATA      = "getEstimatedData"
	METHOD_GET_KR_FILE_ID_BY_WORDS = "getKRFileIdByWords"
	METHOD_GET_FILE_STATUS         = "getFileStatus"
	METHOD_GET_FILE_PATH           = "getFilePath"
	METHOD_GET_KR_BY_QUERY         = "getKRByQuery"
	METHOD_GET_KR_CUSTOM           = "getKRCustom"
	METHOD_GET_BID_BY_WORDS        = "getBidByWords"
	// NewCreativeService
	METHOD_ADD_BRIDGE     = "addBridge"
	METHOD_ADD_SUBLINK    = "addSublink"
	METHOD_UPDATE_SUBLINK = "updateSublink"
	METHOD_DELETE_SUBLINK = "deleteSublink"
	METHOD_ADD_PHONE      = "addPhone"
	METHOD_UPDATE_PHONE   = "updatePhone"
	METHOD_UPDATE_BRIDGE  = "updateBridge"
	METHOD_ADD_ECALL      = "addEcall"
	METHOD_UPDATE_ECALL   = "updateEcall"
	METHOD_GET_SUBLINK    = "getSublink"
	METHOD_GET_BRIDGE     = "getBridge"
	METHOD_GET_PHONE      = "getPhone"
	METHOD_GET_ECALL      = "getEcall"
	METHOD_GET_ECALLGROUP = "getEcallGroup"
	//ReportService
	METHOD_GET_REALTIME_QUERY_DATA    = "getRealTimeQueryData"
	METHOD_GET_REALTIME_PAIR_DATA     = "getRealTimePairData"
	METHOD_GET_PROFESSIONAL_REPORT_ID = "getProfessionalReportId"
	METHOD_GET_REPORT_STATE           = "getReportState"
	METHOD_GET_REPORT_FILE_URL        = "getReportFileUrl"
	METHOD_GET_REAL_TIME_DATA         = "getRealTimeData"
	//SearchService
	METHOD_GET_COUNT_BY_ID             = "getCountById"
	METHOD_GET_TAB                     = "getTab"
	METHOD_GET_MATERIAL_INFO_BY_SEARCH = "getMaterialInfoBySearch"
)
const (
	ID_METHOD_GET_ACCOUNT_INFO    = 1001
	ID_METHOD_UPDATE_ACCOUNT_INFO = 1002
	// AdgroupService
	ID_METHOD_ADD_ADGROUP    = 2001
	ID_METHOD_UPDATE_ADGROUP = 2002
	ID_METHOD_DELETE_ADGROUP = 2003
	ID_METHOD_GET_ADGROUP    = 2004
	// BulkJobService
	ID_METHOD_GET_ALL_CHANGED_OBJECTS = 3001
	ID_METHOD_CANCEL_DOWNLOAD         = 3002
	ID_METHOD_GET_CHANGED_ITEM_ID     = 3003
	ID_METHOD_GET_CHANGED_SCALE       = 3004
	ID_METHOD_GET_ALL_OBJECTS         = 3005
	ID_METHOD_GET_FILE_STATUS         = 3006
	ID_METHOD_GET_FILE_PATH           = 3007
	ID_METHOD_GET_CHANGED_ID          = 3008
	ID_METHOD_GET_USER_CACHE          = 3009
	// CampaignService
	ID_METHOD_GET_CAMPAIGN    = 4001
	ID_METHOD_UPDATE_CAMPAIGN = 4002
	ID_METHOD_DELETE_CAMPAIGN = 4003
	ID_METHOD_ADD_CAMPAIGN    = 4004
	// CreativeService
	ID_METHOD_GET_CREATIVE    = 5001
	ID_METHOD_UPDATE_CREATIVE = 5002
	ID_METHOD_DELETE_CREATIVE = 5003
	ID_METHOD_ADD_CREATIVE    = 5004
	// DynamicCreativeService
	ID_METHOD_GET_DYN_CREATIVE                  = 6001
	ID_METHOD_GET_EXCLUSION_TYPE_BY_CAMPAIGN_ID = 6002
	ID_METHOD_ADD_DYN_CREATIVE                  = 6003
	ID_METHOD_DELETE_DYN_CREATIVE               = 6004
	ID_METHOD_UPDATE_DYN_CREATIVE               = 6005
	ID_METHOD_ADD_EXCLUSION_TYPE                = 6006
	ID_METHOD_DEL_EXCLUSION_TYPE                = 6007
	// KeywordService
	ID_METHOD_UPDATE_WORD = 7001
	ID_METHOD_ADD_WORD    = 7002
	ID_METHOD_DELETE_WORD = 7003
	ID_METHOD_GET_WORD    = 7004
	// KRService
	ID_METHOD_GET_ESTIMATED_DATABYBID = 8001
	ID_METHOD_GET_ESTIMATED_DATA      = 8002
	ID_METHOD_GET_KR_FILE_ID_BY_WORDS = 8003
	ID_METHOD_GET_FILE_STATUS         = 8004
	ID_METHOD_GET_FILE_PATH           = 8005
	ID_METHOD_GET_KR_BY_QUERY         = 8006
	ID_METHOD_GET_KR_CUSTOM           = 8007
	ID_METHOD_GET_BID_BY_WORDS        = 8008
	// NewCreativeService
	ID_METHOD_ADD_BRIDGE     = 9001
	ID_METHOD_ADD_SUBLINK    = 9002
	ID_METHOD_UPDATE_SUBLINK = 9003
	ID_METHOD_DELETE_SUBLINK = 9004
	ID_METHOD_ADD_PHONE      = 9005
	ID_METHOD_UPDATE_PHONE   = 9006
	ID_METHOD_UPDATE_BRIDGE  = 9007
	ID_METHOD_ADD_ECALL      = 9008
	ID_METHOD_UPDATE_ECALL   = 9009
	ID_METHOD_GET_SUBLINK    = 9010
	ID_METHOD_GET_BRIDGE     = 9011
	ID_METHOD_GET_PHONE      = 9012
	ID_METHOD_GET_ECALL      = 9013
	ID_METHOD_GET_ECALLGROUP = 9014
	//ReportService
	ID_METHOD_GET_REALTIME_QUERY_DATA    = 10001
	ID_METHOD_GET_REALTIME_PAIR_DATA     = 10002
	ID_METHOD_GET_PROFESSIONAL_REPORT_ID = 10003
	ID_METHOD_GET_REPORT_STATE           = 10004
	ID_METHOD_GET_REPORT_FILE_URL        = 10005
	ID_METHOD_GET_REAL_TIME_DATA         = 10006
	//SearchService
	ID_METHOD_GET_COUNT_BY_ID             = 11001
	ID_METHOD_GET_TAB                     = 11002
	ID_METHOD_GET_MATERIAL_INFO_BY_SEARCH = 11003
)

const (
	URL_PATH_DAILY_REPORTS_GET = "daily_reports/get"
)

const (
	GET    = 0
	POST   = 1
	DELETE = 2
)

// API预定义常量
const (
	MAX_PAGESIZE = 99
	NOR_PAGESIZE = 33
	MIN_PAGESIZE = 10
)

// 其他
const (
	RERUN     = 1
	LAST_YEAR = "-365"
	YESTERDAY = "-1"
	TODAY     = "0"
)

const (
	DEFAULT_REPORT_TIMEOUT = 3600
)
