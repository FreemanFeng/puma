package gdt

// 令牌有效期
const (
	EXPIRED_NOW           = 0
	EXPIRED_CODE          = 300
	EXPIRED_TOKEN         = 86400
	EXPIRED_REFRESH_TOKEN = 63072000 // 两年
)

const (
	TYPE_CODE           = 0
	TYPE_TOKEN          = 1
	TYPE_REFRESH_TOKEN  = 2
	TYPE_TASK_IDLE_DAYS = 3
)

const (
	STAT_INIT    = 0
	STAT_AUTH    = 1
	STAT_EXPIRED = 2
)

// 腾讯广点通API
const (
	API_VERSION      = "v1.0"
	API_URL          = "https://api.e.qq.com"
	CT               = "application/json"
	UA               = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	OAUTH_URL        = "https://developers.e.qq.com/"
	SANDBOX_API_URL  = "https://sandbox.api.e.qq.com/"
	REDIRECT_URI     = "http://uplus.union.uc.cn/callback/gdt"
	REDIRECT_PORT    = 9080
	CONFIG_PORT      = 9089
	MAX_RETRY        = 3
	RETRY_INTERVAL   = 10
	REQUEST_INTERVAL = 10
)

const (
	ONLINE = 1
)

const (
	URL_PATH_TOKEN              = "oauth/token"
	URL_PATH_DAILY_REPORTS_GET  = "daily_reports/get"
	URL_PATH_HOURLY_REPORTS_GET = "hourly_reports/get"
	URL_PATH_CAMPAIGNS_GET      = "campaigns/get"
	URL_PATH_ADGROUPS_GET       = "adgroups/get"
	URL_PATH_ADCREATIVES_GET    = "adcreatives/get"
	URL_PATH_ADS_GET            = "ads/get"
)

const (
	PARAM_CLIENT_ID          = "client_id"
	PARAM_CLIENT_SECRET      = "client_secret"
	PARAM_ACCESS_TOKEN       = "access_token"
	PARAM_REFRESH_TOKEN      = "refresh_token"
	PARAM_GRANT_TYPE         = "grant_type"
	PARAM_AUTHORIZATION_CODE = "authorization_code"
	PARAM_REDIRECT_URI       = "redirect_uri"
	PARAM_ACCOUNT_ID         = "account_id"
	PARAM_NONCE              = "nonce"
	PARAM_TIMESTAMP          = "timestamp"
)

const (
	QUERY_AUTHORIZATION_CODE = 0
	QUERY_TOKEN              = 1
	QUERY_REFRESH_TOKEN      = 2
	QUERY_IDLE               = 3
)

const (
	CONFIG_TOKEN         = 1
	CONFIG_REFRESH_TOKEN = 2
	CONFIG_LAST_VISIT    = 3
)

// 接口类型
const (
	ADVERTISER_LEVEL = 0
	CAMPAIGN_LEVEL   = 1
	ADGROUP_LEVEL    = 2
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
	RERUN      = 1
	LAST_YEAR  = "-365"
	YESTERDAY  = "-1"
	TODAY      = "0"
	DATA_EMPTY = ""
)

const (
	COST_BASE = 100
)
