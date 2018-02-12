package report

type ServiceData struct {
	ServiceID int    `json:"service_id"` // 服务ID，标识API接口
	Params    string `json:"params"`     // 服务参数
}

type CronJob struct {
	CronType     int           `json:"cron_type"`     // CRON类型
	Interval     int           `json:"interval"`      // CRON JOB间隔
	Start        []int         `json:"start"`         // CRON JOB开始时间
	APIVersion   string        `json:"api_version"`   // 广告平台API版本(广点通)
	ClientID     string        `json:"client_id"`     // 广告平台应用ID(广点通)
	ClientSecret string        `json:"client_secret"` // 广告平台应用密钥(广点通)
	Account      string        `json:"account"`       // 投放账号
	Platform     string        `json:"platform"`      // 平台，SEM/AD/STORE
	Service      string        `json:"service"`       // 服务，GDT/WNYS/LH/JRTT 等
	Data         []ServiceData `json:"data"`          // 调用的服务列表
}

type TaskConfig struct {
	Online int       `json:"online"` // 是否连在线数据库
	Rerun  int       `json:"rerun"`  // 是否重跑，是，会覆盖已有数据；否，不会覆盖已有数据
	Jobs   []CronJob `json:"jobs"`   // 定时任务列表
}

type AccountCookie struct {
	Account  string `json:"account"`
	Password string `json:"password"`
	Cookie   string `json:"cookie"`
}

type CookieList struct {
	Cookies  []AccountCookie `json:"cookies"`
	Platform string          `json:"platform"` // 平台，SEM/AD/STORE
	Service  string          `json:"service"`  // 服务，GDT/WNYS/LH/JRTT 等
	URL      string          `json:"url"`
}

type CookieConfig struct {
	Data []CookieList `json:"data"`
}
