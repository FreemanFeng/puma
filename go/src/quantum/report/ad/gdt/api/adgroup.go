package api

import (
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/ad/gdt"
	. "quantum/defs/util"
	"quantum/util"
	"strconv"
	"strings"
	"time"
)

func extract_adgroups(body []byte) ([]AdgroupsGetDataList, int64, int) {
	data := []AdgroupsGetDataList{}
	msg := AdgroupsGetResponse{}
	err := msg.UnmarshalJSON(body)
	if err != nil {
		util.Log(err)
		return data, FAILED_JSON_UNMARSHAL, -1
	}
	page_info := msg.Data.PageInfo
	return msg.Data.List, msg.Code, page_info.TotalPage
}

func get_adgroups(req_url, method string, task_id, page int, params url.Values, headers map[string]string) ([]AdgroupsGetDataList, int64, int) {
	params["nonce"] = []string{BuildNonce(task_id, params)}
	params["page"] = []string{strconv.Itoa(page)}
	params["page_size"] = []string{strconv.FormatInt(MIN_PAGESIZE, 10)}
	params["timestamp"] = []string{util.GetTimestamp(0)}
	h := []string{req_url, params.Encode()}
	u := strings.Join(h, "?")
	util.Log("ADGROUPS REPORT REQUEST:\n", u)
	body := util.HttpRequest(u, method, "", headers)
	util.Log("ADGROUPS REPORT RESPONSE:\n", string(body))
	return extract_adgroups(body)
}

func get_all_adgroups(req_url, method string, task_id, page int, params url.Values, headers map[string]string) ([]AdgroupsGetDataList, int64, int) {
	data, code, total_pages := get_adgroups(req_url, method, task_id, page, params, headers)
	for i := 0; i < MAX_RETRY; i++ {
		if len(data) > 0 {
			return data, code, total_pages
		}
		util.Log("Retry[", i, "] Getting Adgroups ...")
		time.Sleep(RETRY_INTERVAL * time.Second)
		data, code, total_pages = get_adgroups(req_url, method, task_id, page, params, headers)
	}
	return data, code, total_pages
}

func ProcessAdgroups(reqUrl, method string, taskId int, params url.Values, headers map[string]string) int {
	page := 1
	data, code, total_pages := get_all_adgroups(reqUrl, method, taskId, page, params, headers)
	if code > 0 {
		return int(code)
	}
	adgroups := make([]AdgroupsGetDataList, len(data))
	for i, v := range data {
		adgroups[i] = v
	}
	for page < total_pages {
		page += 1
		data, code, _ = get_all_adgroups(reqUrl, method, taskId, page, params, headers)
		if code > 0 {
			return int(code)
		}
		for _, v := range data {
			adgroups = append(adgroups, v)
		}
	}
	return SUCCESSFUL
}
