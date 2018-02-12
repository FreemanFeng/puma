package gdt

type Token struct {
	TokenType, AccountID int
	Data                 string
}

type RestTask struct {
	Id, PlatformId, ProductId, AccountId             int64
	StartDate, EndDate, Username, Status, CreateTime string
}

type ParamsData struct {
	Key, Value string
}

type ParamsSorter struct {
	Params []ParamsData
	By     func(p1, p2 *ParamsData) bool
}
