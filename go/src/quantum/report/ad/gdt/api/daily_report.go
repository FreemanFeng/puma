package api

import (
	"fmt"
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/ad/gdt"
	. "quantum/defs/util"
	"quantum/util"
	"strconv"
	"strings"
)

func extract_daily_report(level int, body []byte) (DailyReport, int64, string) {
	msg := DailyReportsGetResponse{}
	err := msg.UnmarshalJSON(body)
	if err != nil {
		util.Log(err)
		return DailyReport{}, FAILED_JSON_UNMARSHAL, "Error in Json Unmarshal"
	}
	if msg.Code != 0 {
		return DailyReport{}, msg.Code, msg.Message
	}
	data := make([]ReportData, len(msg.Data.List))
	for i, report := range msg.Data.List {
		data[i].Level = level
		data[i].Date = report.Date
		data[i].Yesterday = util.GetYesterday(report.Date)
		data[i].LastWeek = util.GetLastWeek(report.Date)
		switch level {
		case CAMPAIGN_LEVEL:
			data[i].CampaignID = report.CampaignID
		case ADGROUP_LEVEL:
			data[i].CampaignID = report.CampaignID
			data[i].AdgroupID = report.AdgroupID
		}
		data[i].Impression = report.Impression
		data[i].Click = report.Click
		data[i].Download = report.Download
		data[i].Cost, _ = strconv.ParseFloat(fmt.Sprintf("%.2f", float64(report.Cost/COST_BASE)), 64)
	}
	page_info := msg.Data.PageInfo
	report := DailyReport{Data: data, Pages: page_info.TotalPage}
	return report, msg.Code, msg.Message
}
func get_level(params url.Values) int {
	k, ok := params["level"]
	if ok {
		switch {
		case k[0] == "CAMPAIGN":
			return CAMPAIGN_LEVEL
		case k[0] == "ADGROUP":
			return ADGROUP_LEVEL
		}
	}
	return ADVERTISER_LEVEL
}

func get_daily_report(reqUrl, method string, task_id, page int, params url.Values, headers map[string]string) (DailyReport, int64, string) {
	level := get_level(params)
	_, ok := params["level"]
	if !ok {
		params["level"] = []string{"ADVERTISER"}
	}
	params["nonce"] = []string{BuildNonce(task_id, params)}
	params["page"] = []string{strconv.Itoa(page)}
	params["page_size"] = []string{strconv.FormatInt(MAX_PAGESIZE, 10)}
	params["timestamp"] = []string{util.GetTimestamp(0)}
	h := []string{reqUrl, params.Encode()}
	u := strings.Join(h, "?")
	body := util.HttpRequest(u, method, "", headers)
	util.Log("DAILY REPORT RESPONSE:", string(body))
	return extract_daily_report(level, body)
}

func ProcessDailyReport(reqUrl, method string, taskId int, params url.Values, headers map[string]string) int {
	page := 1
	data, code, message := get_daily_report(reqUrl, method, taskId, page, params, headers)
	if code > 0 {
		util.Log("Error:", message)
		return int(code)
	}
	report := make([]ReportData, len(data.Data))
	for i, v := range data.Data {
		report[i] = v
	}
	for page < data.Pages {
		page += 1
		data, code, message = get_daily_report(reqUrl, method, taskId, page, params, headers)
		if code > 0 {
			util.Log("Error:", message)
			return int(code)
		}
		for _, v := range data.Data {
			report = append(report, v)
		}
	}
	return SUCCESSFUL
}
