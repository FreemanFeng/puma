package util

const (
	SUCCESSFUL                    = 0
	FAILED                        = 1
	FAILED_TIMEOUT                = 2
	FAILED_FUNC_PARAMS_NOT_ENOUGH = 3
)

const (
	NO_CRON_JOB           = 0
	CRON_TYPE_EVERY_DAYS  = 1
	CRON_TYPE_EVERY_HOURS = 2
	CRON_TYPE_EVERY_MINS  = 3
	CRON_TYPE_EVERY_SECS  = 4
	KEEP_ALIVE            = 5
)

const (
	YEAR_SECS = 31536000
	DAY_SECS  = 86400
	HOUR_SECS = 3600
	MIN_SECS  = 60
	ONE_SEC   = 1
)

const (
	STR_DOUBLE_QUOTES = "\""
)

const (
	MIN_ROUTES   = 2 // 最少路由节点数
	PLATFORM_POS = 1 // Platform所在path的位置
	SERVICE_POS  = 2 // Service所在path的位置
)

const (
	GET_CACHE = 0
	SET_CACHE = 1
	DEL_CACHE = 2
)

const (
	CACHE_MISSING = 0
	CACHE_EXISTS  = 1
	CACHE_EXPIRED = 2
)
