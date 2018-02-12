package dingding

import (
	"github.com/satori/go.uuid"
	"net/url"
	. "quantum/defs/sdk/service/dingding"
	. "quantum/defs/util"
	"quantum/util"
	"strconv"
	"strings"
	//"time"
)

func parse_task(task Task) Request {
	msg := Request{}
	msg.ClientId = DEFAULT_CLIENT_ID
	msg.Secret = DEFAULT_SECRET
	msg.Type = DEFAULT_TYPE
	msg.GroupId = ""
	msg.Title = ""
	err := msg.UnmarshalJSON(task.Body)
	if err != nil {
		util.Log("[Error] Failed in rendering json data", err)
	}
	return msg
}

func compute_sign(msg Request, nonce string) string {
	params := map[string]string{}
	params[PARAM_CLIENT_ID] = strconv.Itoa(msg.ClientId)
	params[PARAM_NONCE] = nonce
	params[PARAM_MESSAGE] = msg.Message
	params[PARAM_TYPE] = msg.Type
	switch len(msg.GroupId) {
	case 0:
		switch len(msg.Title) {
		case 0:
			build_msg_send_params(msg, params)
		default:
			build_chat_send_params(msg, params)
		}
	default:
		build_group_send_params(msg, params)
	}
	keys, data := util.SortMapString(params)
	body := util.CombineListParamsSorted([]string{}, keys, data)
	clientId := strconv.Itoa(msg.ClientId)
	secret := msg.Secret
	sign := strings.ToLower(util.MD5Sum(clientId, secret, nonce, body))
	util.Log("Sign:", sign)
	return sign
}

func build_body(msg Request) string {
	data := url.Values{}
	//nonce := strconv.FormatInt(time.Now().Unix(), 10)
	nonce := uuid.NewV4().String()
	data[PARAM_CLIENT_ID] = []string{strconv.Itoa(msg.ClientId)}
	data[PARAM_SIGNATURE] = []string{compute_sign(msg, nonce)}
	data[PARAM_NONCE] = []string{nonce}
	data[PARAM_MESSAGE] = []string{msg.Message}
	data[PARAM_TYPE] = []string{msg.Type}
	switch len(msg.GroupId) {
	case 0:
		switch len(msg.Title) {
		case 0:
			build_msg_send_data(msg, data)
		default:
			build_chat_send_data(msg, data)
		}
	default:
		build_group_send_data(msg, data)
	}
	return data.Encode()
}

func build_msg_send_data(msg Request, data url.Values) {
	data[PARAM_MSG_MOBILES] = []string{strings.Join(msg.Mobiles, ",")}
	data[PARAM_MSG_EMAILS] = []string{strings.Join(msg.Emails, ",")}
}

func build_msg_send_params(msg Request, params map[string]string) {
	params[PARAM_MSG_MOBILES] = strings.Join(msg.Mobiles, ",")
	params[PARAM_MSG_EMAILS] = strings.Join(msg.Emails, ",")
}

func build_chat_send_data(msg Request, data url.Values) {
	build_msg_send_data(msg, data)
	data[PARAM_CHAT_TITLE] = []string{msg.Title}
	data[PARAM_CHAT_OWNER] = []string{msg.Owner}
}

func build_chat_send_params(msg Request, params map[string]string) {
	build_msg_send_params(msg, params)
	params[PARAM_CHAT_TITLE] = msg.Title
	params[PARAM_CHAT_OWNER] = msg.Owner
}

func build_group_send_data(msg Request, data url.Values) {
	data[PARAM_GROUP_ID] = []string{msg.GroupId}
	data[PARAM_GROUP_ATMOBILES] = []string{strings.Join(msg.AtMobiles, ",")}
	data[PARAM_GROUP_ATEMAILS] = []string{strings.Join(msg.AtEmails, ",")}
	data[PARAM_GROUP_ISATALL] = []string{msg.IsAtAll}
}

func build_group_send_params(msg Request, params map[string]string) {
	params[PARAM_GROUP_ID] = msg.GroupId
	params[PARAM_GROUP_ATMOBILES] = strings.Join(msg.AtMobiles, ",")
	params[PARAM_GROUP_ATEMAILS] = strings.Join(msg.AtEmails, ",")
	params[PARAM_GROUP_ISATALL] = msg.IsAtAll
}

func build_headers() map[string]string {
	headers := map[string]string{}
	headers["Content-Type"] = "application/x-www-form-urlencoded"
	headers["Accept"] = "text/plain"
	return headers
}

func build_url(msg Request) string {
	path := PATH_MSG_SEND
	if len(msg.GroupId) > 0 {
		path = PATH_GROUP_SEND
	}
	if len(msg.Title) > 0 {
		path = PATH_CHAT_SEND
	}
	if msg.ClientId == TESTING_CLIENT_ID {
		return strings.Join([]string{TESTING_API, path}, "")
	}
	return strings.Join([]string{ONLINE_API, path}, "")
}

func parse_data(body []byte) Response {
	msg := Response{}
	err := msg.UnmarshalJSON(body)
	if err != nil {
		util.Log("Error in Parsing Json Data:", err)
	}
	return msg
}

func RunService(task Task, ch chan []byte, cache chan Cache, done chan int) {
	msg := parse_task(task)
	r := build_url(msg)
	d := build_body(msg)
	util.Log("Form Data:", d)
	b := util.HttpRequest(r, "POST", d, build_headers())
	ch <- b
	done <- SUCCESSFUL
}
