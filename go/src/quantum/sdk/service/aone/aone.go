package aone

import (
	. "quantum/defs/sdk/service/aone"
	. "quantum/defs/util"
	"quantum/util"
	"strings"
)

func parse_task(task Task) Request {
	msg := Request{}
	msg.Debug = ""
	msg.Secret = ""
	msg.App = ""
	err := msg.UnmarshalJSON(task.Body)
	if err != nil {
		util.Log("[Error] Failed in rendering json data", err)
	}
	if len(msg.Secret) == 0 {
		if len(msg.Debug) > 0 {
			msg.Secret = TESTING_ACCESS_KEY
		} else {
			msg.Secret = ONLINE_ACCESS_KEY
		}
	}
	if len(msg.App) == 0 {
		msg.App = DEFAULT_APP_NAME
	}
	return msg
}

func compute_signature(msg Request) ([]byte, error) {
	timestamp := util.GetMillisecond()
	s := []string{"appName=", msg.App, ";timestamp=", timestamp}
	src := strings.Join(s, "")
	key, _ := util.Base64URLDecode(msg.Secret)
	cryptText := util.AesECBEncrypt(src, string(key))
	signature := util.Base64UrlSafeEncode(cryptText)
	response := Response{Timestamp: timestamp, Signature: signature}
	return response.MarshalJSON()
}

func RunService(task Task, ch chan []byte, cache chan Cache, done chan int) {
	msg := parse_task(task)
	data, err := compute_signature(msg)
	if err != nil {
		util.Log("Failed in Creating Json Response data, err:", err)
		ch <- []byte("")
		done <- FAILED
	}
	util.Log("response:", string(data))
	ch <- []byte(data)
	done <- SUCCESSFUL
}
