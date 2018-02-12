package baidu

type Token struct {
	TokenType, AccountID int
	Data                 string
}

type ReportData struct {
	Date, Yesterday, LastWeek                           string
	Level                                               int
	CampaignID, AdgroupID, AccountID, Impression        int64
	Click, Download, Nu, YesterdayNu, LastweekNu        int64
	Cost, RealCost, YesterdayCost, LastWeekCost         float64
	Roi7, Roi15, RoiOper7, RoiOper15, Income7, Income15 float64
	Cost7, Cost15, CostOper7, CostOper15, Lt            float64
	Day1, Day7, Day30, Dau, Dau30                       float64
}

type Account struct {
	Id, PlatformId, ProductId              int64
	Rebate, Budget, Cost, Balance          float64
	AdvertiserId, AppId, AppKey, UmAccount string
}
type RestTask struct {
	Id, PlatformId, ProductId, AccountId             int64
	StartDate, EndDate, Username, Status, CreateTime string
}

type DailyReport struct {
	Data  []ReportData
	Pages int
}

type ParamsData struct {
	Key, Value string
}

type ParamsSorter struct {
	Params []ParamsData
	By     func(p1, p2 *ParamsData) bool
}
