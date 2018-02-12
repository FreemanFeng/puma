package gdt

import (
	"net/url"
	. "quantum/defs/report/ad/gdt"
	"quantum/util"
	"strconv"
	"strings"
)

func query_code(account_id string) string {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(QUERY_AUTHORIZATION_CODE), "&query=", account_id}
	r := strings.Join(s, "")
	b := util.HttpRequest(r, "GET", "", map[string]string{})
	return string(b)
}

func query_token(account_id string) string {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(QUERY_TOKEN), "&query=", account_id}
	r := strings.Join(s, "")
	b := util.HttpRequest(r, "GET", "", map[string]string{})
	return string(b)
}

func query_refresh_token(account_id string) string {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(QUERY_REFRESH_TOKEN), "&query=", account_id}
	r := strings.Join(s, "")
	b := util.HttpRequest(r, "GET", "", map[string]string{})
	return string(b)
}

func query_idle(account_id string) string {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(QUERY_IDLE), "&query=", account_id}
	r := strings.Join(s, "")
	b := util.HttpRequest(r, "GET", "", map[string]string{})
	return string(b)
}

func config_token(account_id string, token string) {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(CONFIG_TOKEN), "&config=", account_id, "&data=", token}
	r := strings.Join(s, "")
	util.HttpRequest(r, "GET", "", map[string]string{})
}

func config_refresh_token(account_id string, refresh_token string) {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(CONFIG_REFRESH_TOKEN), "&config=", account_id, "&data=", refresh_token}
	r := strings.Join(s, "")
	util.HttpRequest(r, "GET", "", map[string]string{})
}

func config_last_visit(account_id string) {
	s := []string{REDIRECT_URI, "/?type=", strconv.Itoa(CONFIG_LAST_VISIT), "&config=", account_id, "&data=1"}
	r := strings.Join(s, "")
	util.HttpRequest(r, "GET", "", map[string]string{})
}

func extract_token_response(body []byte) TokenData {
	msg := TokenResponse{}
	err := msg.UnmarshalJSON(body)
	if err != nil {
		util.Log(err)
	}
	util.Log("Code:", msg.Code, "Message:", msg.Message)
	return msg.Data
}

func get_token_with_code(auth_url, method, client_id, code, client_secret string) (string, string) {
	params := url.Values{}
	params[PARAM_CLIENT_ID] = []string{client_id}
	params[PARAM_CLIENT_SECRET] = []string{client_secret}
	params[PARAM_AUTHORIZATION_CODE] = []string{code}
	params[PARAM_GRANT_TYPE] = []string{PARAM_AUTHORIZATION_CODE}
	params[PARAM_REDIRECT_URI] = []string{REDIRECT_URI}
	req_url := strings.Join([]string{auth_url, params.Encode()}, "?")
	util.Log("TOKEN REQUEST:", req_url)
	body := util.HttpRequest(req_url, method, "", map[string]string{})
	data := extract_token_response(body)
	return data.AccessToken, data.RefreshToken
}

func get_token_with_refresh_token(auth_url, method, client_id, refresh_token, client_secret string) string {
	params := url.Values{}
	params[PARAM_CLIENT_ID] = []string{client_id}
	params[PARAM_CLIENT_SECRET] = []string{client_secret}
	params[PARAM_REFRESH_TOKEN] = []string{refresh_token}
	params[PARAM_GRANT_TYPE] = []string{PARAM_REFRESH_TOKEN}
	util.Log("TOKEN REQUEST:", auth_url)
	req_url := strings.Join([]string{auth_url, params.Encode()}, "?")
	body := util.HttpRequest(req_url, method, "", map[string]string{})
	data := extract_token_response(body)
	return data.AccessToken
}

func GetToken(auth_url, method, account_id, app_id, app_key string) (string, string) {
	code := query_code(account_id)
	token := query_token(account_id)
	refresh_token := query_refresh_token(account_id)
	util.Log("Authentication Code[", code, "] Token [", token, "] Refresh Token[", refresh_token, "]")
	if len(code)+len(token)+len(refresh_token) == 0 {
		util.Log("Please do OAuth2 Authentication First")
		return token, ""
	}
	switch len(token) {
	case 0:
		switch len(refresh_token) {
		case 0:
			switch len(code) {
			case 0:
				return "", ""
			default:
				// 重新授权后,通过授权码获取Token
				t, r := get_token_with_code(auth_url, method, app_id, code, app_key)
				util.Log("Use Authentication Code [", code,
					"] and Get Token [", t, "] and Refresh Token[", r, "]")
				config_token(account_id, t)
				config_refresh_token(account_id, r)
				idle := query_idle(account_id)
				return t, idle
			}
		default:
			// Token过期，通过Refresh Token获取Token
			t := get_token_with_refresh_token(auth_url, method, app_id, refresh_token, app_key)
			util.Log("Token Expired, Use Refresh Token[", refresh_token, "] and Get Token[", t, "]")
			config_token(account_id, t)
			return t, ""
		}
	default:
		return token, ""
	}
}
