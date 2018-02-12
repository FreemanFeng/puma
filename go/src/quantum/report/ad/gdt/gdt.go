package gdt

import (
	"math/rand"
	"net/url"
	. "quantum/defs/report"
	. "quantum/defs/report/ad/gdt"
	. "quantum/report/ad/gdt/api"
	"quantum/util"
	"strings"
)

func build_params(task_id int, data, access_token, advertiser_id, timestamp string) url.Values {
	params := util.ParseParams(data)
	params[PARAM_ACCOUNT_ID] = []string{advertiser_id}
	params[PARAM_ACCESS_TOKEN] = []string{access_token}
	params[PARAM_TIMESTAMP] = []string{timestamp}
	params[PARAM_NONCE] = []string{BuildNonce(task_id, params)}
	return params
}

func build_url(api_version string, service_id int) string {
	h := []string{API_URL, api_version}
	if len(api_version) == 0 {
		h = append(h, API_VERSION)
	}
	switch service_id {
	case TOKEN_GET:
		h = []string{OAUTH_URL, URL_PATH_TOKEN}
	case DAILY_ACCOUNT_REPORTS_GET:
		h = append(h, URL_PATH_DAILY_REPORTS_GET)
	case HOURLY_ACCOUNT_REPORTS_GET:
		h = append(h, URL_PATH_HOURLY_REPORTS_GET)
	case CAMPAIGN_GET:
		h = append(h, URL_PATH_CAMPAIGNS_GET)
	case ADGROUP_GET:
		h = append(h, URL_PATH_ADGROUPS_GET)
	case CREATIVE_GET:
		h = append(h, URL_PATH_ADCREATIVES_GET)
	case AD_GET:
		h = append(h, URL_PATH_ADS_GET)
	}
	return strings.Join(h, "/")
}

func build_method(serviceId int) string {
	switch serviceId % METHOD_BASE {
	case GET:
		return HTTP_GET
	}
	return HTTP_POST
}

func build_headers() map[string]string {
	headers := map[string]string{}
	headers["Content-Type"] = CT
	headers["User-Agent"] = UA
	return headers
}

func is_token_needed(serviceId int) bool {
	switch serviceId {
	case UM_GET:
		return false
	case SBS_ACCOUNT_GET:
		return false
	}
	return true
}

func dispatch(taskId, serviceId int, reqUrl, method string,
	params url.Values, headers map[string]string, job CronJob, done chan int) {
	switch serviceId {
	case DAILY_ACCOUNT_REPORTS_GET:
		done <- ProcessDailyReport(reqUrl, method, taskId, params, headers)
	case CAMPAIGN_GET:
		done <- ProcessCampaigns(reqUrl, method, taskId, params, headers)
	case ADGROUP_GET:
		done <- ProcessAdgroups(reqUrl, method, taskId, params, headers)
	default:
		util.Log("Unknown Service with ID", serviceId)
		done <- FAILED_UNKNOWN_SERVICE
	}
}

func RunService(taskId, serviceId, readTimeout, writeTimeout int, job CronJob, data string, done chan int) {
	access_token := ""
	util.Log("Running Service for 广点通")
	if serviceId == CALLBACK_SERVICE {
		HandleCallback(readTimeout, writeTimeout, done)
		return
	}
	rand.Seed(util.Timestamp(0))
	if is_token_needed(serviceId) {
		r := build_url(job.APIVersion, TOKEN_GET)
		m := build_method(TOKEN_GET)
		access_token, _ = GetToken(r, m, job.Account, job.ClientID, job.ClientSecret)
		if len(access_token) == 0 {
			return
		}
	}
	ts := util.GetTimestamp(0)
	r := build_url(job.APIVersion, serviceId)
	m := build_method(serviceId)
	params := build_params(taskId, data, access_token, job.Account, ts)
	headers := build_headers()
	dispatch(taskId, serviceId, r, m, params, headers, job, done)
}
