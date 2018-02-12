package api

import (
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/ad/gdt"
	. "quantum/defs/util"
	"quantum/util"
	"strconv"
	"strings"
)

func extract_campaigns(body []byte) ([]CampaignsGetDataList, int64, int) {
	data := []CampaignsGetDataList{}
	msg := CampaignsGetResponse{}
	err := msg.UnmarshalJSON(body)
	if err != nil {
		util.Log(err)
		return data, FAILED_JSON_UNMARSHAL, -1
	}
	page_info := msg.Data.PageInfo
	return msg.Data.List, msg.Code, page_info.TotalPage
}

func get_campaigns(reqUrl, method string, task_id, page int, params url.Values, headers map[string]string) ([]CampaignsGetDataList, int64, int) {
	params["nonce"] = []string{BuildNonce(task_id, params)}
	params["page"] = []string{strconv.Itoa(page)}
	params["page_size"] = []string{strconv.FormatInt(MAX_PAGESIZE, 10)}
	params["timestamp"] = []string{util.GetTimestamp(0)}
	h := []string{reqUrl, params.Encode()}
	u := strings.Join(h, "?")
	util.Log("CAMPAIGNS REPORT REQUEST:\n", u)
	body := util.HttpRequest(u, method, "", headers)
	util.Log("CAMPAIGNS REPORT RESPONSE:\n", string(body))
	return extract_campaigns(body)
}

func ProcessCampaigns(reqUrl, method string, taskId int, params url.Values, headers map[string]string) int {
	page := 1
	data, code, total_pages := get_campaigns(reqUrl, method, taskId, page, params, headers)
	if code > 0 {
		return int(code)
	}
	campaigns := make([]CampaignsGetDataList, len(data))
	for i, v := range data {
		campaigns[i] = v
	}
	for page < total_pages {
		page += 1
		data, code, _ = get_campaigns(reqUrl, method, taskId, page, params, headers)
		if code > 0 {
			return int(code)
		}
		for _, v := range data {
			campaigns = append(campaigns, v)
		}
	}
	return SUCCESSFUL
}
