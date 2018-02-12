package report

type TaskStatus struct {
	Status, Id int
}

type ReportData struct {
	Date, Yesterday, LastWeek                           string
	Level                                               int
	CampaignID, AdgroupID, AccountID, Impression        int64
	Click, Download, Nu, YesterdayNu, LastweekNu        int64
	Cost, RealCost, YesterdayCost, LastWeekCost         float64
	Roi7, Roi15, RoiOper7, RoiOper15, Income7, Income15 float64
	Cost7, Cost15, CostOper7, CostOper15, Lt, Qr        float64
	Ret1, Ret7, Ret30, Dau, Dau30                       int64
}

type DailyReport struct {
	Data  []ReportData
	Pages int
}

type Account struct {
	Id, PlatformId, ProductId, Device              int64
	Rebate, Budget, Cost, Balance                  float64
	AdvertiserId, AppId, AppKey, UmAccount         string
	Token, Bid, AccountUsage, Password, UpdateTime string
}

type UmAccount struct {
	ID, AccountID, ProductID, PID int64
	Account                       string
}
