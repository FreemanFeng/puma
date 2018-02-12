package baidu

import (
	"math/rand"
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/sem/baidu"
	"quantum/util"
	"strings"
)

func build_params(task_id int, data, timestamp string) url.Values {
	params := util.ParseParams(data)
	return params
}

func build_url(service_id, method_id int) string {
	h := []string{API_URL}
	switch service_id {
	case ID_SERVICE_CAMPAIGN:
		h = append(h, SERVICE_CAMPAIGN)
	}
	switch method_id {
	case ID_METHOD_ADD_CAMPAIGN:
		h = append(h, METHOD_ADD_CAMPAIGN)
	}
	return strings.Join(h, "/")
}

func build_headers() map[string]string {
	headers := map[string]string{}
	headers["Content-Type"] = CT
	return headers
}

func dispatch(task_id, service_id int, reqUrl, method string,
	params url.Values, headers map[string]string, job CronJob, done chan int) {
	switch service_id {
	case ID_SERVICE_CAMPAIGN:
		//done <- ProcessCampaign(db, reqUrl, method, account_id, task_id, service_id, params, headers, online)
	default:
		util.Log("Unknown Service with ID", service_id)
		done <- FAILED_UNKNOWN_SERVICE
	}
}

func RunService(task_id, service_id int, job CronJob, data string, done chan int) {
	util.Log("Running Service for 百度")
	rand.Seed(util.Timestamp(0))
	ts := util.GetTimestamp(0)
	r := build_url(service_id, ID_METHOD_ADD_CAMPAIGN)
	params := build_params(task_id, data, ts)
	headers := build_headers()
	dispatch(task_id, service_id, r, HTTP_POST, params, headers, job, done)
}
