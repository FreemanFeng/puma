package report

const (
	REPORT_PORT = 9099
)

const (
	PLATFORM_SEM   = "sem"
	PLATFORM_AD    = "ad"
	PLATFORM_STORE = "store"
	ROI_DATA       = "roi"
)

const (
	CONFIG_TASK   = 0
	CONFIG_COOKIE = 1
)

// Service ID
// GET方法，定义值需模METHOD_BASE值为0
// POST方法，定义值需模METHOD_BASE值为1
const (
	// 其他(ID < 100)
	TOKEN_GET         = 0 // 用于令牌获取
	COOKIE_KEEP_ALIVE = 1 // 用于cookie的keep alive，旧的ID是200
	CALLBACK_SERVICE  = 9 // 用于广点通的回调服务
	// 质量数据(100 <= ID < 200)
	UM_GET           = 110 //旧的ID是10
	ROI_GET          = 120 //旧的ID是20
	SBS_ACCOUNT_GET  = 130 //旧的ID是30
	SBS_CAMPAIGN_GET = 140 //旧的ID是31
	WA_GET           = 150
	// 基础数据(200 <= ID < 300)
	ACCOUNT_GET  = 200
	CAMPAIGN_GET = 210
	ADGROUP_GET  = 220
	AD_GET       = 230
	KEYWORD_GET  = 240
	CREATIVE_GET = 250
	// 天级展点消数据(300 <= ID < 600)
	DAILY_ACCOUNT_REPORTS_GET  = 300 //旧的ID是100
	DAILY_CAMPAIGN_REPORTS_GET = 310 //旧的ID是101
	DAILY_ADGROUP_REPORTS_GET  = 320 //旧的ID是102
	DAILY_AD_REPORTS_GET       = 330 //旧的ID是103
	DAILY_KEYWORD_REPORTS_GET  = 340 //旧的ID是104
	DAILY_CREATIVE_REPORTS_GET = 350
	// 小时级展点消数据(600 <= ID < 900)
	HOURLY_ACCOUNT_REPORTS_GET  = 600
	HOURLY_CAMPAIGN_REPORTS_GET = 610
	HOURLY_ADGROUP_REPORTS_GET  = 620
	HOURLY_AD_REPORTS_GET       = 630
	HOURLY_KEYWORD_REPORTS_GET  = 640
	HOURLY_CREATIVE_REPORTS_GET = 650
)

// 用于决定HTTP请求时使用的方法，如GET,POST,HEAD,DELETE等
const (
	METHOD_BASE = 10
)

//用于配置小时级数据获取时避免获取不到数据设定的一个时间延时
const (
	DEFAULT_START_HOUR = 0
	DEFAULT_END_HOUR   = 23
	DEFAULT_HOURLY_GET = "-1" //默认取这一小时的小时级数据
)

const (
	OFFSET_YESTERDAY = "-1"
	OFFSET_TODAY     = "0"
)

const (
	FAILED_SEARCH_ID = -1
	NOT_EXIST_ID     = 0
)

//自定义任务配置
const (
	CONFIG_NU      = "nu"
	CONFIG_DAU     = "dau"     // 日活
	CONFIG_QR      = "qr"      // 质量系数
	CONFIG_RET     = "ret"     // 留存
	CONFIG_VALIDNU = "validnu" // 留存
	CONFIG_ROI     = "roi"     //ROI
	CONFIG_LAST    = "last"
	CONFIG_START   = "start"
	CONFIG_END     = "end"
)

const (
	FAILED_NO_OAUTH              = 101
	FAILED_NO_TOKEN              = 102
	FAILED_TASK                  = 201
	FAILED_UNKNOWN_SERVICE       = 701
	FAILED_UNKNOWN_ACCOUNT       = 702
	FAILED_DATE_RANGE_INVALID    = 703
	FAILED_JSON_UNMARSHAL        = 901
	FAILED_MYSQL_QUERY           = 801
	FAILED_MYSQL_INSERT          = 802
	FAILED_MYSQL_UPDATE          = 803
	FAILED_MYSQL_DELETE          = 804
	FAILED_MYSQL_DATA_NULL       = 811
	FAILED_MYSQL_DATA_DUPLICATED = 812
)

const (
	NOT_SAVING_DATA = 0
	SAVING_DATA     = 1
)

const (
	HTTP_GET  = "GET"
	HTTP_POST = "POST"
)

const (
	GDT_PLATFORM   = "gdt"
	BAIDU_PLATFORM = "baidu"
)

const (
	DEFAULT_REPORT_TIMEOUT = 3600
)

const (
	DAY_SECONDS    = 86400
	INIT_INTERVAL  = 30
	CLEAR_INTERVAL = 1
	INIT_TIMEOUT   = 3600
)
