package util

type DateSelect struct {
	StartDate string `json:"start_date"`
	EndDate   string `json:"end_date"`
}

type IDList struct {
	Data []string `json:"data"`
}
